"""Phase 2: enrich candidates with DEXScreener data (the source of record).

Every metric reported downstream comes from a DEXScreener response captured here.
GeckoTerminal values are kept only for shortlisting/audit, never reported as fact.
"""
import requests, json, time, os

H = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
DS = "https://api.dexscreener.com"
NOW = time.time()
DATA = "/home/user/test111/data"

# Loose shortlist bounds -- DEXScreener is the authority, so leave slack on both
# sides and let the strict filter happen on DS numbers, not GT numbers.
SHORT_LIQ, SHORT_AGE = 40_000.0, 105.0
FINAL_LIQ, FINAL_AGE = 100_000.0, 90.0   # 90d cap upstream; primary target is <60d (labelled downstream)

stats = {"ds_calls": 0, "ds_fail": 0}
errors = []

def get(url, tries=4):
    delay = 0.35
    for t in range(tries):
        try:
            stats["ds_calls"] += 1
            r = requests.get(url, timeout=35, headers=H)
            if r.status_code == 200:
                time.sleep(delay)
                return r.json()
            if r.status_code == 429:
                time.sleep(6 * (t + 1)); continue
            if r.status_code in (400, 404):
                return None
            time.sleep(1.5 * (t + 1))
        except Exception as e:
            errors.append(f"{url[:80]} :: {type(e).__name__}")
            time.sleep(1.5 * (t + 1))
    stats["ds_fail"] += 1
    return None

def age_days(p):
    ts = p.get("pairCreatedAt")
    return None if not ts else (NOW - ts / 1000.0) / 86400.0

def liq(p):
    return float(((p.get("liquidity") or {}).get("usd")) or 0)

# merge both independent discovery nets, deduped by pool address
pools, seen, srcinfo = [], set(), {}
for fn in ("eth_gt_pools.json", "eth_ds_search_pools.json"):
    path = f"{DATA}/{fn}"
    if not os.path.exists(path):
        print(f"WARNING: {fn} missing -- that net contributed nothing"); continue
    blob = json.load(open(path))
    n = 0
    for p in blob["pools"]:
        k = p["pool_address"].lower()
        if k in seen:
            continue
        seen.add(k); pools.append(p); n += 1
    srcinfo[fn] = {"total": len(blob["pools"]), "new": n, "errors": len(blob.get("errors", []))}
    print(f"loaded {fn}: {len(blob['pools'])} pools ({n} new), {len(blob.get('errors',[]))} errors")
print(f"merged discovery universe: {len(pools)} unique pools")

# ---- shortlist -------------------------------------------------------------
def gt_age(p):
    c = p.get("gt_created")
    if not c: return None
    try:
        return (NOW - time.mktime(time.strptime(c, "%Y-%m-%dT%H:%M:%SZ"))) / 86400.0
    except Exception:
        return None

# Pair-batching is 1:1 and 30-per-call, so the batch net is made maximally
# inclusive: every pool that could plausibly be recent OR liquid gets a real
# DEXScreener reading. Per-token lookups (1 call each) stay on the tighter set.
def recent(p):
    a = gt_age(p)
    return a is None or a <= SHORT_AGE

def reserve(p):
    try: return float(p.get("gt_reserve_usd") or 0)
    except Exception: return 0.0

batch_set = [p for p in pools if recent(p) or reserve(p) >= SHORT_LIQ]
short     = [p for p in pools if reserve(p) >= SHORT_LIQ and recent(p)]
print(f"batch net (recent OR reserve>=${SHORT_LIQ:,.0f}): {len(batch_set)}")
print(f"token-lookup net (reserve>=${SHORT_LIQ:,.0f} AND age<={SHORT_AGE:.0f}d): {len(short)}")

pair_addrs = [p["pool_address"] for p in batch_set
              if p["pool_address"].startswith("0x") and len(p["pool_address"]) == 42]
odd_pools  = [p for p in batch_set
              if not (p["pool_address"].startswith("0x") and len(p["pool_address"]) == 42)]
print(f"  standard pool addrs: {len(pair_addrs)} | singleton/v4-style pool ids: {len(odd_pools)}")

ds_pairs = {}
def absorb(lst, src):
    for p in lst or []:
        if not isinstance(p, dict) or p.get("chainId") != "ethereum": continue
        k = (p.get("pairAddress") or "").lower()
        if not k: continue
        prev = ds_pairs.get(k)
        if prev is None or liq(p) > liq(prev):
            p["_src"] = src
            ds_pairs[k] = p

# ---- A. batch by pair address (true 1:1, 30 per call) ----------------------
for i in range(0, len(pair_addrs), 30):
    b = pair_addrs[i:i + 30]
    d = get(f"{DS}/latest/dex/pairs/ethereum/" + ",".join(b))
    if d: absorb(d.get("pairs"), "pairbatch")
    if i % 600 == 0:
        print(f"  pair batches {i}/{len(pair_addrs)} -> {len(ds_pairs)} ds pairs", flush=True)
print(f"after pair batches: {len(ds_pairs)} DS pairs ({stats['ds_calls']} calls)")

# ---- B. token-level lookups for singleton pools + all shortlisted bases -----
tokens = {p["base_token"].lower() for p in odd_pools if p.get("base_token")}
tokens |= {p["base_token"].lower() for p in short if p.get("base_token")}
QUOTE_SET = {a.lower() for a in [
    "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2","0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "0xdAC17F958D2ee523a2206206994597C13D831ec7","0x6B175474E89094C44Da98b954EedeAC495271d0F",
    "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599","0x0000000000000000000000000000000000000000"]}
tokens -= QUOTE_SET
tokens = [t for t in tokens if t.startswith("0x") and len(t) == 42]
print(f"token-level lookups: {len(tokens)}")
for n, t in enumerate(tokens):
    d = get(f"{DS}/token-pairs/v1/ethereum/{t}")
    if isinstance(d, list): absorb(d, "tokenpairs")
    if n % 200 == 0:
        print(f"  tokens {n}/{len(tokens)} -> {len(ds_pairs)} ds pairs", flush=True)
print(f"after token lookups: {len(ds_pairs)} DS pairs ({stats['ds_calls']} calls)")

# ---- C. DEXScreener's own new-token feeds (Ethereum slice) ----------------------
prof = {}
for u in ["/token-profiles/latest/v1", "/token-boosts/latest/v1", "/token-boosts/top/v1"]:
    d = get(DS + u)
    for x in (d or []):
        if isinstance(x, dict) and x.get("chainId") == "ethereum" and x.get("tokenAddress"):
            a = x["tokenAddress"].lower()
            prof.setdefault(a, {"links": x.get("links"), "description": x.get("description")})
print(f"DS profile/boost Ethereum tokens: {len(prof)}")
for t in prof:
    d = get(f"{DS}/token-pairs/v1/ethereum/{t}")
    if isinstance(d, list): absorb(d, "profile")

# ---- final filter on DEXScreener numbers ----------------------------------
qual = []
for p in ds_pairs.values():
    a, l = age_days(p), liq(p)
    if a is not None and a < FINAL_AGE and l >= FINAL_LIQ:
        p["_age_days"], p["_liq_usd"] = a, l
        qual.append(p)
qual.sort(key=lambda x: -x["_liq_usd"])
print(f"\nQUALIFYING (liq>=${FINAL_LIQ:,.0f}, age<{FINAL_AGE:.0f}d): {len(qual)} pairs")
print(f"distinct base tokens: {len({p['baseToken']['address'].lower() for p in qual})}")

json.dump({"qualifying": qual, "profiles": prof, "stats": stats, "discovery": srcinfo,
           "errors": errors[:100], "total_ds_pairs_seen": len(ds_pairs)},
          open(f"{DATA}/eth_ds_qualifying.json", "w"), indent=1)
print("wrote eth_ds_qualifying.json | ds_calls=%d fail=%d" % (stats["ds_calls"], stats["ds_fail"]))
