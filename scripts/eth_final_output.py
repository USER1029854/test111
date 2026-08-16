"""Merge ABI analysis + proxy/clone detection + exploit cross-check into the final CSV."""
import json, csv

DATA = "/home/user/test111/data"
a = json.load(open(f"{DATA}/eth_abi_analysis.json"))
results, unverified = a["results"], a["unverified"]
clones = {k.lower(): v for k, v in json.load(open(f"{DATA}/eth_minimal_proxies.json")).items()}

# Exploit findings. Each entry here was individually researched and corroborated
# (SlowMist hit + independent source) before being recorded -- a ticker that merely
# collides with an old, unrelated entry is recorded as a collision, never as an
# exploit. Filled in after reviewing data/eth_hack_matches.json; empty means no
# corroborated hit was found among the kept/unverified set at time of writing.
EXPLOIT = {
}

impl_count = {}
for r in results:
    for k in (r.get("implementation"), clones.get(r["token_address"].lower())):
        if k: impl_count[k.lower()] = impl_count.get(k.lower(), 0) + 1

rows = []
for r in results:
    addr = r["token_address"].lower()
    mp = clones.get(addr)
    e = EXPLOIT.get(addr, {})
    impl = mp or r.get("implementation") or ""
    rows.append({**r,
        "minimal_proxy_clone": bool(mp),
        "clone_implementation": mp or "",
        "effective_implementation": impl,
        "impl_shared_by_n_tokens": impl_count.get(impl.lower(), 0) if impl else 0,
        "exploit_status": e.get("status", ""),
        "exploit_date": e.get("date", ""),
        "exploit_source": e.get("source", ""),
        "exploit_detail": e.get("detail", ""),
    })

kept = [r for r in rows if r["keep"]]
dropped = [r for r in rows if not r["keep"]]
kept.sort(key=lambda r: -float(r["liquidity_usd"]))

cols = ["name","symbol","token_address","pair_address","liquidity_usd","age_days","dex","quote",
        "quote_address","contract_name","total_functions","nonstandard_fn_count","keep_categories",
        "fund_fns","sig_gated_fns","has_eip2612_permit","admin_setter_fns","admin_mover_fns",
        "bridge_fns","lifecycle_fns","proxy_upgrade_fns","admin_config_fns","admin_only_confirmed",
        "controls_reserve_treasury_pool_vault","reserve_identifiers",
        "is_proxy","proxy_kind","minimal_proxy_clone","effective_implementation",
        "impl_shared_by_n_tokens","impl_verified","proxy_admin","upgrade_authority",
        "upgrade_authority_src","exploit_status","exploit_date","exploit_source","exploit_detail",
        "holder_count","risk_flags","websites","socials"]

def dump(path, data, extra=()):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(cols) + list(extra), extrasaction="ignore")
        w.writeheader()
        for x in data: w.writerow(x)

dump(f"{DATA}/eth_contract_logic.csv", kept)
dump(f"{DATA}/eth_contract_logic_dropped.csv", dropped)
with open(f"{DATA}/eth_contract_logic_unanalyzable.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["name","symbol","token_address","pair_address",
        "liquidity_usd","age_days","dex","reason"], extrasaction="ignore")
    w.writeheader()
    for x in unverified: w.writerow(x)

print(f"BEFORE logic filter (tokens carried in)      : {len(results)+len(unverified)}")
print(f"  verified source, ABI parsed                : {len(results)}")
print(f"  unverified / no ABI (not analyzable)       : {len(unverified)}")
print(f"AFTER logic filter (fund-handling/privileged): {len(kept)}")
print(f"  dropped as plain ERC-20                    : {len(dropped)}")
print()
print(f"proxies                : {sum(1 for r in kept if r['is_proxy'])}")
print(f"minimal-proxy clones   : {sum(1 for r in kept if r['minimal_proxy_clone'])}")
print(f"controls reserve/vault : {sum(1 for r in kept if r['controls_reserve_treasury_pool_vault'])}")
print(f"exploited / flagged    : {sum(1 for r in kept if r['exploit_status'])}")
print("\nwrote eth_contract_logic{,_dropped,_unanalyzable}.csv")
