"""Merge ABI analysis + proxy/clone detection + exploit cross-check into the final CSV."""
import json, csv

DATA = "/home/user/test111/data"
a = json.load(open(f"{DATA}/abi_analysis.json"))
results, unverified = a["results"], a["unverified"]
clones = {k.lower(): v for k, v in json.load(open(f"{DATA}/minimal_proxies.json")).items()}

# Exploit findings. Each is grounded in a specific cited source; a ticker that merely
# collides with an old entry is recorded as a collision, never as an exploit.
EXPLOIT = {
 "0xd6a4f5aadd88eba9a170acf67f737bd488142857": dict(
   status="EXPLOITED", date="2026-07-30", source="SlowMist Hacked + crypto.news/CoinDesk",
   detail="~$625K. Off-chain signer key hardcoded as _signer in the ZhaiquanBuy contract was "
          "leaked; attacker forged signatures to buy ~687k STY at a 100x discount via a "
          "PancakeSwap flash loan and exited through the STY/USDT pool. Key compromise, not a "
          "signature-verification bug. Vulnerable code sits in ZhaiquanBuy, NOT in the STY token."),
 "0xa9d33e9203e7d4b9ea8f37eca73cfe810c5d7cd0": dict(
   status="EXPLOITED (paired contract)", date="2026-07-28", source="SlowMist Hacked",
   detail="~$52K, ~167,200 Pro tokens lost. The Pro token contract of Crypto DAO was exploited "
          "via missing access control on publicly callable vault functions. CDAO's only "
          "qualifying pool is CDAO/Pro (Pro=0x8D65744527f55d0b2338350912d5C99A81ddF0e2), so the "
          "exploited contract is this token's paired asset, not the CDAO token itself."),
 "0x8554d38b95e4f7ca11d391008627df30b2b07777": dict(
   status="ticker collision - ruled out", date="2021-12-08", source="SlowMist Hacked",
   detail="SlowMist lists a 2021 PIZZA exploit on eCurve. This deployment is an EIP-1167 clone "
          "of the 2026 launchpad implementation 0x024f1829..., shared with 19 other tokens in "
          "this set, so it is not the 2021 contract."),
 "0x9dbef6496134c151b9f9855cc5a1ee77f0324444": dict(
   status="ticker collision - UNRESOLVED", date="2024-05-08", source="SlowMist Hacked",
   detail="SlowMist lists a 2024 GPU exploit on BNB Chain (_transfer self-transfer balance bug). "
          "Could not confirm whether this is the same deployment: getcontractcreation is blocked "
          "on this API key and public RPCs are pruned, so historical eth_getCode fails. Contract "
          "shape differs (launchpad clone with init/setMode). Treat as unconfirmed."),
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
        "contract_name","total_functions","nonstandard_fn_count","keep_categories",
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

dump(f"{DATA}/bsc_contract_logic.csv", kept)
dump(f"{DATA}/bsc_contract_logic_dropped.csv", dropped)
with open(f"{DATA}/bsc_contract_logic_unanalyzable.csv", "w", newline="") as f:
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
print("\nwrote bsc_contract_logic{,_dropped,_unanalyzable}.csv")
