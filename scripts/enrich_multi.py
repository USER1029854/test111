"""Phase 2 multichain: enrich GeckoTerminal candidates with DEXScreener (source of record).

Every downstream metric (name, symbol, liquidity, age, dex, socials) comes from a
DEXScreener response captured here. GeckoTerminal numbers are used only to shortlist.

Usage: python3 enrich_multi.py <eth|arbitrum|base>
"""
import requests, json, time, sys, os

CHAIN = sys.argv[1]
H = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
DS = "https://api.dexscreener.com"
NOW = time.time()
DATA = "/home/user/test111/data"

# DEXScreener chainId slug + major quote tokens to exclude as "projects"
DSCHAIN = {"eth": "ethereum", "arbitrum": "arbitrum", "base": "base"}[CHAIN]
MAJORS = {a.lower() for a in {
    "eth": ["0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2","0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "0xdAC17F958D2ee523a2206206994597C13D831ec7","0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599","0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0",
            "0x0000000000000000000000000000000000000000"],
    "arbitrum": ["0x82aF49447D8a07e3bd95BD0d56f35241523fBab1","0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
            "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8","0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
            "0x912CE59144191C1204E64559FE8253a0e49E6548","0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f",
            "0x0000000000000000000000000000000000000000"],
    "base": ["0x4200000000000000000000000000000000000006","0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
            "0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA","0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf",
            "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb",
            "0x0000000000000000000000000000000000000000"],
}[CHAIN]}

SHORT_LIQ, SHORT_AGE = 40_000.0, 75.0
FINAL_LIQ, FINAL_AGE = 100_000.0, 60.0
stats = {"ds_calls": 0, "ds_fail": 0}
errors = []

def get(url, tries=4):
    for t in range(tries):
        try:
            stats["ds_calls"] += 1
            r = requests.get(url, timeout=35, headers=H)
            if r.status_code == 200:
                time.sleep(0.32); return r.json()
            if r.status_code == 429:
                time.sleep(5 * (t + 1)); continue
            if r.status_code in (400, 404):
                return None
            time.sleep(1.5 * (t + 1))
        except Exception as e:
            errors.append(f"{url[:70]} :: {type(e).__name__}")
            time.sleep(1.5 * (t + 1))
    stats["ds_fail"] += 1
    return None

def age_days(p):
    ts = p.get("pairCreatedAt")
    return None if not ts else (NOW - ts / 1000.0) / 86400.0

def liq(p):
    return float(((p.get("liquidity") or {}).get("usd")) or 0)

pools = json.load(open(f"{DATA}/gt_pools_{CHAIN}.json"))["pools"]
print(f"[{CHAIN}] discovery universe: {len(pools)} pools")

def gt_age(p):
    c = p.get("gt_created")
    if not c: return None
    try: return (NOW - time.mktime(time.strptime(c, "%Y-%m-%dT%H:%M:%SZ"))) / 86400.0
    except Exception: return None

def reserve(p):
    try: return float(p.get("gt_reserve_usd") or 0)
    except Exception: return 0.0

def recent(p):
    a = gt_age(p)
    return a is None or a <= SHORT_AGE

# Batch net: any pool that could plausibly be recent OR liquid gets a real DS reading.
batch_set = [p for p in pools if recent(p) or reserve(p) >= SHORT_LIQ]
short = [p for p in pools if reserve(p) >= SHORT_LIQ and recent(p)]
pair_addrs = [p["pool_address"] for p in batch_set
              if p["pool_address"].startswith("0x") and len(p["pool_address"]) == 42]
odd_pools = [p for p in batch_set
             if not (p["pool_address"].startswith("0x") and len(p["pool_address"]) == 42)]
print(f"  batch net: {len(batch_set)} | standard pool addrs: {len(pair_addrs)} | odd ids: {len(odd_pools)}")

ds_pairs = {}
def absorb(lst, src):
    for p in lst or []:
        if not isinstance(p, dict) or p.get("chainId") != DSCHAIN: continue
        k = (p.get("pairAddress") or "").lower()
        if not k: continue
        prev = ds_pairs.get(k)
        if prev is None or liq(p) > liq(prev):
            p["_src"] = src; ds_pairs[k] = p

# A. batch by pair address (true 1:1, 30 per call)
for i in range(0, len(pair_addrs), 30):
    d = get(f"{DS}/latest/dex/pairs/{DSCHAIN}/" + ",".join(pair_addrs[i:i+30]))
    if d: absorb(d.get("pairs"), "pairbatch")
    if i % 600 == 0:
        print(f"  pair batches {i}/{len(pair_addrs)} -> {len(ds_pairs)} ds pairs", flush=True)
print(f"  after pair batches: {len(ds_pairs)} DS pairs ({stats['ds_calls']} calls)")

# B. token-level lookups for singleton pools + shortlisted bases
tokens = {p["base_token"].lower() for p in odd_pools if p.get("base_token")}
tokens |= {p["base_token"].lower() for p in short if p.get("base_token")}
tokens -= MAJORS
tokens = [t for t in tokens if t.startswith("0x") and len(t) == 42]
print(f"  token-level lookups: {len(tokens)}")
for n, t in enumerate(tokens):
    d = get(f"{DS}/token-pairs/v1/{DSCHAIN}/{t}")
    if isinstance(d, list): absorb(d, "tokenpairs")
    if n % 200 == 0:
        print(f"  tokens {n}/{len(tokens)} -> {len(ds_pairs)} ds pairs", flush=True)
print(f"  after token lookups: {len(ds_pairs)} DS pairs ({stats['ds_calls']} calls)")

# C. DEXScreener's own new-token feeds (chain slice)
prof = {}
for u in ["/token-profiles/latest/v1", "/token-boosts/latest/v1", "/token-boosts/top/v1"]:
    d = get(DS + u)
    for x in (d or []):
        if isinstance(x, dict) and x.get("chainId") == DSCHAIN and x.get("tokenAddress"):
            prof.setdefault(x["tokenAddress"].lower(), {"links": x.get("links"), "description": x.get("description")})
print(f"  DS profile/boost {DSCHAIN} tokens: {len(prof)}")
for t in prof:
    d = get(f"{DS}/token-pairs/v1/{DSCHAIN}/{t}")
    if isinstance(d, list): absorb(d, "profile")

qual = []
for p in ds_pairs.values():
    a, l = age_days(p), liq(p)
    if a is not None and a < FINAL_AGE and l >= FINAL_LIQ:
        p["_age_days"], p["_liq_usd"] = a, l
        qual.append(p)
qual.sort(key=lambda x: -x["_liq_usd"])
distinct = {p["baseToken"]["address"].lower() for p in qual} - MAJORS
print(f"\n[{CHAIN}] QUALIFYING (liq>=${FINAL_LIQ:,.0f}, age<{FINAL_AGE:.0f}d): {len(qual)} pairs, "
      f"{len(distinct)} distinct non-major base tokens")

json.dump({"chain": CHAIN, "qualifying": qual, "profiles": prof, "stats": stats,
           "errors": errors[:100], "total_ds_pairs_seen": len(ds_pairs)},
          open(f"{DATA}/ds_qualifying_{CHAIN}.json", "w"), indent=1)
print(f"wrote ds_qualifying_{CHAIN}.json | ds_calls={stats['ds_calls']} fail={stats['ds_fail']}")
