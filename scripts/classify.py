"""Phase 3: safety-check + junk filter, then emit the table and CSV.

Filter posture is deliberately loose, per the brief: a token is only dropped on
an unambiguous signal (confirmed honeypot, unsellable tax, or meme-name with zero
web presence). Anything uncertain is KEPT and flagged. Failed checks are recorded
as failures -- never silently treated as a pass, never fabricated.
"""
import requests, json, time, csv, re, os

H = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
KEY = "R6PYYNEX4CNFAXX4YX3K8W4NXSBGGG4QGJ"
DATA = "/home/user/test111/data"

MAJORS = {a.lower() for a in [
 "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c","0x55d398326f99059fF775485246999027B3197955",
 "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d","0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c",
 "0x2170Ed0880ac9A755fd29B2688956BD959F933F8","0xc5f0f7b66764F6ec8C8Dff7BA683102295E16409",
 "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56","0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82",
 "0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3","0xfb6115445Bff7b52FeB98650C87f44907E58f802",
 "0x3d4350cD54aeF9f9b2C29435e0fa809957B3F30a","0x14016E85a25aeb13065688cAFB43044C2ef86784"]}

MEME_KW = re.compile(r"(doge|shib|inu|pepe|wojak|elon|moon|floki|bonk|chad|giga|"
                     r"baby|safe|cum|cat\b|kitty|frog|meme|troll|retard|tard|"
                     r"pump|rocket|lambo|ape\b|banana|monkey|clown|poo|shit|"
                     r"trump|biden|milady|mog|brett|andy|turbo|wif\b|hat\b)", re.I)

def get(url, params=None, tries=3, pause=0.25):
    for t in range(tries):
        try:
            r = requests.get(url, params=params, timeout=30, headers=H)
            if r.status_code == 200:
                time.sleep(pause); return r.json()
            if r.status_code == 429:
                time.sleep(5 * (t + 1)); continue
            time.sleep(1.2 * (t + 1))
        except Exception:
            time.sleep(1.2 * (t + 1))
    return None

d = json.load(open(f"{DATA}/ds_qualifying.json"))
qual, profiles = d["qualifying"], d.get("profiles", {})
print(f"qualifying pairs from DEXScreener: {len(qual)}")

# one row per TOKEN -> its highest-liquidity qualifying pair
by_token = {}
for p in qual:
    a = p["baseToken"]["address"].lower()
    if a in MAJORS:
        continue
    e = by_token.setdefault(a, {"best": p, "n": 0})
    e["n"] += 1
    if p["_liq_usd"] > e["best"]["_liq_usd"]:
        e["best"] = p
print(f"distinct candidate projects (majors excluded): {len(by_token)}")

rows = []
for i, (addr, e) in enumerate(sorted(by_token.items(), key=lambda kv: -kv[1]["best"]["_liq_usd"])):
    p = e["best"]
    info = p.get("info") or {}
    sites = [w.get("url") for w in (info.get("websites") or []) if w.get("url")]
    socials = [s.get("url") for s in (info.get("socials") or []) if s.get("url")]
    pr = profiles.get(addr) or {}
    for l in (pr.get("links") or []):
        u = l.get("url")
        if not u: continue
        (sites if (l.get("label") or "").lower() == "website" else socials).append(u)
    sites, socials = list(dict.fromkeys(sites)), list(dict.fromkeys(socials))

    # --- honeypot.is ---
    hp = get("https://api.honeypot.is/v2/IsHoneypot",
             {"address": p["baseToken"]["address"], "chainID": 56}, pause=0.3)
    if hp is None:
        hpd = {"ok": False}
    else:
        hr, sr, sm = hp.get("honeypotResult") or {}, hp.get("simulationResult") or {}, hp.get("summary") or {}
        cc = hp.get("contractCode") or {}
        hpd = {"ok": True, "isHoneypot": hr.get("isHoneypot"),
               "risk": sm.get("risk"), "riskLevel": sm.get("riskLevel"),
               "flags": [f.get("flag") if isinstance(f, dict) else f for f in (sm.get("flags") or [])],
               "buyTax": sr.get("buyTax"), "sellTax": sr.get("sellTax"),
               "transferTax": sr.get("transferTax"),
               "openSource": cc.get("openSource"),
               "simOk": hp.get("simulationSuccess")}

    # --- BscScan source verification (only module the supplied key allows) ---
    sc = get("https://api.etherscan.io/v2/api",
             dict(chainid=56, module="contract", action="getsourcecode",
                  address=p["baseToken"]["address"], apikey=KEY), pause=0.22)
    verified, cname = None, None
    if sc and str(sc.get("status")) == "1":
        r0 = (sc.get("result") or [{}])[0]
        verified, cname = bool(r0.get("SourceCode")), r0.get("ContractName") or None

    name = p["baseToken"].get("name") or ""
    sym = p["baseToken"].get("symbol") or ""
    has_web, has_soc = bool(sites), bool(socials)
    memeish = bool(MEME_KW.search(f"{name} {sym}"))

    drop, why = False, []
    if hpd.get("ok") and hpd.get("isHoneypot") is True:
        drop = True; why.append("honeypot.is: confirmed honeypot")
    st = hpd.get("sellTax")
    if isinstance(st, (int, float)) and st >= 50:
        drop = True; why.append(f"sell tax {st:.0f}%")
    if memeish and not has_web and not has_soc:
        drop = True; why.append("meme-style name, no website/socials")

    rows.append({
        "name": name, "symbol": sym,
        "token_address": p["baseToken"]["address"], "pair_address": p["pairAddress"],
        "liquidity_usd": round(p["_liq_usd"], 2), "age_days": round(p["_age_days"], 1),
        "dex": p.get("dexId"), "labels": "|".join(p.get("labels") or []),
        "quote": (p.get("quoteToken") or {}).get("symbol"),
        "vol24h_usd": round(float((p.get("volume") or {}).get("h24") or 0), 2),
        "txns24h": sum((p.get("txns") or {}).get("h24", {}).get(k, 0) for k in ("buys", "sells")),
        "fdv_usd": p.get("fdv"), "market_cap_usd": p.get("marketCap"),
        "websites": " ; ".join(sites), "socials": " ; ".join(socials),
        "qualifying_pairs": e["n"], "dexscreener_url": p.get("url"),
        "hp_checked": hpd.get("ok"), "hp_is_honeypot": hpd.get("isHoneypot"),
        "hp_risk": hpd.get("risk"), "hp_buy_tax": hpd.get("buyTax"),
        "hp_sell_tax": hpd.get("sellTax"), "hp_flags": "|".join(map(str, hpd.get("flags") or [])),
        "hp_open_source": hpd.get("openSource"),
        "src_verified": verified, "contract_name": cname,
        "memeish_name": memeish, "dropped": drop, "drop_reason": "; ".join(why),
    })
    if i % 25 == 0:
        print(f"  checked {i}/{len(by_token)}", flush=True)

json.dump(rows, open(f"{DATA}/classified.json", "w"), indent=1)
kept = [r for r in rows if not r["dropped"]]
drp = [r for r in rows if r["dropped"]]
print(f"\nchecked {len(rows)} | KEPT {len(kept)} | dropped {len(drp)}")
print(f"honeypot check failed (kept, unverified): {sum(1 for r in kept if not r['hp_checked'])}")

cols = ["name","symbol","token_address","pair_address","liquidity_usd","age_days","dex","quote",
        "labels","vol24h_usd","txns24h","fdv_usd","market_cap_usd","websites","socials",
        "qualifying_pairs","dexscreener_url","hp_checked","hp_is_honeypot","hp_risk",
        "hp_buy_tax","hp_sell_tax","hp_flags","hp_open_source","src_verified","contract_name","memeish_name"]
with open(f"{DATA}/bsc_new_projects.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader()
    for r in kept: w.writerow(r)
with open(f"{DATA}/bsc_excluded.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols+["drop_reason"], extrasaction="ignore"); w.writeheader()
    for r in drp: w.writerow(r)
print("wrote bsc_new_projects.csv and bsc_excluded.csv")
