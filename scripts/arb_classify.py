"""Phase 3: safety screen + junk filter, then emit the table and CSV.

Safety screening on Arbitrum differs from the BSC template in one structural
way, confirmed empirically before writing this script:

  * honeypot.is -- DOES NOT SUPPORT ARBITRUM AT ALL. `IsHoneypot?...&chainID=42161`
                   returns `{"code":400,"error":"Invalid chain"}` for every address,
                   including majors like ARB itself, and the same happens with
                   `chainId` casing. This is chain-level, not per-token, so the
                   whole honeypot.is column is recorded as `chain_unsupported`
                   rather than attempted per-token. GoPlus and source-code
                   verification carry the full safety-screen weight instead.
  * GoPlus       -- confirmed working on chain 42161 (`token_security/42161`),
                    queried one address at a time (batch mode only returns
                    pre-cached entries, same constraint as the BSC template).

Filter posture is deliberately loose per the brief: a token is dropped only on an
unambiguous signal. Anything uncertain is KEPT and flagged. A check that FAILED is
recorded as a failure -- never silently promoted to a pass.
"""
import requests, json, time, csv, re, os

H = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
KEY = "R6PYYNEX4CNFAXX4YX3K8W4NXSBGGG4QGJ"
DATA = "/home/user/test111/data"
CHAINID = 42161

MAJORS = {a.lower() for a in [
 "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1","0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
 "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8","0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
 "0x912CE59144191C1204E64559FE8253a0e49E6548","0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f"]}

MEME_KW = re.compile(r"(doge|shib|inu|pepe|wojak|elon|moon|floki|bonk|chad|giga|"
                     r"baby|safe|cum|cat\b|kitty|frog|meme|troll|retard|tard|"
                     r"pump|rocket|lambo|ape\b|banana|monkey|clown|poo|shit|"
                     r"trump|biden|milady|mog|brett|andy|turbo|wif\b|hat\b)", re.I)

def get(url, params=None, tries=3, pause=0.3):
    for t in range(tries):
        try:
            r = requests.get(url, params=params, timeout=35, headers=H)
            if r.status_code == 200:
                time.sleep(pause); return r.json()
            if r.status_code == 429:
                time.sleep(6 * (t + 1)); continue
            if r.status_code == 404:
                return {"__http": 404}
            time.sleep(1.5 * (t + 1))
        except Exception:
            time.sleep(1.5 * (t + 1))
    return None

def fnum(v):
    """GoPlus returns taxes as fractional strings ('0.03' == 3%); '' means unknown."""
    try:
        return None if v in (None, "", "-") else float(v)
    except Exception:
        return None

d = json.load(open(f"{DATA}/arb_ds_qualifying.json"))
qual, profiles = d["qualifying"], d.get("profiles", {})
print(f"qualifying pairs from DEXScreener: {len(qual)}")

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
    tok = p["baseToken"]["address"]
    info = p.get("info") or {}
    sites = [w.get("url") for w in (info.get("websites") or []) if w.get("url")]
    socials = [s.get("url") for s in (info.get("socials") or []) if s.get("url")]
    pr = profiles.get(addr) or {}
    for l in (pr.get("links") or []):
        u = l.get("url")
        if not u: continue
        (sites if (l.get("label") or "").lower() == "website" else socials).append(u)
    sites, socials = list(dict.fromkeys(sites)), list(dict.fromkeys(socials))

    # --- provider 1: honeypot.is -- chain confirmed unsupported, not attempted per-token ---
    hp_state, hp_honey, hp_risk, hp_buy, hp_sell = "chain_unsupported", None, None, None, None

    # --- provider 2: GoPlus (single address = on-demand scan) ---
    gp = get(f"https://api.gopluslabs.io/api/v1/token_security/{CHAINID}",
             {"contract_addresses": tok}, pause=1.9)
    g = ((gp or {}).get("result") or {}).get(tok.lower()) if isinstance(gp, dict) else None
    gp_state = "ok" if g else "failed"
    g = g or {}
    gp_honey = g.get("is_honeypot")
    gp_buy, gp_sell = fnum(g.get("buy_tax")), fnum(g.get("sell_tax"))   # fractional units

    # --- provider 3: Arbiscan (via Etherscan V2) source verification ---
    sc = get("https://api.etherscan.io/v2/api",
             dict(chainid=CHAINID, module="contract", action="getsourcecode",
                  address=tok, apikey=KEY), pause=0.45)
    verified, cname = None, None
    if isinstance(sc, dict) and str(sc.get("status")) == "1":
        r0 = (sc.get("result") or [{}])[0]
        verified, cname = bool(r0.get("SourceCode")), r0.get("ContractName") or None

    name = p["baseToken"].get("name") or ""
    sym = p["baseToken"].get("symbol") or ""
    has_web, has_soc = bool(sites), bool(socials)
    memeish = bool(MEME_KW.search(f"{name} {sym}"))

    # unify tax units to percent (honeypot.is unavailable on this chain, so
    # GoPlus is the only tax source)
    sell_pct = gp_sell * 100 if gp_sell is not None else None
    buy_pct  = gp_buy  * 100 if gp_buy  is not None else None
    screened = (gp_state == "ok")   # honeypot.is structurally excluded from this chain

    drop, why = False, []
    if str(gp_honey) == "1":
        drop = True; why.append("confirmed honeypot")
    if sell_pct is not None and sell_pct >= 50:
        drop = True; why.append(f"sell tax {sell_pct:.0f}%")
    if str(g.get("cannot_sell_all")) == "1":
        drop = True; why.append("cannot sell all")
    if memeish and not has_web and not has_soc:
        drop = True; why.append("meme-style name, no website/socials")

    flags = []
    if verified is False: flags.append("unverified_source")
    if str(g.get("is_mintable")) == "1": flags.append("mintable")
    if str(g.get("transfer_pausable")) == "1": flags.append("pausable")
    if str(g.get("hidden_owner")) == "1": flags.append("hidden_owner")
    if str(g.get("is_blacklisted")) == "1": flags.append("blacklist_fn")
    if str(g.get("can_take_back_ownership")) == "1": flags.append("reclaimable_ownership")
    op = fnum(g.get("owner_percent"))
    if op is not None and op >= 0.5: flags.append(f"owner_holds_{op*100:.0f}pct")
    if not screened: flags.append("SAFETY_CHECK_UNAVAILABLE")
    flags.append("honeypot_is_chain_unsupported")

    rows.append({
        "name": name, "symbol": sym, "token_address": tok, "pair_address": p["pairAddress"],
        "liquidity_usd": round(p["_liq_usd"], 2), "age_days": round(p["_age_days"], 1),
        "dex": p.get("dexId"), "labels": "|".join(p.get("labels") or []),
        "quote": (p.get("quoteToken") or {}).get("symbol"),
        "quote_address": (p.get("quoteToken") or {}).get("address"),
        "vol24h_usd": round(float((p.get("volume") or {}).get("h24") or 0), 2),
        "txns24h": sum((p.get("txns") or {}).get("h24", {}).get(k, 0) for k in ("buys", "sells")),
        "fdv_usd": p.get("fdv"), "market_cap_usd": p.get("marketCap"),
        "websites": " ; ".join(sites), "socials": " ; ".join(socials),
        "qualifying_pairs": e["n"], "dexscreener_url": p.get("url"),
        "screened": screened, "honeypot_is_state": hp_state, "honeypot_is_result": hp_honey,
        "honeypot_is_risk": hp_risk, "goplus_state": gp_state, "goplus_is_honeypot": gp_honey,
        "buy_tax_pct": buy_pct, "sell_tax_pct": sell_pct,
        "holder_count": g.get("holder_count"), "lp_holder_count": g.get("lp_holder_count"),
        "owner_percent": g.get("owner_percent"), "creator_percent": g.get("creator_percent"),
        "src_verified": verified, "contract_name": cname,
        "risk_flags": "|".join(flags), "memeish_name": memeish,
        "dropped": drop, "drop_reason": "; ".join(why),
    })
    if i % 20 == 0:
        print(f"  screened {i}/{len(by_token)}", flush=True)

json.dump(rows, open(f"{DATA}/arb_classified.json", "w"), indent=1)
kept = [r for r in rows if not r["dropped"]]
drp = [r for r in rows if r["dropped"]]
print(f"\nscreened {len(rows)} | KEPT {len(kept)} | dropped {len(drp)}")
print(f"  honeypot.is: chain 42161 confirmed unsupported (Invalid chain on every call) -- not used")
print(f"  GoPlus usable: {sum(1 for r in rows if r['goplus_state']=='ok')}")
print(f"  NO safety data at all (kept, flagged): {sum(1 for r in kept if not r['screened'])}")

cols = ["name","symbol","token_address","pair_address","liquidity_usd","age_days","dex","quote",
        "quote_address","labels","vol24h_usd","txns24h","fdv_usd","market_cap_usd","websites","socials",
        "qualifying_pairs","dexscreener_url","screened","honeypot_is_state","honeypot_is_result",
        "honeypot_is_risk","goplus_state","goplus_is_honeypot","buy_tax_pct","sell_tax_pct",
        "holder_count","lp_holder_count","owner_percent","creator_percent","src_verified",
        "contract_name","risk_flags","memeish_name"]
with open(f"{DATA}/arb_new_projects.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader()
    for r in kept: w.writerow(r)
with open(f"{DATA}/arb_excluded.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols+["drop_reason"], extrasaction="ignore"); w.writeheader()
    for r in drp: w.writerow(r)
print("wrote arb_new_projects.csv and arb_excluded.csv")
