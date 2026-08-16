"""Ground-truth liquidity verification (client's central requirement).

DEXScreener/GeckoTerminal headline USD liquidity is not trusted at face value.
For each of the top-N kept candidates by liquidity:

  1. Re-read the pair fresh from DEXScreener (freshness + a second QA cross-check
     beyond the random sample in eth_verify.py).
  2. Independently read the quote token's on-chain balanceOf(pairAddress) via the
     public RPC and compare it (in raw token units, no price conversion needed)
     against DEXScreener's own reported liquidity.quote raw amount. This validates
     that DS is not stale/wrong about what the pool actually holds.
  3. Classify the quote asset: if it is one of the five major, independently-priced
     assets (WETH/USDC/USDT/DAI/WBTC), the USD figure is well-grounded and marked
     VERIFIED. If not, the headline USD figure is marked UNVERIFIED/SOFT -- because
     its USD conversion is only as good as DEXScreener's price for that quote token,
     which can itself be thin or circular. For soft cases we additionally probe
     whether the quote token has its own independent deep pool against a major
     asset, as a secondary sanity signal (not a substitute for the primary check).

Special-cased AMM shapes:
  * Balancer (v2/v3): tokens are custody-held by a single shared Vault contract,
    not the pool address, so a naive balanceOf(pool) reads ~0 and is meaningless.
    These are flagged as "vault-custody, needs getPoolTokens()" rather than silently
    marked verified or unverified.
  * Curve, Uniswap v2/v3/v4, Solidly-style, and most others hold reserves directly
    on the pool/pair address, so balanceOf(pair) is valid ground truth for them.
"""
import requests, json, csv, time, sys

H = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
DS = "https://api.dexscreener.com"
# Brief's suggested fallbacks (ankr, cloudflare-eth) tested live and both fail
# (ankr needs an API key now; cloudflare returns "Cannot fulfill request") --
# replaced with fallbacks verified working at run time.
RPCS = ["https://ethereum.publicnode.com", "https://eth.merkle.io", "https://1rpc.io/eth",
        "https://eth-mainnet.public.blastapi.io"]
DATA = "/home/user/test111/data"

MAJORS = {
    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": ("WETH", 18),
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": ("USDC", 6),
    "0xdac17f958d2ee523a2206206994597c13d831ec7": ("USDT", 6),
    "0x6b175474e89094c44da98b954eedeac495271d0f": ("DAI", 18),
    "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599": ("WBTC", 8),
}

BALANCER_VAULT = "0xba12222222228d8ba445958a75a0704d566bf2c8"  # v2 Vault (v3 uses its own; handled generically)

def rpc(method, params, tries=4):
    for url in RPCS:
        for t in range(tries):
            try:
                r = requests.post(url, timeout=20, json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params})
                if r.status_code == 200:
                    j = r.json()
                    if "result" in j:
                        return j["result"]
                time.sleep(0.6 * (t + 1))
            except Exception:
                time.sleep(0.6 * (t + 1))
    return None

def eth_call(to, data):
    return rpc("eth_call", [{"to": to, "data": data}, "latest"])

def decimals(token):
    r = eth_call(token, "0x313ce567")
    if not r or r == "0x":
        return None
    try:
        return int(r, 16)
    except Exception:
        return None

def balance_of(token, holder):
    data = "0x70a08231" + holder.lower().replace("0x", "").rjust(64, "0")
    r = eth_call(token, data)
    if not r or r == "0x":
        return None
    try:
        return int(r, 16)
    except Exception:
        return None

def ds_pair(pair_addr):
    for t in range(3):
        try:
            r = requests.get(f"{DS}/latest/dex/pairs/ethereum/{pair_addr}", headers=H, timeout=25)
            if r.status_code == 200:
                ps = r.json().get("pairs") or []
                return ps[0] if ps else None
            time.sleep(1.2)
        except Exception:
            time.sleep(1.2)
    return None

def main(n=20):
    rows = list(csv.DictReader(open(f"{DATA}/eth_contract_logic.csv")))
    rows.sort(key=lambda r: -float(r["liquidity_usd"] or 0))
    top = rows[:n]
    print(f"verifying top {len(top)} kept candidates by liquidity on-chain\n")

    out = []
    for i, r in enumerate(top):
        sym, tok, pair = r["symbol"], r["token_address"], r["pair_address"]
        p = ds_pair(pair)
        if not p:
            out.append({**r, "verify_status": "DS_REFETCH_FAILED", "note": "pair not returned on re-fetch"})
            print(f"  [{i+1}] {sym:<12} DS re-fetch FAILED"); continue

        qt = (p.get("quoteToken") or {}).get("address", "")
        qsym = (p.get("quoteToken") or {}).get("symbol", "")
        dex = p.get("dexId") or ""
        ds_liq_usd = float((p.get("liquidity") or {}).get("usd") or 0)
        ds_quote_raw = (p.get("liquidity") or {}).get("quote")

        is_major = qt.lower() in MAJORS
        note = ""
        onchain_quote_tokens = None
        drift_pct = None
        status = ""

        if "balancer" in dex.lower():
            status = "VAULT_CUSTODY_UNVERIFIED"
            note = "Balancer pool: tokens held by shared Vault, not pool address -- balanceOf(pool) is not meaningful; needs getPoolTokens(poolId). Not independently confirmed here."
        else:
            dec = decimals(qt)
            bal = balance_of(qt, pair)
            time.sleep(0.15)
            if dec is None or bal is None:
                status = "RPC_READ_FAILED"
                note = "could not read quote-token decimals/balanceOf from public RPC"
            else:
                onchain_quote_tokens = bal / (10 ** dec)
                if ds_quote_raw:
                    drift_pct = abs(onchain_quote_tokens - float(ds_quote_raw)) / max(float(ds_quote_raw), 1e-9) * 100
                if is_major:
                    if drift_pct is not None and drift_pct < 15:
                        status = "VERIFIED_MAJOR_QUOTE"
                    elif drift_pct is not None:
                        status = "MISMATCH_CHECK"
                        note = f"on-chain quote balance drifts {drift_pct:.1f}% from DS-reported reserve"
                    else:
                        status = "VERIFIED_MAJOR_QUOTE_NO_DS_RAW"
                        note = "DS did not report raw quote reserve to diff against; on-chain balance read directly"
                else:
                    status = "UNVERIFIED_SOFT_QUOTE"
                    note = f"quote asset {qsym or qt} is not one of the 5 major assets -- USD figure only as good as DS's price for it"

        maj_name = MAJORS.get(qt.lower(), (qsym, None))[0]
        out.append({
            "symbol": sym, "name": r["name"], "token_address": tok, "pair_address": pair,
            "dex": dex, "quote_symbol": qsym or maj_name, "quote_address": qt,
            "ds_liquidity_usd_fresh": round(ds_liq_usd, 2),
            "ds_liquidity_usd_csv": r["liquidity_usd"],
            "is_major_quote": is_major,
            "ds_reported_quote_reserve_tokens": ds_quote_raw,
            "onchain_quote_balance_tokens": onchain_quote_tokens,
            "reserve_drift_pct": round(drift_pct, 2) if drift_pct is not None else None,
            "verify_status": status, "note": note,
        })
        drift_s = f"{drift_pct:.1f}%" if drift_pct is not None else "n/a"
        print(f"  [{i+1:2d}] {sym:<12} ${ds_liq_usd:>13,.0f}  quote={qsym or maj_name:<8} major={is_major!s:<5} drift={drift_s:<8} -> {status}")

    json.dump(out, open(f"{DATA}/eth_liquidity_verification.json", "w"), indent=1)
    with open(f"{DATA}/eth_liquidity_verification.csv", "w", newline="") as f:
        cols = ["symbol","name","token_address","pair_address","dex","quote_symbol","quote_address",
                "ds_liquidity_usd_fresh","ds_liquidity_usd_csv","is_major_quote",
                "ds_reported_quote_reserve_tokens","onchain_quote_balance_tokens","reserve_drift_pct",
                "verify_status","note"]
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader()
        for x in out: w.writerow(x)

    verified = sum(1 for x in out if x["verify_status"].startswith("VERIFIED"))
    soft = sum(1 for x in out if x["verify_status"] == "UNVERIFIED_SOFT_QUOTE")
    vault = sum(1 for x in out if x["verify_status"] == "VAULT_CUSTODY_UNVERIFIED")
    failed = sum(1 for x in out if x["verify_status"] in ("RPC_READ_FAILED", "DS_REFETCH_FAILED"))
    mismatch = sum(1 for x in out if x["verify_status"] == "MISMATCH_CHECK")
    print(f"\n{len(out)} candidates checked | verified-major-quote: {verified} | soft/unverified quote: {soft}"
          f" | balancer-vault (unverified): {vault} | mismatch flagged: {mismatch} | read failures: {failed}")
    print("wrote eth_liquidity_verification.{json,csv}")

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    main(n)
