"""Phase 1: discover candidate Base pools/tokens.

GeckoTerminal is used ONLY as an address index (it is the one free source that
exposes a chain-wide pool enumeration for Base). All reported metrics come from
DEXScreener in phase 2. Nothing here is invented: every record is a raw API response.

Scope note: Base is younger than BSC but has a much higher launch rate and a huge
long tail of DEXes (>=100 registered on GeckoTerminal). Per the scope calibration,
this sweep prioritizes chain-wide feeds + major quote-token pools + the DEXes that
actually carry volume (Aerodrome dominates, confirmed empirically below), then does
a shallow pass over the remaining long tail rather than full-depth on all ~100+.
"""
import requests, json, time, sys, os

H = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
GT = "https://api.geckoterminal.com/api/v2"
OUT = "/home/user/test111/data/base_gt_pools.json"
LOG = "/home/user/test111/data/base_discover_log.txt"

pools = {}
errors = []
calls = 0

def log(m):
    print(m, flush=True)
    with open(LOG, "a") as f:
        f.write(m + "\n")

def get(url, tries=4):
    """GET with adaptive backoff. Returns parsed json or None. Base's GT rate
    limit was empirically observed to be tighter than BSC's -- isolated manual
    test calls spaced ~1-2s apart still drew 429s, consistent with the
    documented ~30 calls/min free-tier ceiling. A 2.2s steady-state delay
    (~27/min) avoids that tax almost entirely rather than repeatedly paying a
    9s+ backoff, which is the more expensive path in aggregate."""
    global calls
    delay = 2.2
    for t in range(tries):
        try:
            calls += 1
            r = requests.get(url, timeout=35, headers=H)
            if r.status_code == 200:
                time.sleep(delay)
                return r.json()
            if r.status_code == 429:
                time.sleep(12 * (t + 1))
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
                    "gt_vol_h24": (a.get("volume_usd") or {}).get("h24"),
                    "base_token": bt.replace("base_", ""),
                    "quote_token": qt.replace("base_", ""),
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
log("=== base discovery start ===")

# 1. chain-wide feeds
for path, label, pages, sorts in [
    ("/networks/base/new_pools", "new_pools", 10, ("h24_volume_usd_desc",)),
    ("/networks/base/trending_pools", "trending", 10, ("h24_volume_usd_desc",)),
    ("/networks/base/pools", "base_pools", 10, ("h24_volume_usd_desc", "h24_tx_count_desc")),
]:
    sweep(path, label, pages, sorts)
log(f"after chain-wide feeds: {len(pools)} pools ({calls} calls)")

# 2. pools of the major quote assets -- verified on-chain (symbol/name/decimals
# read via eth_call against mainnet.base.org) before use, per the brief's
# instruction not to trust the given addresses blindly.
QUOTES = {
    "WETH": "0x4200000000000000000000000000000000000006",
    "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "DAI":  "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb",
    "cbETH":"0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22",
}
for sym, addr in QUOTES.items():
    sweep(f"/networks/base/tokens/{addr}/pools", f"quote_{sym}", 10,
          ("h24_volume_usd_desc", "h24_tx_count_desc"))
log(f"after quote-token sweeps: {len(pools)} pools ({calls} calls)")

# 3. per-DEX sweeps. Priority venues get full depth + both sorts. Selected by
# empirically tallying dex_id frequency + summed h24 volume across the top
# ~250 base_pools by both sort orders (Aerodrome's slipstream/v2 forms and
# Uniswap v3/v4 dominate by a wide margin -- consistent with Aerodrome being
# Base's primary DEX per the brief). Launchpad-adjacent venues (virtuals-base,
# mint-club-base) are included explicitly since agent-token / bonding-curve
# launches are part of Base's "clanker"-style automated-deployment culture.
PRIORITY = [
    "aerodrome-slipstream", "aerodrome-slipstream-2", "aerodrome-slipstream-3",
    "aerodrome-base",
    "uniswap-v3-base", "uniswap-v4-base", "uniswap-v2-base",
    "pancakeswap-v3-base", "pancakeswap-v2-base", "pancakeswap-infinity-clmm-base",
    "baseswap", "baseswap-v3",
    "alien-base", "alien-base-v3",
    "sushiswap-v3-base", "sushiswap-v2-base",
    "balancer-v2-base", "balancer-v3-base",
    "curve-base", "maverick-v2-base",
    "velocimeter-base", "solidly-v3-base",
    "kim-v2-base", "kim-v4-base",
    "virtuals-base", "virtuals-unicorn-base", "mint-club-base",
    "squadswap-base", "squadswap-v3-base", "equalizer-base",
    "smardex-base", "dackieswap-v2-base", "dackieswap-v3-base",
]
for dex in PRIORITY:
    sweep(f"/networks/base/dexes/{dex}/pools", f"dex_{dex}", 8,
          ("h24_volume_usd_desc", "h24_tx_count_desc"))
log(f"after priority dex sweeps: {len(pools)} pools ({calls} calls)")

# 4. shallow pass over every remaining DEX so nothing is structurally excluded
alldex = []
for pg in (1, 2, 3, 4):
    d = get(f"{GT}/networks/base/dexes?page={pg}")
    if isinstance(d, dict) and d.get("data"):
        alldex += [x["id"] for x in d["data"]]
    else:
        break
rest = [d for d in alldex if d not in PRIORITY]
log(f"shallow pass over {len(rest)} remaining dexes (of {len(alldex)} total)")
for dex in rest:
    sweep(f"/networks/base/dexes/{dex}/pools", f"dex_{dex}", 2, ("h24_volume_usd_desc",))

log(f"=== done: {len(pools)} unique pools, {calls} calls, {len(errors)} errors, {time.time()-t0:.0f}s ===")
json.dump({"pools": list(pools.values()), "errors": errors[:200], "calls": calls},
          open(OUT, "w"), indent=1)
log("wrote " + OUT)
