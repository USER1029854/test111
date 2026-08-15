"""Render one self-contained, copy-pasteable Markdown block per ranked candidate.

Reads data/exploit_candidates_ranked.csv + data/families.json and writes
data/candidates.md: an index by chain, then a block per candidate with everything
the mapping step needs (chain, address, real+headline liquidity, age, the custom
logic that makes it a candidate, family/lineage, deployer, links).
"""
import csv, json, datetime

DATA = "/home/user/test111/data"
RUN_DATE = datetime.date(2026, 8, 15)  # snapshot date (age measured then)

ESCAN = {"eth": "https://etherscan.io/address/", "bsc": "https://bscscan.com/address/",
         "arbitrum": "https://arbiscan.io/address/", "base": "https://basescan.org/address/"}
DSCHAIN = {"eth": "ethereum", "bsc": "bsc", "arbitrum": "arbitrum", "base": "base"}
CHAIN_NAME = {"eth": "Ethereum", "bsc": "BNB Chain", "arbitrum": "Arbitrum", "base": "Base"}
# recognisable template lineages beyond exact-clone families (by verified impl/contract name)
LINEAGE = {
    "StakedTrUSD": "Ethena USDe/sUSDe staking-vault fork", "TrUSD": "Ethena USDe/sUSDe fork (base minter)",
    "StakedUSDat": "Ethena USDe/sUSDe staking-vault fork", "ApyUSD": "Ethena USDe/sUSDe fork (base minter)",
    "ApxUSD": "Ethena USDe/sUSDe fork (base minter)",
    "BackedAutoFeeTokenImplementation": "Backed Finance tokenised-RWA template",
    "FXRPOFT": "LayerZero OFT (cross-chain) template", "FlapTaxTokenV3": "BSC launchpad tax-token template",
}

rows = list(csv.DictReader(open(f"{DATA}/exploit_candidates_ranked.csv")))
fam = json.load(open(f"{DATA}/families.json"))
fam_by_id = {f["family_id"]: f for f in fam["families"]}

def f2(v):
    try: return float(v)
    except Exception: return 0.0

def money(v):
    v = f2(v)
    return f"${v:,.0f}"

def deployed(age):
    try: return (RUN_DATE - datetime.timedelta(days=float(age))).isoformat()
    except Exception: return "?"

def logic_line(r):
    label = r.get("impl_contract_name") or r.get("contract_name") or ""
    cats = (r["keep_categories"] or "").replace("_", " ").replace("|", ", ")
    fns = []
    for col, tag in [("fund_fns", "fund"), ("proxy_upgrade_fns", "upgrade"),
                     ("bridge_fns", "bridge"), ("admin_mover_fns", "fund-mover"), ("sig_gated_fns", "sig")]:
        v = r.get(col)
        if v:
            fns.append(f"{tag}: `{v.replace('|', '`, `')}`")
    out = ""
    if label and label not in ("Token", "ERC1967Proxy", "BeaconProxy"):
        out += f"impl/contract `{label}` — "
    out += f"**{cats}**"
    if fns:
        out += "\n  - key fns → " + " · ".join(fns)
    return out

def family_line(r):
    fid = r.get("family_id")
    if fid and fid in fam_by_id:
        F = fam_by_id[fid]
        sibs = [m for m in F["members"] if m["address"].lower() != r["token_address"].lower()]
        sib_txt = "; ".join(f"{m['symbol']} `{m['address']}` ({m['chain']})" for m in sibs)
        return (f"**{fid}** — shares a codebase with {len(sibs)} other(s) via "
                f"*{', '.join(F['basis'])}*. A flaw here is a flaw in all {F['size']} members.\n"
                f"  - siblings: {sib_txt}")
    lin = LINEAGE.get(r.get("impl_contract_name") or "") or LINEAGE.get(r.get("contract_name") or "")
    if lin:
        return (f"No exact-clone family, but this is a **{lin}** — a *template lineage*: separate "
                f"deployments of a shared codebase that inherit risk together (see README).")
    return "No exact-clone family or known template lineage detected."

out = ["# Exploit-candidate reference — per-candidate blocks",
       "",
       f"Snapshot **{RUN_DATE.isoformat()}**. {len(rows)} custom-logic candidates across four chains, "
       "ranked by exploit-likelihood score. Each block is self-contained — copy one to hand a single "
       "target into the mapping/audit step.",
       "",
       "> Risk-ranking of a population, not a prediction about any individual contract. Every value traces "
       "to on-chain / DEXScreener data captured in `data/`. `Real liq` is the **quote-side** reserve (real "
       "external money), not the headline. For staking-vault / paired-contract cases the real value at risk "
       "is the **satellite/vault TVL**, which the mapping step must pull separately.",
       ""]

# index by chain
by_chain = {}
for r in rows:
    by_chain.setdefault(r["chain"], []).append(r)
out.append("## Index")
for ch in ("eth", "bsc", "base", "arbitrum"):
    if ch in by_chain:
        syms = ", ".join(f"#{r['rank']} {r['symbol']}" for r in by_chain[ch])
        out.append(f"- **{CHAIN_NAME[ch]}** ({len(by_chain[ch])}): {syms}")
out.append("\n---\n")

for r in rows:
    ch = r["chain"]
    warn = "  ⚠️ **ALREADY EXPLOITED**" if r.get("exploit_status") else ""
    out.append(f"## #{r['rank']} · {r['symbol']} · {CHAIN_NAME[ch]} · score {r['exploit_likelihood_score']}{warn}")
    nm = r.get("name") or ""
    if nm and nm.lower() != (r["symbol"] or "").lower():
        out.append(f"*{nm}*")
    out.append("")
    out.append(f"- **Chain:** {CHAIN_NAME[ch]}")
    out.append(f"- **Token address:** `{r['token_address']}`  ·  [explorer]({ESCAN[ch]}{r['token_address']})")
    liq = f"{money(r['real_liquidity_usd'])} real quote-side"
    if f2(r['liquidity_usd']) != f2(r['real_liquidity_usd']):
        liq += f"  (headline {money(r['liquidity_usd'])})"
    if r.get("liquidity_quality") and r["liquidity_quality"] != "good":
        liq += f"  — ⚠ *{r['liquidity_quality']}*"
    out.append(f"- **Liquidity:** {liq}")
    out.append(f"- **Age / qualified by:** {f2(r['age_days']):.0f} days (≈ deployed {deployed(r['age_days'])})")
    out.append(f"- **Custom logic:** {logic_line(r)}")
    out.append(f"- **Controls reserve/treasury/pool/vault:** {'yes' if r.get('controls_reserve')=='True' else 'no'}")
    if r.get("is_proxy") == "True":
        iv = r.get("impl_verified")
        ivs = {"True": "verified", "False": "UNVERIFIED impl ⚠", "None": "impl unknown", "": ""}.get(str(iv), str(iv))
        impl = r.get("implementation") or "?"
        out.append(f"- **Proxy / swappable logic:** {r.get('proxy_kind') or 'proxy'} → impl `{impl}` ({ivs})")
    out.append(f"- **Shared codebase:** {family_line(r)}")
    if r.get("deployer"):
        out.append(f"- **Deployer:** `{r['deployer']}`")
    dsurl = f"https://dexscreener.com/{DSCHAIN[ch]}/{r['pair_address']}"
    out.append(f"- **Market:** {r.get('dex','?')} · quote {r.get('quote','?')} · pair `{r['pair_address']}` · [DexScreener]({dsurl})")
    flags = "; ".join(x for x in [r.get("goplus_flags"), r.get("risk_flags")] if x)
    if flags:
        out.append(f"- **Safety flags:** {flags}")
    if r.get("holder_count"):
        out.append(f"- **Holders:** {r['holder_count']}")
    if r.get("exploit_status"):
        out.append(f"- **Exploit status:** {r['exploit_status']}")
    out.append(f"- **Why (score {r['exploit_likelihood_score']}):** {r.get('score_breakdown','')}")
    out.append("")

# appendix: excluded / not candidates
out.append("---\n\n## Appendix — excluded (NOT candidates)")
out.append("Inflated / circular liquidity (headline USD is not real money):\n")
for e in fam.get("excluded_inflated", []):
    out.append(f"- **{e['symbol']}** ({e['chain']}) `{e['address']}` — headline {money(e['headline_liquidity_usd'])}, "
               f"real quote-side {money(e.get('quote_side_usd') or 0)} [{e.get('contract_name','')}]")
if fam.get("honeypots"):
    out.append("\nHoneypots (scam-on-buyers, set aside from the victim ranking):\n")
    for h in fam["honeypots"]:
        out.append(f"- **{h['symbol']}** ({h['chain']}) `{h['address']}` — {h.get('goplus_flags','')}")

open(f"{DATA}/candidates.md", "w").write("\n".join(out))
print(f"wrote data/candidates.md — {len(rows)} candidate blocks")
