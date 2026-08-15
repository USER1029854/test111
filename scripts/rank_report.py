"""Final integration across all four chains.

Loads every custom-logic KEEP record (BSC from the committed CSV; ETH/Arbitrum/Base from
analysis_{chain}.json), clusters them into shared-codebase families with union-find over
{implementation, runtime-bytecode fingerprint, normalised-source hash, deployer}, scores
each by a transparent exploit-likelihood formula, and writes:
  data/exploit_candidates_ranked.csv   -- master ranked list, all four chains
  data/families.json                   -- shared-codebase family rollups
  data/rank_summary.txt                -- printed stats + top rows + family table

The score ranks a POPULATION by resemblance to what gets exploited. It is ordinal and its
components are documented; it is not a prediction about any individual contract.
"""
import json, csv, os, math, collections

DATA = "/home/user/test111/data"

def truthy(v): return str(v).strip().lower() in ("true", "1", "yes")
def fnum(v):
    try: return float(v)
    except Exception: return 0.0

MAJOR_INFRA = {  # never treat these as a shared "implementation" that forms a family
    "", "0x0000000000000000000000000000000000000000",
    "0x000000000000000000000000000000000000dead",
}
# Deployers that are shared public infrastructure, not one operator -> must not form a family.
FACTORY_DEPLOYERS = {
    "0x4e59b44847b379578588920ca78fbf26c0b4956c",  # canonical CREATE2 deterministic deployer
    "0x0000000000ffe8b47b3e2130213b802212439497",  # immutable create2 factory
}

records = []

# ---- BSC: committed custom-logic keep set ----
bsc_path = f"{DATA}/bsc_contract_logic.csv"
if os.path.exists(bsc_path):
    for r in csv.DictReader(open(bsc_path)):
        records.append({
            "chain": "bsc", "name": r["name"], "symbol": r["symbol"],
            "token_address": r["token_address"], "pair_address": r["pair_address"],
            "liquidity_usd": fnum(r["liquidity_usd"]), "age_days": fnum(r["age_days"]),
            "dex": r["dex"], "quote": r["quote"], "contract_name": r.get("contract_name", ""),
            "impl_contract_name": "",
            "keep_categories": r.get("keep_categories", ""),
            "nonstandard_fn_count": int(fnum(r.get("nonstandard_fn_count", 0))),
            "fund_fns": r.get("fund_fns", ""), "bridge_fns": r.get("bridge_fns", ""),
            "sig_gated_fns": r.get("sig_gated_fns", ""), "admin_mover_fns": r.get("admin_mover_fns", ""),
            "admin_setter_fns": r.get("admin_setter_fns", ""), "proxy_upgrade_fns": r.get("proxy_upgrade_fns", ""),
            "lifecycle_fns": r.get("lifecycle_fns", ""),
            "controls_reserve": truthy(r.get("controls_reserve_treasury_pool_vault")),
            "is_proxy": truthy(r.get("is_proxy")), "proxy_kind": r.get("proxy_kind", ""),
            "minimal_proxy_clone": truthy(r.get("minimal_proxy_clone")),
            "implementation": (r.get("effective_implementation") or "").lower(),
            "impl_verified": r.get("impl_verified", ""),
            "bytecode_fp": "", "source_norm_hash": "", "deployer": "",
            "upgrade_authority": r.get("upgrade_authority", ""), "upgrade_authority_src": r.get("upgrade_authority_src", ""),
            "exploit_status": r.get("exploit_status", ""), "exploit_detail": r.get("exploit_detail", ""),
            "risk_flags": r.get("risk_flags", ""), "goplus_flags": "",
            "holder_count": r.get("holder_count", ""),
            "websites": r.get("websites", ""), "socials": r.get("socials", ""),
        })

# ---- ETH / Arbitrum / Base: analysis_{chain}.json keep set ----
for ch in ("eth", "arbitrum", "base"):
    p = f"{DATA}/analysis_{ch}.json"
    if not os.path.exists(p):
        print(f"NOTE: {p} missing -- {ch} not yet analyzed, skipped"); continue
    blob = json.load(open(p))
    for r in blob["results"]:
        if not r.get("keep"): continue
        records.append({
            "chain": ch, "name": r.get("name", ""), "symbol": r.get("symbol", ""),
            "token_address": r["token_address"], "pair_address": r.get("pair_address", ""),
            "liquidity_usd": fnum(r.get("liquidity_usd")), "age_days": fnum(r.get("age_days")),
            "dex": r.get("dex", ""), "quote": r.get("quote", ""), "contract_name": r.get("contract_name", ""),
            "impl_contract_name": r.get("impl_contract_name", ""),
            "keep_categories": r.get("keep_categories", ""),
            "nonstandard_fn_count": int(r.get("nonstandard_fn_count", 0)),
            "fund_fns": r.get("fund_fns", ""), "bridge_fns": r.get("bridge_fns", ""),
            "sig_gated_fns": r.get("sig_gated_fns", ""), "admin_mover_fns": r.get("admin_mover_fns", ""),
            "admin_setter_fns": r.get("admin_setter_fns", ""), "proxy_upgrade_fns": r.get("proxy_upgrade_fns", ""),
            "lifecycle_fns": r.get("lifecycle_fns", ""),
            "controls_reserve": bool(r.get("controls_reserve_treasury_pool_vault")),
            "is_proxy": bool(r.get("is_proxy")), "proxy_kind": r.get("proxy_kind", ""),
            "minimal_proxy_clone": bool(r.get("minimal_proxy_clone")),
            "implementation": (r.get("implementation") or "").lower(),
            "impl_verified": r.get("impl_verified", ""),
            "bytecode_fp": (r.get("bytecode_fp") or "").lower(),
            "source_norm_hash": (r.get("source_norm_hash") or "").lower(),
            "deployer": (r.get("deployer") or "").lower(),
            "upgrade_authority": "", "upgrade_authority_src": "",
            "exploit_status": "", "exploit_detail": "",
            "risk_flags": "", "goplus_flags": r.get("goplus_flags", ""),
            "holder_count": r.get("holder_count", ""),
            "websites": r.get("websites", ""), "socials": r.get("socials", ""),
        })

print(f"total custom-logic KEEP records across chains: {len(records)}")
for ch in ("bsc", "eth", "arbitrum", "base"):
    print(f"  {ch}: {sum(1 for r in records if r['chain']==ch)}")

# ---- liquidity-quality guard: headline DEXScreener liquidity can be inflated/circular
# (a one-sided pool priced off a worthless token -> e.g. TAO/HBAR "MintBurnTeamToken" showed
# $2.1B/$1.4B on ~$0.40 of real WETH). The trustworthy figure is the QUOTE-side reserve, which
# is real external money. real_liq ~= 2 x quote_side_usd. Pools whose real side is below the
# $100k floor are moved OUT of the victim ranking; non-major quotes are flagged circular-risk. ----
QMAJORS = {  # trustworthy quote tokens per chain (by address)
 "bsc": {"0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c","0x55d398326f99059ff775485246999027b3197955",
  "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d","0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c",
  "0x2170ed0880ac9a755fd29b2688956bd959f933f8","0xc5f0f7b66764f6ec8c8dff7ba683102295e16409",
  "0xe9e7cea3dedca5984780bafc599bd69add087d56","0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82"},
 "eth": {"0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2","0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
  "0xdac17f958d2ee523a2206206994597c13d831ec7","0x6b175474e89094c44da98b954eedeac495271d0f",
  "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599","0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0"},
 "arbitrum": {"0x82af49447d8a07e3bd95bd0d56f35241523fbab1","0xaf88d065e77c8cc2239327c5edb3a432268e5831",
  "0xff970a61a04b1ca14834a43f5de4533ebddb5cc8","0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9",
  "0x912ce59144191c1204e64559fe8253a0e49e6548","0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f"},
 "base": {"0x4200000000000000000000000000000000000006","0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
  "0xd9aaec86b65d86f6a7b5b1b0c42ffa531710b6ca","0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf",
  "0x50c5725949a6f0c72e6c4a641f24049a917db0cb"},
}
QFILE = {"bsc": "ds_qualifying.json", "eth": "ds_qualifying_eth.json",
         "arbitrum": "ds_qualifying_arbitrum.json", "base": "ds_qualifying_base.json"}

def best_pairs(ch):
    p = f"{DATA}/{QFILE[ch]}"
    if not os.path.exists(p): return {}
    out = {}
    for pr in json.load(open(p))["qualifying"]:
        a = pr["baseToken"]["address"].lower()
        if a not in out or pr.get("_liq_usd", 0) > out[a].get("_liq_usd", 0):
            out[a] = pr
    return out

liq_lookup = {ch: best_pairs(ch) for ch in ("bsc", "eth", "arbitrum", "base")}

def liquidity_quality(r):
    pr = liq_lookup.get(r["chain"], {}).get(r["token_address"].lower())
    headline = r["liquidity_usd"]
    if not pr:
        return {"real_liquidity_usd": headline, "quote_side_usd": None, "vol24h_usd": None,
                "quote_is_major": None, "liquidity_quality": "unknown"}
    L = pr.get("liquidity") or {}
    pn, pu = pr.get("priceNative"), pr.get("priceUsd")
    qside = None
    try:
        if pn and float(pn) > 0 and L.get("quote") is not None:
            qside = float(L["quote"]) * (float(pu) / float(pn))
    except Exception:
        qside = None
    vol = None
    try: vol = float((pr.get("volume") or {}).get("h24") or 0)
    except Exception: pass
    qaddr = (pr.get("quoteToken") or {}).get("address", "").lower()
    qmajor = qaddr in QMAJORS.get(r["chain"], set())
    real = min(headline, 2 * qside) if qside is not None else headline
    if qside is not None and 2 * qside < 100_000:
        qual = "inflated"           # real external money below the six-figure floor
    elif not qmajor:
        qual = "thin_quote_circular_risk"
    else:
        qual = "good"
    return {"real_liquidity_usd": round(real, 2), "quote_side_usd": round(qside, 2) if qside is not None else None,
            "vol24h_usd": round(vol, 2) if vol is not None else None,
            "quote_is_major": qmajor, "liquidity_quality": qual}

for r in records:
    r.update(liquidity_quality(r))
inflated = [r for r in records if r["liquidity_quality"] == "inflated"]
records = [r for r in records if r["liquidity_quality"] != "inflated"]
print(f"excluded {len(inflated)} records for inflated/circular liquidity (real quote-side < $50k)")

# ---- union-find family clustering ----
parent = {}
def find(x):
    parent.setdefault(x, x)
    while parent[x] != x:
        parent[x] = parent[parent[x]]; x = parent[x]
    return x
def union(a, b):
    parent[find(a)] = find(b)

idx = {r["token_address"].lower(): i for i, r in enumerate(records)}
for r in records:
    find(r["token_address"].lower())

# link tokens that share any non-trivial structural key
def link_by(keyfn, tag):
    buckets = collections.defaultdict(list)
    for r in records:
        v = keyfn(r)
        if v and v not in MAJOR_INFRA and len(v) > 6:
            buckets[v].append(r["token_address"].lower())
    for v, toks in buckets.items():
        if len(toks) > 1:
            for t in toks[1:]:
                union(toks[0], t)
    return {v: toks for v, toks in buckets.items() if len(toks) > 1}

# A proxy's own runtime bytecode is the generic OZ ERC1967/beacon shell, identical across
# thousands of unrelated projects -> it must NOT form a family. Only non-proxy contracts
# (whose bytecode IS their logic) cluster by bytecode. Proxies cluster by implementation.
shared_impl = link_by(lambda r: r["implementation"], "implementation")
shared_bc   = link_by(lambda r: "" if r["is_proxy"] else r["bytecode_fp"], "bytecode")
shared_src  = link_by(lambda r: r["source_norm_hash"], "source")
shared_dep  = link_by(lambda r: "" if r["deployer"] in FACTORY_DEPLOYERS else r["deployer"], "deployer")

# assign families, size, and the basis that linked each
comp = collections.defaultdict(list)
for r in records:
    comp[find(r["token_address"].lower())].append(r)
fam_id = {}
families = []
for root, members in comp.items():
    if len(members) < 2:
        continue
    fid = f"FAM{len(families)+1:02d}"
    bases = set()
    # a basis holds only when a specific value is shared by >=2 members of THIS family
    def shared_val(keyfn, skip_proxy_shell=False):
        c = collections.Counter()
        for m in members:
            if skip_proxy_shell and m["is_proxy"]:
                continue
            v = keyfn(m)
            if v and v not in MAJOR_INFRA and v not in FACTORY_DEPLOYERS and len(v) > 6:
                c[v] += 1
        return {v for v, n in c.items() if n >= 2}
    impls = shared_val(lambda m: m["implementation"])
    if impls: bases.add("shared_implementation")
    if shared_val(lambda m: m["bytecode_fp"], skip_proxy_shell=True): bases.add("identical_bytecode")
    if shared_val(lambda m: m["source_norm_hash"]): bases.add("identical_source")
    if shared_val(lambda m: m["deployer"]): bases.add("same_deployer")
    for m in members:
        fam_id[m["token_address"].lower()] = fid
    chains = sorted(set(m["chain"] for m in members))
    families.append({
        "family_id": fid, "size": len(members), "chains": chains,
        "basis": sorted(bases) or ["shared_structural_key"],
        "implementations": sorted(impls)[:6],
        "total_liquidity_usd": round(sum(m["liquidity_usd"] for m in members), 2),
        # only a confirmed exploit counts -- a ruled-out ticker collision must not flag a family
        "any_exploited": any("EXPLOITED" in (m["exploit_status"] or "").upper() for m in members),
        "members": [{"chain": m["chain"], "symbol": m["symbol"], "address": m["token_address"],
                     "liquidity_usd": round(m["liquidity_usd"], 2)} for m in
                    sorted(members, key=lambda x: -x["liquidity_usd"])],
    })
families.sort(key=lambda f: (-f["size"], -f["total_liquidity_usd"]))
fam_size = {}
for f in families:
    for m in f["members"]:
        fam_size[m["address"].lower()] = f["size"]

# ---- exploit-likelihood score (documented, ordinal) ----
def has(r, *cats): return any(c in (r["keep_categories"] or "") for c in cats)
def score(r):
    s, why = 0.0, []
    def add(pts, tag):
        nonlocal s
        if pts: s += pts; why.append(f"{tag}+{pts:g}")
    add(12 if has(r, "fund_ops") else 0, "fund_ops")
    add(10 if r["controls_reserve"] else 0, "controls_reserve")
    add(14 if (has(r, "proxy_upgrade") or r["proxy_upgrade_fns"]) else 0, "swappable_logic")
    add(8 if has(r, "bridge_ops") else 0, "bridge")
    add(8 if has(r, "sig_gated") else 0, "sig_gated")
    add(10 if has(r, "admin_token_mover") else 0, "admin_mover")
    add(6 if has(r, "admin_treasury_pool_signer") else 0, "admin_setters")
    add(5 if has(r, "lifecycle_ops") else 0, "lifecycle")
    add(round(min(r["nonstandard_fn_count"], 20) * 0.6, 1), "surface_breadth")
    # unreviewed money-moving code behind a proxy whose implementation is unverified
    if r["is_proxy"] and str(r.get("impl_verified")).lower() in ("false",):
        add(10, "unverified_impl")
    # shared-codebase blast radius: a flaw here is a flaw across the family
    fs = fam_size.get(r["token_address"].lower(), 1)
    if fs >= 2:
        add(round(min(fs, 25) * 1.4, 1), f"family_x{fs}")
    # attacker incentive (REAL quote-side liquidity, log scaled) and unreviewed window (recency)
    rl = r.get("real_liquidity_usd") or r["liquidity_usd"]
    if rl > 0:
        add(round(min(6.0, max(0.0, math.log10(rl / 100_000.0) * 4.0)), 1), "liquidity")
    add(round(max(0.0, (60 - r["age_days"]) / 60.0) * 6.0, 1), "recency")
    for flag, pts in [("mintable", 3), ("pausable", 2), ("hidden_owner", 5),
                      ("reclaimable_ownership", 5), ("external_call", 3), ("selfdestruct", 6)]:
        if flag in (r["goplus_flags"] or "") or flag in (r["risk_flags"] or ""):
            add(pts, flag)
    return round(s, 1), " ".join(why)

honeypots = []
for r in records:
    r["family_id"] = fam_id.get(r["token_address"].lower(), "")
    r["family_size"] = fam_size.get(r["token_address"].lower(), 1)
    sc, why = score(r)
    r["exploit_likelihood_score"], r["score_breakdown"] = sc, why
    if "HONEYPOT" in (r["goplus_flags"] or ""):
        honeypots.append(r)

# a honeypot is a scam-on-buyers, not a contract-exploit victim -> set aside from the victim ranking
ranked = [r for r in records if "HONEYPOT" not in (r["goplus_flags"] or "")]
ranked.sort(key=lambda r: -r["exploit_likelihood_score"])

cols = ["rank", "chain", "symbol", "name", "token_address", "exploit_likelihood_score",
        "real_liquidity_usd", "liquidity_usd", "liquidity_quality", "quote_side_usd", "vol24h_usd",
        "quote_is_major", "age_days", "keep_categories", "controls_reserve",
        "is_proxy", "proxy_kind", "minimal_proxy_clone", "implementation", "impl_verified",
        "family_id", "family_size", "contract_name", "impl_contract_name",
        "deployer", "bytecode_fp", "source_norm_hash",
        "exploit_status", "fund_fns", "bridge_fns", "admin_mover_fns", "proxy_upgrade_fns",
        "sig_gated_fns", "goplus_flags", "risk_flags", "holder_count", "dex", "quote",
        "pair_address", "score_breakdown", "websites", "socials"]
with open(f"{DATA}/exploit_candidates_ranked.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader()
    for i, r in enumerate(ranked, 1):
        r["rank"] = i; w.writerow(r)

json.dump({"families": families, "n_records": len(records), "n_honeypots": len(honeypots),
           "excluded_inflated": [{"chain": r["chain"], "symbol": r["symbol"], "address": r["token_address"],
                "headline_liquidity_usd": r["liquidity_usd"], "quote_side_usd": r["quote_side_usd"],
                "contract_name": r.get("contract_name", ""), "keep_categories": r["keep_categories"]}
               for r in sorted(inflated, key=lambda x: -x["liquidity_usd"])],
           "honeypots": [{"chain": r["chain"], "symbol": r["symbol"], "address": r["token_address"],
                "goplus_flags": r["goplus_flags"]} for r in honeypots]},
          open(f"{DATA}/families.json", "w"), indent=1)

# ---- summary ----
out = []
def pr(m): out.append(m); print(m)
pr(f"\n==== RANKED CUSTOM-LOGIC EXPLOIT CANDIDATES (all chains) ====")
pr(f"custom-logic KEEP records: {len(records)+len(inflated)} | "
   f"excluded inflated/circular liq: {len(inflated)} | honeypots set aside: {len(honeypots)} | "
   f"ranked victim-candidates: {len(ranked)}")
for ch in ("bsc", "eth", "arbitrum", "base"):
    n = sum(1 for r in ranked if r["chain"] == ch)
    liq = sum((r.get("real_liquidity_usd") or 0) for r in ranked if r["chain"] == ch)
    pr(f"  {ch:9s}: {n:3d} candidates  (${liq:,.0f} real quote-side liquidity)")
pr(f"\nshared-codebase families (>=2 members): {len(families)}")
pr(f"  cross-chain families: {sum(1 for f in families if len(f['chains'])>1)}")
pr(f"\n--- top 25 by exploit-likelihood score ---")
for i, r in enumerate(ranked[:25], 1):
    fam = f" [{r['family_id']}x{r['family_size']}]" if r["family_id"] else ""
    ex = " EXPLOITED" if r["exploit_status"] else ""
    q = "" if r["liquidity_quality"] == "good" else f" ~{r['liquidity_quality']}"
    pr(f"{i:2d}. score={r['exploit_likelihood_score']:>5.1f} {r['chain']:4s} {r['symbol']:<12} "
       f"{r['token_address']} real≈${(r.get('real_liquidity_usd') or 0):>11,.0f} {r['age_days']:>4.0f}d "
       f"{r['keep_categories'][:40]}{fam}{ex}{q}")
pr(f"\n--- largest shared-codebase families ---")
for f in families[:14]:
    xc = "CROSS-CHAIN " if len(f["chains"]) > 1 else ""
    pr(f"  {f['family_id']} size={f['size']:2d} {xc}chains={','.join(f['chains'])} "
       f"basis={','.join(f['basis'])} liq=${f['total_liquidity_usd']:,.0f}"
       f"{' EXPLOITED-MEMBER' if f['any_exploited'] else ''}")
open(f"{DATA}/rank_summary.txt", "w").write("\n".join(out))

# ---- paste-ready markdown tables for the report ----
def logic_label(r):
    lab = r.get("impl_contract_name") or r.get("contract_name") or ""
    cats = (r["keep_categories"] or "").replace("admin_treasury_pool_signer", "admin-setters") \
        .replace("admin_token_mover", "admin-mover").replace("proxy_upgrade", "upgradeable") \
        .replace("fund_ops", "fund-ops").replace("lifecycle_ops", "lifecycle") \
        .replace("bridge_ops", "bridge").replace("sig_gated", "sig-gated") \
        .replace("admin_config_gated", "admin-config").replace("|", ", ")
    return (f"`{lab}` — " if lab and lab not in ("Token", "ERC1967Proxy") else "") + cats

md = ["### Top 30 candidates by exploit-likelihood score\n",
      "| # | Score | Chain | Symbol | Address | Real liq (quote-side) | Age | Custom logic | Family | Liq quality |",
      "|--:|--:|:--|:--|:--|--:|--:|:--|:--|:--|"]
for i, r in enumerate(ranked[:30], 1):
    fam = f"{r['family_id']} (×{r['family_size']})" if r["family_id"] else "—"
    ex = " ⚠️EXPLOITED" if r["exploit_status"] else ""
    md.append(f"| {i} | {r['exploit_likelihood_score']:.1f} | {r['chain']} | {r['symbol']}{ex} | "
              f"`{r['token_address']}` | ${(r.get('real_liquidity_usd') or 0):,.0f} | {r['age_days']:.0f}d | "
              f"{logic_label(r)} | {fam} | {r['liquidity_quality']} |")
md.append("\n### Shared-codebase families (one flaw implicates all members)\n")
md.append("| Family | Size | Chain(s) | Linked by | Combined liq | Members |")
md.append("|:--|--:|:--|:--|--:|:--|")
for f in families:
    mem = ", ".join(f"{m['symbol']}" for m in f["members"])
    md.append(f"| {f['family_id']} | {f['size']} | {','.join(f['chains'])} | {', '.join(f['basis'])} | "
              f"${f['total_liquidity_usd']:,.0f} | {mem} |")
md.append("\n### Excluded — inflated / circular liquidity (headline USD not real money)\n")
md.append("| Chain | Symbol | Address | Headline liq | Real quote-side | Contract |")
md.append("|:--|:--|:--|--:|--:|:--|")
for r in sorted(inflated, key=lambda x: -x["liquidity_usd"]):
    md.append(f"| {r['chain']} | {r['symbol']} | `{r['token_address']}` | ${r['liquidity_usd']:,.0f} | "
              f"${(r['quote_side_usd'] or 0):,.0f} | {r.get('contract_name','')} |")
open(f"{DATA}/report_tables.md", "w").write("\n".join(md))
print("\nwrote exploit_candidates_ranked.csv, families.json, rank_summary.txt, report_tables.md")
