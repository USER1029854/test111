"""Multichain discovery (ETH / Arbitrum / Base). Same posture as the BSC discover.py:

GeckoTerminal is used ONLY as an address index (the one free source with a chain-wide
pool enumeration). Every reported metric comes from DEXScreener in phase 2. Nothing here
is invented -- each record is a raw GeckoTerminal response field.

Usage: python3 discover_multi.py <eth|arbitrum|base>
"""
import requests, json, time, sys

CHAIN = sys.argv[1]
H = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
GT = "https://api.geckoterminal.com/api/v2"
DATA = "/home/user/test111/data"
OUT = f"{DATA}/gt_pools_{CHAIN}.json"
LOG = f"{DATA}/discover_{CHAIN}.log"

# GeckoTerminal network slug + major quote tokens per chain. Quote-token pool sweeps
# target exactly the liquid pairs a real project launches against.
CFG = {
    "eth": {"net": "eth", "quotes": {
        "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "DAI":  "0x6B175474E89094C44Da98b954EedeAC495271d0F",
        "WBTC": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
        "WSTETH": "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0",
    }, "priority": ["uniswap_v2", "uniswap_v3", "uniswap-v4-ethereum", "sushiswap",
        "pancakeswap-v3-eth", "pancakeswap_ethereum", "curve", "balancer_ethereum",
        "fluid-dex", "maverick-v2-ethereum", "shibaswap", "fraxswap"]},
    "arbitrum": {"net": "arbitrum", "quotes": {
        "WETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        "USDC": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
        "USDCe": "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8",
        "USDT": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
        "ARB":  "0x912CE59144191C1204E64559FE8253a0e49E6548",
        "WBTC": "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f",
    }, "priority": ["uniswap_v3_arbitrum", "uniswap-v2-arbitrum", "uniswap-v4-arbitrum",
        "camelot", "camelot-v3", "sushiswap-arbitrum", "pancakeswap-v3-arbitrum",
        "ramses-cl", "trader-joe-v2-1-arbitrum", "curve-arbitrum", "balancer-v2-arbitrum",
        "fluid-dex-arbitrum"]},
    "base": {"net": "base", "quotes": {
        "WETH": "0x4200000000000000000000000000000000000006",
        "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "USDbC": "0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA",
        "cbBTC": "0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf",
        "DAI":  "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb",
    }, "priority": ["uniswap_v2_base", "uniswap-v3-base", "uniswap-v4-base",
        "aerodrome-base", "aerodrome-slipstream", "pancakeswap-v3-base",
        "sushiswap-v3-base", "baseswap", "alienbase", "swapbased", "maverick-v2-base",
        "clanker"]},
}[CHAIN]
NET = CFG["net"]
PREFIX = NET + "_"

pools, errors, calls = {}, [], [0]
# GeckoTerminal free tier is ~30 req/min per IP. Pace to ~27/min (2.2s min gap) so we
# never trip the cooldown; on 429 honor Retry-After. The earlier 1.0s pacing = 60/min
# doubled the limit and put the process into 90s backoff loops.
_last = [0.0]
MIN_GAP = 2.2

def log(m):
    print(m, flush=True)
    open(LOG, "a").write(m + "\n")

def get(url, tries=5):
    for t in range(tries):
        gap = MIN_GAP - (time.time() - _last[0])
        if gap > 0:
            time.sleep(gap)
        try:
            calls[0] += 1
            r = requests.get(url, timeout=35, headers=H)
            _last[0] = time.time()
            if r.status_code == 200:
                return r.json()
            if r.status_code == 429:
                ra = r.headers.get("Retry-After")
                time.sleep(float(ra) if ra and ra.isdigit() else 8 * (t + 1))
                continue
            if r.status_code in (400, 404):
                return {"__err": r.status_code}
            time.sleep(2 * (t + 1))
        except Exception as e:
            _last[0] = time.time()
            errors.append(f"{url[:70]} :: {type(e).__name__}")
            time.sleep(2 * (t + 1))
    return None

def absorb(data, src):
    if not isinstance(data, dict) or "data" not in data:
        return
    for x in data.get("data") or []:
        try:
            a = x["attributes"]; rel = x.get("relationships") or {}
            addr = a.get("address")
            if not addr:
                continue
            k = addr.lower()
            if k not in pools:
                bt = (rel.get("base_token", {}).get("data") or {}).get("id", "")
                qt = (rel.get("quote_token", {}).get("data") or {}).get("id", "")
                dex = (rel.get("dex", {}).get("data") or {}).get("id", "")
                pools[k] = {"pool_address": addr, "gt_name": a.get("name"),
                    "gt_created": a.get("pool_created_at"),
                    "gt_reserve_usd": a.get("reserve_in_usd"), "gt_fdv": a.get("fdv_usd"),
                    "base_token": bt.replace(PREFIX, ""), "quote_token": qt.replace(PREFIX, ""),
                    "dex": dex, "srcs": []}
            if src not in pools[k]["srcs"]:
                pools[k]["srcs"].append(src)
        except Exception as e:
            errors.append(f"absorb {src}: {type(e).__name__}")

def sweep(path, label, pages, sorts):
    for s in sorts:
        for pg in range(1, pages + 1):
            sep = "&" if "?" in path else "?"
            d = get(f"{GT}{path}{sep}page={pg}&sort={s}")
            if d is None or d.get("__err"):
                break
            n0 = len(pools)
            absorb(d, label)
            if len(d.get("data") or []) == 0:
                break

t0 = time.time()
log(f"=== discovery start [{CHAIN}] ===")

# 1. chain-wide feeds
for path, label, pages, sorts in [
    (f"/networks/{NET}/new_pools", "new_pools", 8, ("h24_volume_usd_desc",)),
    (f"/networks/{NET}/trending_pools", "trending", 8, ("h24_volume_usd_desc",)),
    (f"/networks/{NET}/pools", "top_pools", 8, ("h24_volume_usd_desc", "h24_tx_count_desc")),
]:
    sweep(path, label, pages, sorts)
log(f"after chain-wide feeds: {len(pools)} pools ({calls[0]} calls)")

# 2. major quote-token pools -- the top 3 quotes are where a real new project lists;
# both sorts on the top 2, volume on the 3rd. (Rate-limit budget: quotes 4-6 like WBTC/DAI
# rarely host a new sub-60d launch and are covered by the chain-wide top_pools feed.)
for i, (sym, addr) in enumerate(list(CFG["quotes"].items())[:3]):
    srt = ("h24_volume_usd_desc", "h24_tx_count_desc") if i < 2 else ("h24_volume_usd_desc",)
    sweep(f"/networks/{NET}/tokens/{addr}/pools", f"quote_{sym}", 6, srt)
log(f"after quote sweeps: {len(pools)} pools ({calls[0]} calls)")

# 3. priority DEX sweeps (top venues, volume sort, 5 pages). The shallow-all-dexes pass
# from the BSC run is dropped here to stay within GeckoTerminal's ~30/min budget; this is
# a deliberate, documented coverage reduction on the long tail of minor DEXes.
for dex in CFG["priority"][:8]:
    sweep(f"/networks/{NET}/dexes/{dex}/pools", f"dex_{dex}", 5, ("h24_volume_usd_desc",))
log(f"after priority dex sweeps: {len(pools)} pools ({calls[0]} calls)")

log(f"=== done [{CHAIN}]: {len(pools)} pools, {calls[0]} calls, {len(errors)} errors, {time.time()-t0:.0f}s ===")
json.dump({"chain": CHAIN, "pools": list(pools.values()), "errors": errors[:200], "calls": calls[0]},
          open(OUT, "w"), indent=1)
log("wrote " + OUT)
