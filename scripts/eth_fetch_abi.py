"""Fetch verified ABI + source for the kept Ethereum token set.

Not a re-discovery: the token list is read from eth_new_projects.csv and never
changes. classify.py discarded the ABI/Proxy/Implementation fields, so they are
pulled once here. Proxies get their implementation fetched too, because a proxy's
own ABI is usually a near-empty shell and the real surface lives behind it.
"""
import requests, json, csv, time, os

KEY = "R6PYYNEX4CNFAXX4YX3K8W4NXSBGGG4QGJ"
H = {"User-Agent": "Mozilla/5.0"}
OUT = "/tmp/claude-0/-home-user-test111/958631bf-a002-5f41-98f2-bf8502fbeec3/scratchpad/contracts"
DATA = "/home/user/test111/data"
os.makedirs(OUT, exist_ok=True)

def src(addr, tries=4):
    for t in range(tries):
        try:
            r = requests.get("https://api.etherscan.io/v2/api", timeout=40, headers=H,
                             params=dict(chainid=1, module="contract", action="getsourcecode",
                                         address=addr, apikey=KEY))
            if r.status_code == 200:
                d = r.json()
                if str(d.get("status")) == "1":
                    return (d.get("result") or [{}])[0]
                if "rate limit" in str(d.get("result", "")).lower():
                    time.sleep(2 * (t + 1)); continue
                return {"__err": str(d.get("result"))[:120]}
            time.sleep(1.5 * (t + 1))
        except Exception as e:
            time.sleep(1.5 * (t + 1))
    return None

rows = list(csv.DictReader(open(f"{DATA}/eth_new_projects.csv")))
print(f"tokens in CSV: {len(rows)}")
meta, fails, nproxy = {}, [], 0

for i, r in enumerate(rows):
    a = r["token_address"]
    d = src(a)
    if d is None or d.get("__err"):
        fails.append({"token": a, "symbol": r["symbol"], "why": (d or {}).get("__err", "no response")})
        print(f"  FAIL {r['symbol']}: {(d or {}).get('__err','no response')}", flush=True)
        time.sleep(0.25); continue

    abi_raw = d.get("ABI") or ""
    verified = bool(d.get("SourceCode")) and not abi_raw.startswith("Contract source code not verified")
    is_proxy = str(d.get("Proxy")) == "1"
    impl = (d.get("Implementation") or "").strip()

    rec = {"token": a, "symbol": r["symbol"], "name": r["name"],
           "contract_name": d.get("ContractName"), "verified": verified,
           "is_proxy": is_proxy, "implementation": impl or None,
           "compiler": d.get("CompilerVersion"), "impl_verified": None}

    blob = {"abi": abi_raw, "source": d.get("SourceCode") or "", "impl_abi": "", "impl_source": ""}

    if is_proxy and impl and impl != "0x" + "0" * 40:
        nproxy += 1
        time.sleep(0.25)
        di = src(impl)
        if di and not di.get("__err"):
            ia = di.get("ABI") or ""
            rec["impl_verified"] = bool(di.get("SourceCode")) and not ia.startswith("Contract source code not verified")
            rec["impl_contract_name"] = di.get("ContractName")
            blob["impl_abi"] = ia
            blob["impl_source"] = di.get("SourceCode") or ""
        else:
            rec["impl_verified"] = False

    json.dump(blob, open(f"{OUT}/{a.lower()}.json", "w"))
    meta[a.lower()] = rec
    if i % 20 == 0:
        print(f"  {i}/{len(rows)} fetched", flush=True)
    time.sleep(0.25)

json.dump({"meta": meta, "fails": fails}, open(f"{DATA}/eth_contract_meta.json", "w"), indent=1)
print(f"\nfetched {len(meta)}/{len(rows)} | verified {sum(1 for v in meta.values() if v['verified'])}"
      f" | proxies {nproxy} | failures {len(fails)}")
