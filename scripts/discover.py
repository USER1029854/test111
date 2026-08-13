"""Phase 1: discover candidate BSC pools/tokens.

GeckoTerminal is used ONLY as an address index (it is the one free source that
exposes a BSC-wide pool enumeration). All reported metrics come from DEXScreener
in phase 2. Nothing here is invented: every record is a raw API response.
"""
import requests, json, time, sys, os

H = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
GT = "https://api.geckoterminal.com/api/v2"
OUT = "/home/user/test111/data/gt_pools.json"
LOG = "/home/user/test111/data/discover_log.txt"

pools = {}
errors = []
calls = 0

def log(m):
    print(m, flush=True)
    with open(LOG, "a") as f:
        f.write(m + "\n")

def get(url, tries=4):
    """GET with adaptive backoff. Returns parsed json or None."""
    global calls
    delay = 0.8
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
                    "base_token": bt.replace("bsc_", ""),
                    "quote_token": qt.replace("bsc_", ""),
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
log("=== discovery start ===")

# 1. chain-wide feeds
for path, label, pages, sorts in [
    ("/networks/bsc/new_pools", "new_pools", 10, ("h24_volume_usd_desc",)),
    ("/networks/bsc/trending_pools", "trending", 10, ("h24_volume_usd_desc",)),
    ("/networks/bsc/pools", "bsc_pools", 10, ("h24_volume_usd_desc", "h24_tx_count_desc")),
]:
    sweep(path, label, pages, sorts)
log(f"after chain-wide feeds: {len(pools)} pools ({calls} calls)")

# 2. pools of the major quote assets -- targets exactly the liquid pairs
QUOTES = {
    "WBNB": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",
    "USDT": "0x55d398326f99059fF775485246999027B3197955",
    "USDC": "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",
    "BTCB": "0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c",
    "ETH":  "0x2170Ed0880ac9A755fd29B2688956BD959F933F8",
    "CAKE": "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82",
    "FDUSD": "0xc5f0f7b66764F6ec8C8Dff7BA683102295E16409",
    "BUSD": "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56",
}
for sym, addr in QUOTES.items():
    sweep(f"/networks/bsc/tokens/{addr}/pools", f"quote_{sym}", 10,
          ("h24_volume_usd_desc", "h24_tx_count_desc"))
log(f"after quote-token sweeps: {len(pools)} pools ({calls} calls)")

# 3. per-DEX sweeps. Priority venues get full depth + both sorts.
PRIORITY = [
    "pancakeswap_v2", "pancakeswap-v3-bsc", "pancakeswap-infinity-clmm",
    "pancakeswap-infinity-lbamm-bsc", "pancakeswap_stableswap",
    "uniswap-bsc", "uniswap-v2-bsc", "uniswap-v4-bsc",
    "thena", "thena-fusion", "thena-v3", "biswap", "biswap-v3",
    "four-meme", "tiktokfun", "squadswap-v2-bsc", "squadswap-v3-bsc",
    "maverick-v2-bsc", "unchain-x", "dnax", "coinfair-bsc",
    "omni-exchange-v2-bsc", "omni-exchange-v3-bsc", "omni-exchange-v4-bsc",
    "curve-bsc", "smardex-bsc", "sushiswap-v3-bsc", "iziswap-bsc",
    "ring-exchange-bsc", "hello-dex-bsc", "topaz", "forest-protocol",
    "falcox-swap-bnb", "coinhain", "token-dex", "tidaldex", "lovely-swap",
]
for dex in PRIORITY:
    sweep(f"/networks/bsc/dexes/{dex}/pools", f"dex_{dex}", 10,
          ("h24_volume_usd_desc", "h24_tx_count_desc"))
log(f"after priority dex sweeps: {len(pools)} pools ({calls} calls)")

# 4. shallow pass over every remaining DEX so nothing is structurally excluded
alldex = []
for pg in (1, 2, 3):
    d = get(f"{GT}/networks/bsc/dexes?page={pg}")
    if isinstance(d, dict) and d.get("data"):
        alldex += [x["id"] for x in d["data"]]
    else:
        break
rest = [d for d in alldex if d not in PRIORITY]
log(f"shallow pass over {len(rest)} remaining dexes")
for dex in rest:
    sweep(f"/networks/bsc/dexes/{dex}/pools", f"dex_{dex}", 3, ("h24_volume_usd_desc",))

log(f"=== done: {len(pools)} unique pools, {calls} calls, {len(errors)} errors, {time.time()-t0:.0f}s ===")
json.dump({"pools": list(pools.values()), "errors": errors[:200], "calls": calls},
          open(OUT, "w"), indent=1)
log("wrote " + OUT)
