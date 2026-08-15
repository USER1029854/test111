"""Phase 3 multichain: for each qualifying candidate, decide custom-logic vs bare token,
and collect every family signal (implementation, bytecode fingerprint, deployer, source hash).

Per token, via Etherscan V2 (chainid) on the free key -- all three endpoints are available
on eth/arbitrum/base (unlike BSC):
  * getsourcecode      -> source, ABI, ContractName, Proxy, Implementation, compiler
  * proxy/eth_getCode  -> runtime bytecode -> EIP-1167 clone detection + metadata-stripped hash
  * getcontractcreation-> deployer address + block (deployer-family clustering)
GoPlus is queried only for the kept set (honeypot/mintable/pausable/owner flags).

The custom-logic classifier is the BSC one verbatim: view/pure excluded, ERC-20 boilerplate
excluded, admin-only confirmed by reading source modifiers. A bare token (only balance
shuffling) is dropped; anything with fund-moving or privileged surface is kept.

Usage: python3 analyze_multi.py <eth|arbitrum|base>
"""
import requests, json, re, csv, sys, time, hashlib

CHAIN = sys.argv[1]
CHAINID = {"eth": 1, "arbitrum": 42161, "base": 8453}[CHAIN]
KEY = "R6PYYNEX4CNFAXX4YX3K8W4NXSBGGG4QGJ"
H = {"User-Agent": "Mozilla/5.0"}
DATA = "/home/user/test111/data"
ES = "https://api.etherscan.io/v2/api"

MAJORS = {a.lower() for a in {
    "eth": ["0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2","0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "0xdAC17F958D2ee523a2206206994597C13D831ec7","0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599","0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0"],
    "arbitrum": ["0x82aF49447D8a07e3bd95BD0d56f35241523fBab1","0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
            "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8","0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
            "0x912CE59144191C1204E64559FE8253a0e49E6548","0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f"],
    "base": ["0x4200000000000000000000000000000000000006","0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
            "0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA","0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf",
            "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb"],
}[CHAIN]}

# ---- classifier (identical posture to the BSC analyze_abi.py) ----
STD = {"name","symbol","decimals","totalsupply","balanceof","transfer","transferfrom","approve",
       "allowance","increaseallowance","decreaseallowance","getowner","owner","renounceownership",
       "transferownership","domain_separator","nonces","eip712domain","version","paused",
       "supportsinterface","implementation","admin"}
BOILER = {"approve","transfer","transferfrom","increaseallowance","decreaseallowance",
          "renounceownership","transferownership"}
FUND = re.compile(r"(claim|mint|burn|recycl|releas|reward|harvest|stak|unstak|deposit|withdraw|"
                  r"redeem|vault|distribut|settle)", re.I)
ADMIN_SET = re.compile(r"^set.*(treasur|reserve|pool|vault|signer|fee|router|receiver|wallet|"
                       r"operator|admin|manager|minter|oracle|bridge|market|dev|tax|swap|pair|liquid|"
                       r"fund|collector|beneficiar|peer|delegate|inspector|precrime|enforcedoption|"
                       r"trusted|remote|endpoint)", re.I)
ADMIN_MOVE = re.compile(r"(rescue|sweep|recover|salvage|emergenc|airdrop|seize|withdrawstuck|"
                        r"clearstuck|takeout|transferany|forcetransfer|admintransfer|withdrawtoken|"
                        r"withdrawerc20|drain)", re.I)
BRIDGE = re.compile(r"^(send|sendfrom|lzreceive|bridge|crosschain|teleport|relay|"
                    r"lzreceiveandrevert|lzreceivesimulate)", re.I)
LIFECYCLE = re.compile(r"(migrat|initialize|upgrade|^pause$|^unpause$|snapshot|rebase|blacklist|"
                       r"blocklist|freeze|whitelist|excludefrom|setmaxtx|setmaxwallet)", re.I)
MODIFIER = re.compile(r"(onlyowner|onlyrole|onlyadmin|onlyoperator|onlygovern|onlymanager|"
                      r"onlyminter|onlyauthor|auth\b|requiresauth|onlydao|onlyteam)", re.I)
CTRL = re.compile(r"(treasur|reserve|vault|pool|escrow|fund|bank)", re.I)
UPGRADE = re.compile(r"(setimplementation|upgradeto|setbeacon|changeimplementation|setlogic|"
                     r"setmaster|setcode)", re.I)
CONFIGISH = re.compile(r"^(set|update|change|config|enable|disable|toggle|add|remove|grant|revoke)", re.I)

def is_sig_gated(f):
    ins = f.get("inputs") or []
    names = " ".join((i.get("name") or "").lower() for i in ins)
    types = [i.get("type") for i in ins]
    if "bytes" in types and re.search(r"(sig|signature|proof|voucher)", names): return True
    if types.count("bytes32") >= 2 and "uint8" in types and re.search(r"\bv\b|\br\b|\bs\b", names): return True
    return False

def modifiers_of(src, fname):
    for m in re.finditer(r"function\s+" + re.escape(fname) + r"\s*\([^)]*\)([^{;]{0,200})[{;]", src):
        if MODIFIER.search(m.group(1)): return True
    return False

def load_source(blob):
    out = []
    for key in ("source", "impl_source"):
        s = (blob.get(key) or "").strip()
        if not s: continue
        if s.startswith("{"):
            try:
                j = json.loads(s[1:-1] if s.startswith("{{") else s)
                srcs = j.get("sources", j)
                for v in srcs.values():
                    if isinstance(v, dict) and "content" in v: out.append(v["content"])
            except Exception:
                out.append(s)
        else:
            out.append(s)
    return "\n".join(out)

def load_abi(blob):
    fns = []
    for key in ("abi", "impl_abi"):
        a = blob.get(key) or ""
        if not a or a.startswith("Contract source code not verified"): continue
        try:
            for it in json.loads(a):
                if it.get("type") == "function": fns.append(it)
        except Exception:
            pass
    seen, out = set(), []
    for f in fns:
        k = (f.get("name",""), len(f.get("inputs") or []))
        if k not in seen: seen.add(k); out.append(f)
    return out

def classify(blob):
    fns, src = load_abi(blob), load_source(blob)
    if not fns:
        return None
    fund, sig, admin_set, admin_move, permit, bridge, lifecycle, upgrade, admin_cfg = ([] for _ in range(9))
    for f in fns:
        n = f.get("name") or ""; ln = n.lower(); mut = f.get("stateMutability")
        if ln == "permit": permit.append(n); continue
        if ln in BOILER: continue
        if mut in ("view", "pure"): continue
        if FUND.search(n): fund.append(n)
        if is_sig_gated(f): sig.append(n)
        if ADMIN_SET.search(n): admin_set.append(n)
        if ADMIN_MOVE.search(n): admin_move.append(n)
        if BRIDGE.search(n): bridge.append(n)
        if LIFECYCLE.search(n) or re.match(r"^init", ln): lifecycle.append(n)
        if UPGRADE.search(n): upgrade.append(n)
        elif CONFIGISH.search(n) and not ADMIN_SET.search(n) and modifiers_of(src, n): admin_cfg.append(n)
    gated = sorted({n for n in set(admin_set+admin_move+lifecycle+bridge+upgrade) if modifiers_of(src, n)})
    nonstd = sorted(set(fund+sig+admin_set+admin_move+bridge+lifecycle+upgrade+admin_cfg))
    ctrl_ids = set()
    for f in fns:
        if CTRL.search(f.get("name") or ""): ctrl_ids.add(f["name"])
    for mm in re.finditer(r"address\s+(?:public|private|internal)\s+(?:immutable\s+|constant\s+)?(\w+)", src):
        if CTRL.search(mm.group(1)): ctrl_ids.add(mm.group(1))
    cats = [c for c, v in [("fund_ops", fund), ("sig_gated", sig),
        ("admin_treasury_pool_signer", admin_set), ("admin_token_mover", admin_move),
        ("bridge_ops", bridge), ("lifecycle_ops", lifecycle), ("proxy_upgrade", upgrade),
        ("admin_config_gated", admin_cfg)] if v]
    return {"keep": bool(nonstd), "total_functions": len(fns), "nonstandard_fn_count": len(nonstd),
        "keep_categories": "|".join(cats),
        "fund_fns": "|".join(sorted(set(fund))[:24]), "sig_gated_fns": "|".join(sorted(set(sig))[:10]),
        "has_eip2612_permit": bool(permit), "admin_setter_fns": "|".join(sorted(set(admin_set))[:16]),
        "admin_mover_fns": "|".join(sorted(set(admin_move))[:12]), "bridge_fns": "|".join(sorted(set(bridge))[:10]),
        "proxy_upgrade_fns": "|".join(sorted(set(upgrade))[:8]), "admin_config_fns": "|".join(sorted(set(admin_cfg))[:14]),
        "lifecycle_fns": "|".join(sorted(set(lifecycle))[:14]), "admin_only_confirmed": "|".join(gated[:16]),
        "controls_reserve_treasury_pool_vault": bool(ctrl_ids),
        "reserve_identifiers": "|".join(sorted(ctrl_ids)[:12]),
        "source_norm_hash": hashlib.sha256(re.sub(r"\s+", "", src).encode()[:200000]).hexdigest()[:16] if src else ""}

# ---- Etherscan V2 helpers ----
def es(params, tries=5):
    p = dict(params); p["apikey"] = KEY; p["chainid"] = CHAINID
    for t in range(tries):
        try:
            r = requests.get(ES, params=p, timeout=40, headers=H)
            if r.status_code == 200:
                d = r.json()
                if "rate limit" in str(d.get("result", "")).lower():
                    time.sleep(1.2 * (t + 1)); continue
                time.sleep(0.22); return d
            time.sleep(1.2 * (t + 1))
        except Exception:
            time.sleep(1.2 * (t + 1))
    return None

def get_source(addr):
    d = es(dict(module="contract", action="getsourcecode", address=addr))
    if isinstance(d, dict) and str(d.get("status")) == "1":
        return (d.get("result") or [{}])[0]
    return None

# On Base/BSC the free key blocks proxy/eth_getCode and getcontractcreation
# ("not supported for this chain"); ETH/Arbitrum allow both. A public RPC recovers
# bytecode (=> EIP-1167 detection + fingerprint) on Base; deployer stays unavailable
# there and is reported as such rather than guessed.
RPCS = {"eth": ["https://eth.llamarpc.com", "https://ethereum.publicnode.com", "https://rpc.ankr.com/eth"],
        "arbitrum": ["https://arbitrum.llamarpc.com", "https://arbitrum-one.publicnode.com", "https://rpc.ankr.com/arbitrum"],
        "base": ["https://mainnet.base.org", "https://base.publicnode.com", "https://base.llamarpc.com"]}[CHAIN]

def rpc_getcode(addr):
    for url in RPCS:
        try:
            r = requests.post(url, timeout=20, headers=H,
                json={"jsonrpc": "2.0", "id": 1, "method": "eth_getCode", "params": [addr, "latest"]})
            v = (r.json() or {}).get("result")
            if isinstance(v, str) and v.startswith("0x") and len(v) > 4:
                return v
        except Exception:
            continue
    return None

def get_code(addr):
    d = es(dict(module="proxy", action="eth_getCode", address=addr, tag="latest"))
    if isinstance(d, dict):
        r = d.get("result")
        if isinstance(r, str) and r.startswith("0x") and len(r) > 4:
            return r
    return rpc_getcode(addr)  # Base fallback

def get_creation(addr):
    d = es(dict(module="contract", action="getcontractcreation", contractaddresses=addr))
    if isinstance(d, dict) and str(d.get("status")) == "1":
        res = d.get("result")
        if isinstance(res, list) and res and isinstance(res[0], dict):
            return res[0]
    return None  # blocked on Base -> deployer unavailable, reported honestly

EIP1167 = re.compile(r"^0x363d3d373d3d3d363d73([0-9a-f]{40})5af43d82803e903d91602b57fd5bf3", re.I)
# push0 / vyper / newer minimal-proxy variants seen in the wild
EIP1167_V2 = re.compile(r"363d3d373d3d3d363d73([0-9a-f]{40})5af43d82803e903d91602b57fd5bf3", re.I)

def strip_metadata(code):
    """Strip Solidity CBOR metadata trailer so identical-source contracts hash equal."""
    h = code[2:] if code.startswith("0x") else code
    try:
        L = int(h[-4:], 16) * 2  # last 2 bytes = CBOR length
        if 0 < L < len(h) - 4:
            return h[:-(L + 4)]
    except Exception:
        pass
    return h

def bytecode_fingerprint(code):
    if not code or len(code) < 6:
        return "", 0, None, False
    stripped = strip_metadata(code)
    fp = hashlib.sha256(stripped.encode()).hexdigest()[:16]
    runtime_bytes = (len(code) - 2) // 2
    m = EIP1167.match(code) or EIP1167_V2.search(code[:120])
    impl_1167 = ("0x" + m.group(1)) if m else None
    is_min = impl_1167 is not None
    return fp, runtime_bytes, impl_1167, is_min

def goplus(addr, tries=3):
    # public tier is rate-limited; retry on 429/empty so flags are not silently blanked
    for t in range(tries):
        try:
            r = requests.get(f"https://api.gopluslabs.io/api/v1/token_security/{CHAINID}",
                             params={"contract_addresses": addr}, timeout=30, headers=H)
            if r.status_code == 200:
                res = ((r.json() or {}).get("result") or {}).get(addr.lower())
                if res:
                    return res
                time.sleep(1.5 * (t + 1)); continue
            if r.status_code == 429:
                time.sleep(3 * (t + 1)); continue
        except Exception:
            time.sleep(1.5 * (t + 1))
    return None

# ---- build candidate set from qualifying pairs ----
d = json.load(open(f"{DATA}/ds_qualifying_{CHAIN}.json"))
qual, profiles = d["qualifying"], d.get("profiles", {})
by_token = {}
for p in qual:
    a = p["baseToken"]["address"].lower()
    if a in MAJORS: continue
    e = by_token.setdefault(a, {"best": p, "n": 0}); e["n"] += 1
    if p["_liq_usd"] > e["best"]["_liq_usd"]: e["best"] = p
print(f"[{CHAIN}] distinct candidate projects (majors excluded): {len(by_token)}")

results, unverified = [], []
for i, (addr, e) in enumerate(sorted(by_token.items(), key=lambda kv: -kv[1]["best"]["_liq_usd"])):
    p = e["best"]; tok = p["baseToken"]["address"]
    info = p.get("info") or {}
    sites = [w.get("url") for w in (info.get("websites") or []) if w.get("url")]
    socials = [s.get("url") for s in (info.get("socials") or []) if s.get("url")]
    for l in (profiles.get(addr, {}).get("links") or []):
        u = l.get("url")
        if u: (sites if (l.get("label") or "").lower() == "website" else socials).append(u)

    sc = get_source(tok)
    code = get_code(tok)
    fp, rt_bytes, impl_1167, is_min = bytecode_fingerprint(code or "")
    creation = get_creation(tok)
    deployer = (creation or {}).get("contractCreator", "")

    base = {"chain": CHAIN, "name": p["baseToken"].get("name") or "", "symbol": p["baseToken"].get("symbol") or "",
        "token_address": tok, "pair_address": p["pairAddress"],
        "liquidity_usd": round(p["_liq_usd"], 2), "age_days": round(p["_age_days"], 1),
        "dex": p.get("dexId"), "quote": (p.get("quoteToken") or {}).get("symbol"),
        "vol24h_usd": round(float((p.get("volume") or {}).get("h24") or 0), 2),
        "fdv_usd": p.get("fdv"), "qualifying_pairs": e["n"],
        "websites": " ; ".join(dict.fromkeys(sites)), "socials": " ; ".join(dict.fromkeys(socials)),
        "dexscreener_url": p.get("url"), "runtime_bytecode_bytes": rt_bytes,
        "bytecode_fp": fp, "deployer": deployer,
        "creation_block": (creation or {}).get("blockNumber", "")}

    if sc is None:
        unverified.append({**base, "reason": "getsourcecode failed / no response"});
        if i % 15 == 0: print(f"  {i}/{len(by_token)}", flush=True)
        continue
    verified = bool(sc.get("SourceCode"))
    is_proxy = str(sc.get("Proxy")) == "1"
    impl = (sc.get("Implementation") or "").strip() or impl_1167 or ""
    cname = sc.get("ContractName") or ""
    blob = {"abi": sc.get("ABI") or "", "source": sc.get("SourceCode") or "", "impl_abi": "", "impl_source": ""}
    impl_verified = None; impl_cname = ""
    if impl and impl.lower() != "0x" + "0"*40:
        di = get_source(impl)
        if di:
            ia = di.get("ABI") or ""
            impl_verified = bool(di.get("SourceCode")) and not ia.startswith("Contract source code not verified")
            impl_cname = di.get("ContractName") or ""
            blob["impl_abi"] = ia; blob["impl_source"] = di.get("SourceCode") or ""

    cls = classify(blob)
    proxy_kind = ("eip1967" if is_proxy else ("eip1167_minimal_clone" if is_min else ""))
    if cls is None:
        unverified.append({**base, "verified": verified, "is_proxy": is_proxy or is_min,
            "proxy_kind": proxy_kind, "implementation": impl, "contract_name": cname,
            "reason": "no verified ABI on proxy or implementation" if (is_proxy or is_min) else "source not verified"})
    else:
        results.append({**base, **cls, "contract_name": cname, "compiler": sc.get("CompilerVersion"),
            "is_proxy": is_proxy or is_min, "proxy_kind": proxy_kind,
            "implementation": impl, "impl_verified": impl_verified, "impl_contract_name": impl_cname,
            "minimal_proxy_clone": is_min, "verified": verified})
    if i % 15 == 0:
        print(f"  {i}/{len(by_token)} -> kept {sum(1 for r in results if r.get('keep'))}", flush=True)

# ---- family signals across this chain (implementation / deployer / bytecode / source) ----
def tally(key):
    c = {}
    for r in results:
        v = (r.get(key) or "")
        if v: c[v.lower()] = c.get(v.lower(), 0) + 1
    return c
impl_ct, dep_ct, bc_ct, src_ct = tally("implementation"), tally("deployer"), tally("bytecode_fp"), tally("source_norm_hash")
for r in results:
    r["impl_shared_by_n"] = impl_ct.get((r.get("implementation") or "").lower(), 0)
    r["deployer_shared_by_n"] = dep_ct.get((r.get("deployer") or "").lower(), 0)
    r["bytecode_shared_by_n"] = bc_ct.get((r.get("bytecode_fp") or "").lower(), 0)
    r["source_shared_by_n"] = src_ct.get((r.get("source_norm_hash") or "").lower(), 0)

# ---- GoPlus flags for the kept set only ----
kept = [r for r in results if r.get("keep")]
print(f"[{CHAIN}] GoPlus on {len(kept)} kept tokens...")
for j, r in enumerate(kept):
    g = goplus(r["token_address"]) or {}
    flags = []
    if str(g.get("is_honeypot")) == "1": flags.append("HONEYPOT")
    if str(g.get("is_mintable")) == "1": flags.append("mintable")
    if str(g.get("transfer_pausable")) == "1": flags.append("pausable")
    if str(g.get("hidden_owner")) == "1": flags.append("hidden_owner")
    if str(g.get("can_take_back_ownership")) == "1": flags.append("reclaimable_ownership")
    if str(g.get("selfdestruct")) == "1": flags.append("selfdestruct")
    if str(g.get("external_call")) == "1": flags.append("external_call")
    try:
        op = float(g.get("owner_percent") or 0)
        if op >= 0.5: flags.append(f"owner_holds_{op*100:.0f}pct")
    except Exception: pass
    r["holder_count"] = g.get("holder_count"); r["lp_holder_count"] = g.get("lp_holder_count")
    r["goplus_flags"] = "|".join(flags); r["goplus_ok"] = bool(g)
    time.sleep(1.4)

json.dump({"chain": CHAIN, "results": results, "unverified": unverified},
          open(f"{DATA}/analysis_{CHAIN}.json", "w"), indent=1)
print(f"\n[{CHAIN}] analyzed {len(results)} | unverified/no-ABI {len(unverified)} | KEPT {len(kept)}")
print(f"  proxies in kept: {sum(1 for r in kept if r['is_proxy'])} | "
      f"minimal clones: {sum(1 for r in kept if r['minimal_proxy_clone'])} | "
      f"controls reserve/vault: {sum(1 for r in kept if r['controls_reserve_treasury_pool_vault'])}")
print(f"  shared-impl (n>1): {sum(1 for r in kept if r['impl_shared_by_n']>1)} | "
      f"shared-deployer (n>1): {sum(1 for r in kept if r['deployer_shared_by_n']>1)} | "
      f"shared-bytecode (n>1): {sum(1 for r in kept if r['bytecode_shared_by_n']>1)}")
