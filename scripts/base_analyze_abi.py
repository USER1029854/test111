"""Parse verified ABIs and keep only tokens with real fund-handling / privileged surface.

Reuses the exact regex taxonomy from the BSC template's analyze_abi.py (FUND,
ADMIN_SET, ADMIN_MOVE, BRIDGE, LIFECYCLE, MODIFIER, CTRL, UPGRADE, CONFIGISH) --
this is the operationalization of "custom logic vs plain token" and is not
re-tuned per chain. Two extra notes specific to this pass:

  * ABIs do not encode access-control modifiers, so admin-only status is confirmed
    by locating the function declaration in the verified source and reading its
    modifiers.
  * For proxies the proxy's own ABI is a shell, so the implementation ABI is merged
    in before classification, and the EIP-1967 admin/impl slots are read from a
    public Base RPC. EIP-1167 minimal-proxy clone detection is folded directly into
    this script (via eth_getCode + bytecode pattern match) rather than left as an
    unsaved ad hoc step, since Base's launchpad/"clanker"-style culture makes clone
    families a first-class thing to look for here.
"""
import json, re, csv, os, requests, time

DATA = "/home/user/test111/data"
CDIR = "/tmp/claude-0/-home-user-test111/958631bf-a002-5f41-98f2-bf8502fbeec3/scratchpad/contracts_base"

# Plain ERC-20 surface + ownership boilerplate. Nothing here is "fund handling".
STD = {"name","symbol","decimals","totalsupply","balanceof","transfer","transferfrom",
       "approve","allowance","increaseallowance","decreaseallowance","getowner","owner",
       "renounceownership","transferownership","domain_separator","nonces","eip712domain",
       "version","paused","supportsinterface","implementation","admin"}

# Ownership/allowance boilerplate present on nearly every token -- never a keep trigger.
BOILER = {"approve","transfer","transferfrom","increaseallowance","decreaseallowance",
          "renounceownership","transferownership"}

FUND = re.compile(r"(claim|mint|burn|recycl|releas|reward|harvest|stak|unstak|deposit|"
                  r"withdraw|redeem|vault|distribut|settle)", re.I)
# owner-only setters for a treasury/pool/signer-equivalent address. setPeer/setDelegate
# are included: on a LayerZero OFT the peer is the address authorised to mint locally.
ADMIN_SET = re.compile(r"^set.*(treasur|reserve|pool|vault|signer|fee|router|receiver|wallet|"
                       r"operator|admin|manager|minter|oracle|bridge|market|dev|tax|swap|pair|"
                       r"liquid|fund|collector|beneficiar|peer|delegate|inspector|precrime|"
                       r"enforcedoption|trusted|remote|endpoint)", re.I)
ADMIN_MOVE = re.compile(r"(rescue|sweep|recover|salvage|emergenc|airdrop|seize|withdrawstuck|"
                        r"clearstuck|takeout|transferany|forcetransfer|admintransfer|"
                        r"withdrawtoken|withdrawerc20|drain)", re.I)
# cross-chain movement: an OFT send()/lzReceive() debits or credits real balance.
BRIDGE = re.compile(r"^(send|sendfrom|lzreceive|bridge|crosschain|teleport|relay|"
                    r"lzreceiveandrevert|lzreceivesimulate)", re.I)
# privileged lifecycle control: halts, converts or re-points the token.
LIFECYCLE = re.compile(r"(migrat|initialize|upgrade|^pause$|^unpause$|snapshot|rebase|"
                       r"blacklist|blocklist|freeze|whitelist|excludefrom|setmaxtx|setmaxwallet)", re.I)
MODIFIER = re.compile(r"(onlyowner|onlyrole|onlyadmin|onlyoperator|onlygovern|onlymanager|"
                      r"onlyminter|onlyauthor|auth\b|requiresauth|onlydao|onlyteam)", re.I)
CTRL = re.compile(r"(treasur|reserve|vault|pool|escrow|fund|bank)", re.I)
# owner can swap the whole logic contract -- the single most privileged thing a token can expose
UPGRADE = re.compile(r"(setimplementation|upgradeto|setbeacon|changeimplementation|setlogic|"
                     r"setmaster|setcode)", re.I)
# generic privileged config: any set/update/change fn CONFIRMED owner-gated in the source,
# which catches launchpad-clone setters (setMode, init) that no keyword list would predict
CONFIGISH = re.compile(r"^(set|update|change|config|enable|disable|toggle|add|remove|grant|revoke)", re.I)

def load_source(blob):
    """SourceCode is plain text, {..} json, or {{..}} standard-json multi-file."""
    out = []
    for key in ("source", "impl_source"):
        s = blob.get(key) or ""
        if not s: continue
        t = s.strip()
        if t.startswith("{"):
            try:
                j = json.loads(t[1:-1] if t.startswith("{{") else t)
                srcs = j.get("sources", j)
                for v in srcs.values():
                    if isinstance(v, dict) and "content" in v:
                        out.append(v["content"])
            except Exception:
                out.append(s)
        else:
            out.append(s)
    return "\n".join(out)

def load_abi(blob):
    fns = []
    for key in ("abi", "impl_abi"):
        a = blob.get(key) or ""
        if not a or a.startswith("Contract source code not verified"):
            continue
        try:
            for it in json.loads(a):
                if it.get("type") == "function":
                    fns.append(it)
        except Exception:
            pass
    # dedupe by name+arity
    seen, out = set(), []
    for f in fns:
        k = (f.get("name",""), len(f.get("inputs") or []))
        if k not in seen:
            seen.add(k); out.append(f)
    return out

def is_sig_gated(f):
    ins = f.get("inputs") or []
    names = " ".join((i.get("name") or "").lower() for i in ins)
    types = [i.get("type") for i in ins]
    if "bytes" in types and re.search(r"(sig|signature|proof|voucher)", names):
        return True
    if types.count("bytes32") >= 2 and "uint8" in types and re.search(r"\bv\b|\br\b|\bs\b", names):
        return True
    return False

def modifiers_of(src, fname):
    for m in re.finditer(r"function\s+" + re.escape(fname) + r"\s*\([^)]*\)([^{;]{0,200})[{;]", src):
        if MODIFIER.search(m.group(1)):
            return True
    return False

# --- EIP-1967 slots + EIP-1167 clone bytecode via public Base RPC ---
# (BaseScan proxy module is blocked on this key, same restriction as BSC)
RPCS = ["https://mainnet.base.org", "https://base.llamarpc.com", "https://base.publicnode.com"]
RH = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
SLOT_ADMIN = "0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103"
SLOT_IMPL  = "0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc"
SLOT_BEACON = "0xa3f0ad74e5423aebfd80d3ef4346578335a9a72aeaee59ff6cb3582b35133d50"
# getRoleMember(DEFAULT_ADMIN_ROLE, 0) -- some proxies use AccessControl, not Ownable,
# so owner() reverts and the real upgrade authority is the admin-role holder.
ROLE_MEMBER_CALL = "0x9010d07c" + "0" * 64 + "0" * 64

def raw_call(addr, data):
    for url in RPCS:
        try:
            r = requests.post(url, timeout=15, headers=RH, json={"jsonrpc":"2.0","id":1,"method":"eth_call",
                "params":[{"to": addr, "data": data}, "latest"]})
            v = r.json().get("result")
            if v and len(v) >= 66:
                a = "0x" + v[-40:]
                return None if int(a, 16) == 0 else a
        except Exception:
            continue
    return None

FN_SELECTORS = {"implementation": "0x5c60da1b", "getImplementation": "0xaaf10f42",
                "owner": "0x8da5cb5b"}

def eth_call(addr, fname):
    sel = FN_SELECTORS.get(fname)
    if not sel: return None
    for url in RPCS:
        try:
            r = requests.post(url, timeout=15, headers=RH, json={"jsonrpc":"2.0","id":1,"method":"eth_call",
                "params":[{"to": addr, "data": sel}, "latest"]})
            v = r.json().get("result")
            if v and len(v) >= 66:
                a = "0x" + v[-40:]
                return None if int(a, 16) == 0 else a
        except Exception:
            continue
    return None

def storage(addr, slot):
    for url in RPCS:
        try:
            r = requests.post(url, timeout=15, headers=RH, json={"jsonrpc":"2.0","id":1,
                "method":"eth_getStorageAt","params":[addr, slot, "latest"]})
            v = r.json().get("result")
            if v and isinstance(v, str) and len(v) == 66:
                a = "0x" + v[-40:]
                return None if int(a, 16) == 0 else a
        except Exception:
            continue
    return None

EIP1167_PREFIX = "363d3d373d3d3d363d73"
EIP1167_SUFFIX = "5af43d82803e903d91602b57fd5bf3"

def get_code(addr):
    for url in RPCS:
        try:
            r = requests.post(url, timeout=15, headers=RH, json={"jsonrpc":"2.0","id":1,
                "method":"eth_getCode","params":[addr, "latest"]})
            v = r.json().get("result")
            if v and v != "0x":
                return v
        except Exception:
            continue
    return None

def detect_eip1167(code_hex):
    """EIP-1167 minimal proxy runtime is a fixed 45-byte template with the
    implementation address spliced in the middle. Vanity CREATE2 clone
    addresses (e.g. a `...7777` suffix) come from salt-mining, not custom
    bytecode, so the fixed prefix/suffix match still applies."""
    if not code_hex: return None
    c = code_hex[2:].lower() if code_hex.startswith("0x") else code_hex.lower()
    if len(c) == 90 and c.startswith(EIP1167_PREFIX) and c.endswith(EIP1167_SUFFIX):
        return "0x" + c[20:60]
    return None

meta = json.load(open(f"{DATA}/base_contract_meta.json"))["meta"]
rows = list(csv.DictReader(open(f"{DATA}/base_new_projects.csv")))
by_addr = {r["token_address"].lower(): r for r in rows}
print(f"tokens in scope: {len(rows)}")

# EIP-1167 clone check runs for EVERY token regardless of Etherscan's own Proxy
# flag -- that flag does not reliably catch minimal-proxy clones (this is why
# the BSC run needed a separate bytecode pass; folded in here so it's captured
# in a saved script this time).
clones = {}
for i, addr in enumerate(by_addr):
    code = get_code(by_addr[addr]["token_address"])
    impl = detect_eip1167(code)
    if impl:
        clones[addr] = impl
    if i % 25 == 0:
        print(f"  eth_getCode clone scan {i}/{len(by_addr)} -> {len(clones)} EIP-1167 clones so far", flush=True)
    time.sleep(0.08)
print(f"EIP-1167 minimal-proxy clones detected: {len(clones)}")
json.dump(clones, open(f"{DATA}/base_minimal_proxies.json", "w"), indent=1)

results, unverified = [], []
for addr, m in meta.items():
    base = by_addr.get(addr)
    if not base: continue
    if not m["verified"]:
        unverified.append({**base, "reason": "source not verified - ABI unavailable"})
        continue
    blob = json.load(open(f"{CDIR}/{addr}.json"))
    fns = load_abi(blob)
    src = load_source(blob)
    if not fns:
        unverified.append({**base, "reason": "verified flag set but ABI unparseable/empty"})
        continue

    fund, sig, admin_set, admin_move, permit, bridge, lifecycle = [], [], [], [], [], [], []
    upgrade, admin_cfg = [], []
    for f in fns:
        n = f.get("name") or ""
        ln = n.lower()
        mut = f.get("stateMutability")
        if ln == "permit":
            permit.append(n); continue
        if ln in BOILER:
            continue
        # a view/pure function cannot move funds or change privilege -- constants like
        # ALLOC_STAKING_REWARD were otherwise being scored as staking logic.
        if mut in ("view", "pure"):
            continue
        if FUND.search(n): fund.append(n)
        if is_sig_gated(f): sig.append(n)
        if ADMIN_SET.search(n): admin_set.append(n)
        if ADMIN_MOVE.search(n): admin_move.append(n)
        if BRIDGE.search(n): bridge.append(n)
        if LIFECYCLE.search(n) or re.match(r"^init", ln): lifecycle.append(n)
        if UPGRADE.search(n): upgrade.append(n)
        elif CONFIGISH.search(n) and not ADMIN_SET.search(n) and modifiers_of(src, n):
            admin_cfg.append(n)

    # admin-only confirmation from source modifiers
    gated = sorted({n for n in set(admin_set + admin_move + lifecycle + bridge + upgrade) if modifiers_of(src, n)})
    nonstd = sorted(set(fund + sig + admin_set + admin_move + bridge + lifecycle + upgrade + admin_cfg))
    keep = bool(nonstd)

    # controlled reserve/treasury/pool/vault
    ctrl_ids = set()
    for f in fns:
        if CTRL.search(f.get("name") or ""): ctrl_ids.add(f["name"])
    for mm in re.finditer(r"address\s+(?:public|private|internal)\s+(?:immutable\s+|constant\s+)?(\w+)", src):
        if CTRL.search(mm.group(1)): ctrl_ids.add(mm.group(1))

    impl = m.get("implementation")
    admin_slot = None
    custom_proxy = bool(upgrade)
    if custom_proxy and not impl:
        for f in fns:
            if (f.get("name") or "").lower() in ("implementation", "getimplementation") \
               and f.get("stateMutability") in ("view", "pure"):
                impl = eth_call(base["token_address"], f["name"]); break
    upgrade_authority, auth_src = "", ""
    is_eip1167 = addr in clones
    if m["is_proxy"] or custom_proxy or is_eip1167:
        admin_slot = storage(base["token_address"], SLOT_ADMIN)
        if not impl:
            impl = storage(base["token_address"], SLOT_IMPL)
        if not impl and is_eip1167:
            impl = clones[addr]
        # An empty EIP-1967 admin slot usually means UUPS/Ownable rather than a
        # transparent ProxyAdmin, so upgrade authority is owner() instead.
        beacon = storage(base["token_address"], SLOT_BEACON)
        upgrade_authority = admin_slot or ""
        auth_src = "eip1967_admin_slot" if admin_slot else ""
        if not upgrade_authority:
            o = eth_call(base["token_address"], "owner")
            if o: upgrade_authority, auth_src = o, "owner()"
        if not upgrade_authority:
            ra = raw_call(base["token_address"], ROLE_MEMBER_CALL)
            if ra: upgrade_authority, auth_src = ra, "DEFAULT_ADMIN_ROLE holder"
        if beacon:
            auth_src = (auth_src + " | beacon " + beacon).strip(" |")

    results.append({
        "name": base["name"], "symbol": base["symbol"], "token_address": base["token_address"],
        "pair_address": base["pair_address"], "liquidity_usd": base["liquidity_usd"],
        "age_days": base["age_days"], "dex": base["dex"], "quote": base["quote"],
        "websites": base["websites"], "socials": base["socials"],
        "contract_name": m.get("contract_name"), "total_functions": len(fns),
        "keep": keep,
        "fund_fns": "|".join(sorted(set(fund))[:24]),
        "sig_gated_fns": "|".join(sorted(set(sig))[:10]),
        "has_eip2612_permit": bool(permit),
        "admin_setter_fns": "|".join(sorted(set(admin_set))[:16]),
        "admin_mover_fns": "|".join(sorted(set(admin_move))[:12]),
        "bridge_fns": "|".join(sorted(set(bridge))[:10]),
        "proxy_upgrade_fns": "|".join(sorted(set(upgrade))[:8]),
        "admin_config_fns": "|".join(sorted(set(admin_cfg))[:14]),
        "lifecycle_fns": "|".join(sorted(set(lifecycle))[:14]),
        "admin_only_confirmed": "|".join(gated[:16]),
        "keep_categories": "|".join([c for c, v in [("fund_ops", fund), ("sig_gated", sig),
            ("admin_treasury_pool_signer", admin_set), ("admin_token_mover", admin_move),
            ("bridge_ops", bridge), ("lifecycle_ops", lifecycle),
            ("proxy_upgrade", upgrade), ("admin_config_gated", admin_cfg)] if v]),
        "nonstandard_fn_count": len(nonstd),
        "controls_reserve_treasury_pool_vault": bool(ctrl_ids),
        "reserve_identifiers": "|".join(sorted(ctrl_ids)[:12]),
        "is_proxy": m["is_proxy"] or custom_proxy or is_eip1167,
        "proxy_kind": ("eip1167_clone" if is_eip1167 else ("eip1967" if m["is_proxy"] else
                       ("custom_setImplementation" if custom_proxy else ""))),
        "implementation": impl or "",
        "proxy_admin": admin_slot or "",
        "upgrade_authority": upgrade_authority,
        "upgrade_authority_src": auth_src or "unresolved", "impl_verified": m.get("impl_verified"),
        "holder_count": base.get("holder_count"), "risk_flags": base.get("risk_flags"),
    })

json.dump({"results": results, "unverified": unverified}, open(f"{DATA}/base_abi_analysis.json","w"), indent=1)
kept = [r for r in results if r["keep"]]
drop = [r for r in results if not r["keep"]]
print(f"\nverified & analyzed : {len(results)}")
print(f"unverified/no ABI   : {len(unverified)}")
print(f"KEPT (fund/priv fns): {len(kept)}")
print(f"DROPPED (plain)     : {len(drop)}")
print(f"proxies in kept set : {sum(1 for r in kept if r['is_proxy'])}")
print(f"kept w/ reserve ref : {sum(1 for r in kept if r['controls_reserve_treasury_pool_vault'])}")
