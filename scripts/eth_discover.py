"""Phase 1: discover candidate Ethereum mainnet pools/tokens.

GeckoTerminal is used ONLY as an address index (it is the one free source that
exposes a chain-wide pool enumeration). All reported metrics come from DEXScreener
in phase 2. Nothing here is invented: every record is a raw API response.
"""
import requests, json, time, sys, os

H = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
GT = "https://api.geckoterminal.com/api/v2"
OUT = "/home/user/test111/data/eth_gt_pools.json"
LOG = "/home/user/test111/data/eth_discover_log.txt"

pools = {}
errors = []
calls = 0

def log(m):
    print(m, flush=True)
    with open(LOG, "a") as f:
        f.write(m + "\n")

def get(url, tries=5):
    """GET with adaptive backoff. Returns parsed json or None."""
    global calls
    delay = 0.9
    for t in range(tries):
        try:
            calls += 1
            r = requests.get(url, timeout=35, headers=H)
            if r.status_code == 200:
                time.sleep(delay)
                return r.json()
            if r.status_code == 429:
                time.sleep(8 * (t + 1))
                continue
            if r.status_code in (400, 404):
                return {"__err": r.status_code}
            time.sleep(2 * (t + 1))
        except Exception as e:
            errors.append(f"{url} :: {type(e).__name__}")
            time.sleep(2 * (t + 1))
    return None

def absorb(data, src):
    """Pull pool records out of a GeckoTerminal response."""
    n = 0
    if not isinstance(data, dict) or "data" not in data:
        return 0
    for x in data.get("data") or []:
        try:
            a = x["attributes"]; rel = x.get("relationships") or {}
            addr = a.get("address")
            if not addr:
                continue
            bt = (rel.get("base_token", {}).get("data") or {}).get("id", "")
            qt = (rel.get("quote_token", {}).get("data") or {}).get("id", "")
            dex = (rel.get("dex", {}).get("data") or {}).get("id", "")
            key = addr.lower()
            if key not in pools:
                pools[key] = {
                    "pool_address": addr,
                    "gt_name": a.get("name"),
                    "gt_created": a.get("pool_created_at"),
                    "gt_reserve_usd": a.get("reserve_in_usd"),
                    "gt_fdv": a.get("fdv_usd"),
                    "base_token": bt.replace("eth_", ""),
                    "quote_token": qt.replace("eth_", ""),
                    "dex": dex,
                    "srcs": [],
                }
                n += 1
            if src not in pools[key]["srcs"]:
                pools[key]["srcs"].append(src)
        except Exception as e:
            errors.append(f"absorb {src}: {type(e).__name__}")
    return n

def sweep(path, label, pages=10, sorts=("h24_volume_usd_desc",)):
    for s in sorts:
        empty_streak = 0
        for pg in range(1, pages + 1):
            sep = "&" if "?" in path else "?"
            d = get(f"{GT}{path}{sep}page={pg}&sort={s}")
            if d is None:
                errors.append(f"{label} p{pg} {s}: no response")
                break
            if d.get("__err"):
                break
            got = len(d.get("data") or [])
            absorb(d, label)
            if got == 0:
                empty_streak += 1
                if empty_streak >= 1:
                    break

t0 = time.time()
log("=== eth discovery start ===")

# 1. chain-wide feeds
for path, label, pages, sorts in [
    ("/networks/eth/new_pools", "new_pools", 10, ("h24_volume_usd_desc",)),
    ("/networks/eth/trending_pools", "trending", 10, ("h24_volume_usd_desc",)),
    ("/networks/eth/pools", "eth_pools", 10, ("h24_volume_usd_desc", "h24_tx_count_desc")),
]:
    sweep(path, label, pages, sorts)
log(f"after chain-wide feeds: {len(pools)} pools ({calls} calls)")

# 2. pools of the major quote assets -- targets exactly the liquid pairs
QUOTES = {
    "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    "DAI":  "0x6B175474E89094C44Da98b954EedeAC495271d0F",
    "WBTC": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
}
for sym, addr in QUOTES.items():
    sweep(f"/networks/eth/tokens/{addr}/pools", f"quote_{sym}", 10,
          ("h24_volume_usd_desc", "h24_tx_count_desc"))
log(f"after quote-token sweeps: {len(pools)} pools ({calls} calls)")

# 3. per-DEX sweeps. Priority venues (by known Ethereum-mainnet volume) get full depth + both sorts.
PRIORITY = [
    "uniswap_v2", "uniswap_v3", "uniswap-v4-ethereum",
    "sushiswap", "sushiswap-v3-ethereum",
    "curve", "balancer_ethereum", "balancer-v3-ethereum",
    "pancakeswap_ethereum", "pancakeswap-v3-ethereum", "pancakeswap-stableswap-ethereum",
    "kyberswap_elastic", "kyberswap_classic_ethereum",
    "fluid-ethereum", "maverick-v2-eth", "solidly-v3",
    "dodo-pmm-ethereum", "ekubo-v3-ethereum", "ekubo-v2-ethereum",
    "traderjoe-v2-1-ethereum", "smardex-ethereum", "fraxswap_ethereum",
    "carbon-defi-ethereum", "x7-finance-ethereum",
]
for dex in PRIORITY:
    sweep(f"/networks/eth/dexes/{dex}/pools", f"dex_{dex}", 10,
          ("h24_volume_usd_desc", "h24_tx_count_desc"))
log(f"after priority dex sweeps: {len(pools)} pools ({calls} calls)")

# 4. shallow pass over every remaining DEX so nothing is structurally excluded
alldex = []
for pg in (1, 2, 3):
    d = get(f"{GT}/networks/eth/dexes?page={pg}")
    if isinstance(d, dict) and d.get("data"):
        alldex += [x["id"] for x in d["data"]]
    else:
        break
rest = [d for d in alldex if d not in PRIORITY]
log(f"shallow pass over {len(rest)} remaining dexes")
for dex in rest:
    sweep(f"/networks/eth/dexes/{dex}/pools", f"dex_{dex}", 3, ("h24_volume_usd_desc",))

log(f"=== done: {len(pools)} unique pools, {calls} calls, {len(errors)} errors, {time.time()-t0:.0f}s ===")
json.dump({"pools": list(pools.values()), "errors": errors[:200], "calls": calls},
          open(OUT, "w"), indent=1)
log("wrote " + OUT)
