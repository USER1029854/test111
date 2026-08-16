"""Ground-truth liquidity verification for the top kept candidates.

The client explicitly does not trust headline liquidity/TVL at face value. For
each of the top-N candidates (by reported liquidity_usd) in arb_contract_logic.csv:

  1. Re-fetch the pair LIVE from DEXScreener (freshness + gives the native
     base/quote reserve breakdown DS itself computed: `liquidity.quote`).
  2. Independently read the quote token's on-chain balance AT the pair address
     via `balanceOf(pairAddress)` on the public Arbitrum RPC -- this is real
     ground truth: whatever DEXScreener or GeckoTerminal say, this is what the
     pool contract actually holds right now.
  3. Compare the two quote-side reserve numbers directly (native units,
     apples-to-apples, no USD conversion needed for this part).
  4. Only if the quote token is a MAJOR (WETH/USDC/USDC.e/USDT/ARB/WBTC) is a
     USD figure trusted: converted using an INDEPENDENT price source
     (CoinGecko simple/price, not GeckoTerminal/DEXScreener) so the USD
     conversion itself isn't circular.
  5. If the quote token is NOT a major, the headline USD liquidity is marked
     UNVERIFIED/SOFT, and a secondary check looks at whether that quote token
     itself has real backing (its own deepest pair, ideally against a major).

A pool with no code at the reported pair address, or a balanceOf call that
reverts/returns nothing, is recorded as UNVERIFIABLE -- never silently
promoted to verified.
"""
import requests, json, csv, time, sys

H = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
DS = "https://api.dexscreener.com"
DATA = "/home/user/test111/data"
RPCS = ["https://arb1.arbitrum.io/rpc", "https://arbitrum.llamarpc.com",
        "https://arbitrum-one.publicnode.com"]

MAJORS = {
    "0x82af49447d8a07e3bd95bd0d56f35241523fbab1": ("WETH", "ethereum"),
    "0xaf88d065e77c8cc2239327c5edb3a432268e5831": ("USDC", None),      # stable, $1
    "0xff970a61a04b1ca14834a43f5de4533ebddb5cc8": ("USDC.e", None),    # stable, $1
    "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9": ("USDT", None),      # stable, $1
    "0x912ce59144191c1204e64559fe8253a0e49e6548": ("ARB", "arbitrum"),
    "0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f": ("WBTC", "bitcoin"),
}
TOPN = int(sys.argv[1]) if len(sys.argv) > 1 else 20

def rpc(payload, tries=3):
    for url in RPCS:
        for t in range(tries):
            try:
                r = requests.post(url, timeout=15, json=payload)
                if r.status_code == 200:
                    j = r.json()
                    if "result" in j:
                        return j["result"]
                if r.status_code == 429:
                    time.sleep(1.0 * (t + 1)); continue
            except Exception:
                time.sleep(0.4)
    return None

def get_code(addr):
    return rpc({"jsonrpc":"2.0","id":1,"method":"eth_getCode","params":[addr,"latest"]})

def eth_call(to, data):
    return rpc({"jsonrpc":"2.0","id":1,"method":"eth_call","params":[{"to":to,"data":data},"latest"]})

def balance_of(token, holder):
    padded = holder.lower().replace("0x", "").rjust(64, "0")
    r = eth_call(token, "0x70a08231" + padded)
    if not r or r in ("0x", "0x0"):
        return None
    try:
        return int(r, 16)
    except Exception:
        return None

def decimals_of(token):
    r = eth_call(token, "0x313ce567")
    if not r or r in ("0x", "0x0"):
        return None
    try:
        return int(r, 16)
    except Exception:
        return None

def ds_get(url, tries=3):
    for t in range(tries):
        try:
            r = requests.get(url, timeout=30, headers=H)
            if r.status_code == 200:
                return r.json()
            if r.status_code == 429:
                time.sleep(4 * (t + 1)); continue
        except Exception:
            time.sleep(1.5)
    return None

def cg_prices(ids):
    d = ds_get(f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(ids)}&vs_currencies=usd")
    if not isinstance(d, dict):
        return {}
    return {k: v.get("usd") for k, v in d.items() if isinstance(v, dict) and "usd" in v}

def ds_top_pair_for_token(addr):
    """Independent liquidity-backing check for a non-major quote token: does IT
    have a deep pair against a major, elsewhere?"""
    d = ds_get(f"{DS}/token-pairs/v1/arbitrum/{addr}")
    if not isinstance(d, list) or not d:
        return None
    best = max(d, key=lambda p: float(((p.get("liquidity") or {}).get("usd")) or 0))
    return best

rows = list(csv.DictReader(open(f"{DATA}/arb_contract_logic.csv")))
rows.sort(key=lambda r: -float(r["liquidity_usd"]))
top = rows[:TOPN]
print(f"verifying top {len(top)} of {len(rows)} kept candidates on-chain\n")

prices = cg_prices(["ethereum", "arbitrum", "bitcoin"])
print(f"independent CoinGecko reference prices: {prices}\n")
PRICE_MAP = {"ethereum": prices.get("ethereum"), "arbitrum": prices.get("arbitrum"),
             "bitcoin": prices.get("bitcoin")}

out = []
for i, r in enumerate(top):
    sym, tok, pair, qaddr = r["symbol"], r["token_address"], r["pair_address"], r.get("quote_address") or ""
    liq_reported = float(r["liquidity_usd"])
    rec = {"symbol": sym, "token_address": tok, "pair_address": pair,
           "quote_symbol": r["quote"], "quote_address": qaddr,
           "liquidity_usd_reported": liq_reported}

    # 1. live DS re-fetch
    live = ds_get(f"{DS}/latest/dex/pairs/arbitrum/{pair}")
    pairs = (live or {}).get("pairs") or []
    p = pairs[0] if pairs else None
    if not p:
        rec.update(status="UNVERIFIABLE", note="live DEXScreener re-fetch returned no pair")
        out.append(rec); print(f"  [{i+1}] {sym:<12} UNVERIFIABLE - no live DS data"); continue

    ds_liq_usd = float(((p.get("liquidity") or {}).get("usd")) or 0)
    ds_liq_quote_native = (p.get("liquidity") or {}).get("quote")
    ds_liq_base_native = (p.get("liquidity") or {}).get("base")
    rec.update(liquidity_usd_live=ds_liq_usd, ds_quote_native=ds_liq_quote_native,
               ds_base_native=ds_liq_base_native)

    # 2. on-chain contract existence
    code = get_code(pair)
    has_code = bool(code) and code not in ("0x", "0x0")
    rec["pair_has_onchain_code"] = has_code
    if not has_code:
        rec.update(status="UNVERIFIABLE", note="no bytecode at reported pair address on-chain")
        out.append(rec); print(f"  [{i+1}] {sym:<12} UNVERIFIABLE - pair address has no code"); continue

    qaddr_l = (qaddr or "").lower()
    is_major = qaddr_l in MAJORS

    # 3. on-chain quote-side balance (works regardless of AMM design: V2 pair,
    # V3/V4 pool, Solidly, etc. -- balanceOf is universal, getReserves() is not)
    dec = decimals_of(qaddr) if qaddr else None
    bal = balance_of(qaddr, pair) if qaddr else None
    if bal is None or dec is None:
        rec.update(status="UNVERIFIABLE", note="balanceOf/decimals call failed on quote token")
        out.append(rec); print(f"  [{i+1}] {sym:<12} UNVERIFIABLE - RPC balanceOf/decimals failed"); continue

    onchain_native = bal / (10 ** dec)
    rec["onchain_quote_balance_native"] = onchain_native

    pct_diff_native = None
    if ds_liq_quote_native:
        try:
            pct_diff_native = abs(onchain_native - float(ds_liq_quote_native)) / max(float(ds_liq_quote_native), 1e-9) * 100
        except Exception:
            pct_diff_native = None
    rec["native_reserve_pct_diff"] = round(pct_diff_native, 2) if pct_diff_native is not None else None

    if is_major:
        qsym, cgid = MAJORS[qaddr_l]
        price = 1.0 if cgid is None else PRICE_MAP.get(cgid)
        rec["quote_is_major"] = True
        rec["independent_price_usd"] = price
        if price:
            onchain_usd_one_side = onchain_native * price
            rec["onchain_quote_side_usd"] = round(onchain_usd_one_side, 2)
            # sanity band: total pool USD should be same order of magnitude as
            # 2x one side for a roughly-balanced pool; concentrated-liquidity
            # (V3/V4) pools can be skewed, so the band is deliberately wide.
            implied_total = onchain_usd_one_side * 2
            ratio = implied_total / max(liq_reported, 1e-9)
            rec["implied_total_from_onchain_usd"] = round(implied_total, 2)
            rec["ratio_onchain_implied_vs_reported"] = round(ratio, 3)
            native_ok = pct_diff_native is None or pct_diff_native < 20
            magnitude_ok = 0.15 <= ratio <= 6.0   # generous: catches order-of-magnitude fraud, not price noise
            if native_ok and magnitude_ok:
                rec["status"] = "VERIFIED_ONCHAIN"
            else:
                rec["status"] = "MISMATCH"
                rec["note"] = f"native_diff={rec['native_reserve_pct_diff']}% ratio={ratio:.2f}x"
        else:
            rec["status"] = "PARTIAL_ONCHAIN"
            rec["note"] = "on-chain native reserve read OK, no independent USD price available"
    else:
        rec["quote_is_major"] = False
        # secondary check: does the quote token itself have real backing?
        backing = ds_top_pair_for_token(qaddr) if qaddr else None
        if backing:
            bq = (backing.get("quoteToken") or {}).get("address", "").lower()
            bliq = float(((backing.get("liquidity") or {}).get("usd")) or 0)
            rec["quote_token_best_own_pair_quote"] = (backing.get("quoteToken") or {}).get("symbol")
            rec["quote_token_best_own_pair_liq_usd"] = bliq
            rec["quote_token_backed_by_major"] = bq in MAJORS
        else:
            rec["quote_token_backed_by_major"] = False
            rec["quote_token_best_own_pair_liq_usd"] = 0
        native_ok = pct_diff_native is None or pct_diff_native < 20
        rec["status"] = "SOFT_UNVERIFIED_NONMAJOR_QUOTE" if native_ok else "MISMATCH"
        rec["note"] = ("on-chain token count matches DS, but quote token is not a major asset -- "
                        "headline USD figure is not independently priced" if native_ok else
                        f"native token-count mismatch {rec['native_reserve_pct_diff']}% AND non-major quote")

    out.append(rec)
    print(f"  [{i+1}] {sym:<12} {rec['status']:<28} quote={r['quote']:<8} "
          f"reported=${liq_reported:>12,.0f}  native_diff={rec.get('native_reserve_pct_diff')}"
          f"  ratio={rec.get('ratio_onchain_implied_vs_reported')}")
    time.sleep(0.15)

json.dump({"generated_prices": PRICE_MAP, "results": out}, open(f"{DATA}/arb_liquidity_verification.json", "w"), indent=1)
n_ver = sum(1 for r in out if r["status"] == "VERIFIED_ONCHAIN")
n_soft = sum(1 for r in out if r["status"] == "SOFT_UNVERIFIED_NONMAJOR_QUOTE")
n_mismatch = sum(1 for r in out if r["status"] == "MISMATCH")
n_unver = sum(1 for r in out if r["status"] in ("UNVERIFIABLE", "PARTIAL_ONCHAIN"))
print(f"\nVERIFIED_ONCHAIN={n_ver}  SOFT_NONMAJOR_QUOTE={n_soft}  MISMATCH={n_mismatch}  UNVERIFIABLE/PARTIAL={n_unver}")
print("wrote arb_liquidity_verification.json")
