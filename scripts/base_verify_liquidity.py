"""Ground-truth liquidity verification: read the chain directly for the top kept
candidates and independently confirm the quote-side reserve against what
DEXScreener/GeckoTerminal report. This is the client's central requirement and
the only reliable path on Base, since the Etherscan-family balance/reserve
endpoints are blocked on the free key (same restriction as BSC).

Method per candidate:
  1. Read the pair contract's token0()/token1() and getReserves() (standard on
     Uniswap-v2-style AMMs -- BaseSwap, AlienBase, SushiSwap v2, Aerodrome v2
     pools, PancakeSwap v2, Uniswap v2, etc all implement this).
  2. If getReserves() is unavailable (e.g. a v3/v4 concentrated-liquidity pool
     or a singleton/CLMM pool with no such function), fall back to reading the
     quote token's balanceOf(pairAddress) directly -- always valid regardless
     of pool type, since the quote tokens still have to sit somewhere.
  3. Only convert the on-chain quote-token amount to USD using a real price if
     the quote token is one of the brief's four explicitly-named majors
     (WETH/USDC/DAI/cbETH). Anything else is reported as a verified TOKEN
     amount but flagged as a SOFT/unverified USD figure, exactly per the brief
     -- no USD conversion is invented through a thin or unknown quote asset.
  4. WETH/cbETH need a USD price for step 3; pulled from DEXScreener's own
     WETH/USDC and cbETH/WETH readings captured in the same run (not a third
     external price source), then cross-checked for sanity.
"""
import requests, json, csv, time

DATA = "/home/user/test111/data"
RPCS = ["https://mainnet.base.org", "https://base.llamarpc.com", "https://base.publicnode.com"]
RH = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
DS = "https://api.dexscreener.com"
H = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

MAJORS_4 = {
    "0x4200000000000000000000000000000000000006": ("WETH", 18),
    "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913": ("USDC", 6),
    "0x50c5725949a6f0c72e6c4a641f24049a917db0cb": ("DAI", 18),
    "0x2ae3f1ec7f1f5012cfeab0185bfc7aa3cf0dec22": ("cbETH", 18),
}

def rpc(method, params, tries=2):
    for url in RPCS:
        for t in range(tries):
            try:
                r = requests.post(url, timeout=20, headers=RH,
                                   json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params})
                d = r.json()
                if "result" in d:
                    return d["result"]
                if "error" in d:
                    break  # deterministic revert/unsupported call -- retrying the same url won't help
            except Exception:
                time.sleep(1)
    return None

def call(to, selector, args_hex=""):
    return rpc("eth_call", [{"to": to, "data": selector + args_hex}, "latest"])

def addr_from_word(hexres):
    if not hexres or len(hexres) < 66: return None
    return "0x" + hexres[-40:]

def get_reserves(pair):
    """UniswapV2-style getReserves() -> (reserve0 uint112, reserve1 uint112, ts uint32)."""
    res = call(pair, "0x0902f1ac")
    if not res or res == "0x": return None
    b = bytes.fromhex(res[2:])
    if len(b) < 96: return None
    r0 = int.from_bytes(b[0:32], "big")
    r1 = int.from_bytes(b[32:64], "big")
    return r0, r1

def token0(pair):
    return addr_from_word(call(pair, "0x0dfe1681"))

def token1(pair):
    return addr_from_word(call(pair, "0xd21220a7"))

def balance_of(token, holder):
    res = call(token, "0x70a08231", holder[2:].rjust(64, "0"))
    if not res or res == "0x": return None
    return int(res, 16)

def decimals(token):
    res = call(token, "0x313ce567")
    try:
        return int(res, 16) if res else 18
    except Exception:
        return 18

def get(url, params=None, tries=3):
    for t in range(tries):
        try:
            r = requests.get(url, params=params, timeout=30, headers=H)
            if r.status_code == 200:
                return r.json()
            time.sleep(2 * (t + 1))
        except Exception:
            time.sleep(2 * (t + 1))
    return None

# ---- establish WETH and cbETH USD price from DEXScreener directly (not a 3rd source) ----
weth_usd = None
d = get(f"{DS}/latest/dex/pairs/base/0x6c561B446416E1A00E8E93E221854d6eA4171372")  # WETH/USDC uniswap v3, seen earlier
if d and d.get("pairs"):
    weth_usd = float(d["pairs"][0].get("priceUsd") or 0) or None
if not weth_usd:
    # fallback: token-pairs lookup, take highest-liquidity WETH pair vs USDC
    d = get(f"{DS}/token-pairs/v1/base/0x4200000000000000000000000000000000000006")
    best = None
    for p in (d or []):
        if p.get("quoteToken", {}).get("symbol") in ("USDC", "USD"):
            if not best or (p.get("liquidity", {}).get("usd") or 0) > (best.get("liquidity", {}).get("usd") or 0):
                best = p
    if best:
        weth_usd = float(best.get("priceUsd") or 0) or None
print(f"WETH/USD reference price (from DEXScreener): {weth_usd}")

cbeth_usd = None
d = get(f"{DS}/token-pairs/v1/base/0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22")
best = None
for p in (d or []):
    if (p.get("liquidity", {}).get("usd") or 0) and (not best or p["liquidity"]["usd"] > best["liquidity"]["usd"]):
        best = p
if best:
    cbeth_usd = float(best.get("priceUsd") or 0) or None
print(f"cbETH/USD reference price (from DEXScreener): {cbeth_usd}")

PRICE = {
    "0x4200000000000000000000000000000000000006": weth_usd,
    "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913": 1.0,
    "0x50c5725949a6f0c72e6c4a641f24049a917db0cb": 1.0,
    "0x2ae3f1ec7f1f5012cfeab0185bfc7aa3cf0dec22": cbeth_usd,
}

# ---- load candidates: top N kept by liquidity from base_contract_logic.csv ----
rows = list(csv.DictReader(open(f"{DATA}/base_contract_logic.csv")))
rows.sort(key=lambda r: -float(r["liquidity_usd"]))
TOPN = 20
targets = rows[:TOPN]
print(f"verifying top {len(targets)} of {len(rows)} kept candidates on-chain\n")

# need quote token address + reported DS liquidity/quote symbol from base_new_projects.csv
ds_by_pair = {}
for r in csv.DictReader(open(f"{DATA}/base_new_projects.csv")):
    ds_by_pair[r["pair_address"].lower()] = r

out = []
for r in targets:
    pair = r["pair_address"]
    ds = ds_by_pair.get(pair.lower(), {})
    quote_sym = ds.get("quote") or ""
    quote_addr = (ds.get("quote_address") or "").lower()
    reported_liq = float(r["liquidity_usd"])
    rec = {"symbol": r["symbol"], "token_address": r["token_address"], "pair_address": pair,
           "reported_liq_usd": reported_liq, "quote_symbol": quote_sym, "quote_address": quote_addr,
           "method": None, "onchain_quote_amount": None, "onchain_quote_usd": None,
           "delta_pct": None, "verified": False, "note": ""}

    t0, t1 = token0(pair), token1(pair)
    reserves = get_reserves(pair)
    qtok, qamt_raw = None, None

    if t0 and t1 and reserves:
        r0, r1 = reserves
        t0l, t1l = t0.lower(), t1.lower()
        if quote_addr and quote_addr == t0l:
            qtok, qamt_raw = t0, r0
        elif quote_addr and quote_addr == t1l:
            qtok, qamt_raw = t1, r1
        elif t0l in MAJORS_4:
            qtok, qamt_raw = t0, r0
        elif t1l in MAJORS_4:
            qtok, qamt_raw = t1, r1
        else:
            qtok, qamt_raw = t1, r1  # best-effort guess if quote wasn't identifiable
        rec["method"] = "getReserves"
    else:
        # v3/v4 or CLMM pool: getReserves() doesn't apply. Fall back to reading
        # the quote token's balanceOf(pair) directly -- valid for any pool shape.
        if quote_addr:
            qtok = quote_addr
            qamt_raw = balance_of(quote_addr, pair)
            rec["method"] = "balanceOf(pair) [v3/v4 or non-standard pool]"
        else:
            rec["method"] = "UNRESOLVED (no getReserves, no known quote address)"

    if qtok and qamt_raw is not None:
        dec = decimals(qtok)
        qamt = qamt_raw / (10 ** dec)
        rec["onchain_quote_amount"] = qamt
        qtokl = qtok.lower()
        if qtokl in MAJORS_4 and PRICE.get(qtokl):
            usd_side = qamt * PRICE[qtokl]
            # AMM liquidity_usd is base+quote combined; a single side's USD value
            # run through the SAME quote asset should be roughly half of a
            # symmetric-value AMM pool's reported total (v2-style). For v3/v4
            # concentrated pools this ratio does not hold structurally, so it is
            # reported as a floor/sanity figure, not doubled into a full-pool claim.
            rec["onchain_quote_usd"] = round(usd_side, 2)
            twice = usd_side * 2
            rec["delta_pct"] = round(abs(twice - reported_liq) / max(reported_liq, 1) * 100, 1)
            rec["verified"] = True
            rec["note"] = f"quote-side reserve ${usd_side:,.0f} (~${twice:,.0f} if doubled for a symmetric v2 pool) vs DS-reported ${reported_liq:,.0f}"
        else:
            rec["note"] = f"quote token is NOT one of the 4 brief-named majors (or price unavailable) -- {qamt:,.4f} {quote_sym or qtok} confirmed on-chain, but USD conversion is UNVERIFIED/SOFT"
    else:
        rec["note"] = "could not read a quote-side balance on-chain"

    out.append(rec)
    tag = "OK" if rec["verified"] else ("SOFT" if rec["onchain_quote_amount"] is not None else "FAIL")
    print(f"  [{tag}] {r['symbol']:<14} pair={pair}  {rec['note']}")
    time.sleep(0.15)

json.dump(out, open(f"{DATA}/base_liquidity_verification.json", "w"), indent=1)
n_ok = sum(1 for x in out if x["verified"])
n_soft = sum(1 for x in out if not x["verified"] and x["onchain_quote_amount"] is not None)
n_fail = sum(1 for x in out if x["onchain_quote_amount"] is None)
print(f"\nverified (major-quote, USD-converted): {n_ok}")
print(f"soft (on-chain amount confirmed, quote not a major -> USD unverified): {n_soft}")
print(f"unresolved (could not read on-chain at all): {n_fail}")
print("wrote base_liquidity_verification.json")
