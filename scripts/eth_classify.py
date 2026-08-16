"""Phase 3: safety screen + junk filter, then emit the table and CSV.

Safety screening uses two providers because neither alone covers the population:

  * honeypot.is  -- requested screen; unlike BSC, Ethereum's mature Uniswap v2/v3
                    routing means honeypot.is's simulator can price most pairs.
  * GoPlus       -- fallback, queried one address at a time because batch mode
                    only returns pre-cached entries. Recovers tokens honeypot.is
                    cannot see, and adds holder/owner/LP signals.

Filter posture is deliberately loose per the brief: a token is dropped only on an
unambiguous signal. Anything uncertain is KEPT and flagged. A check that FAILED is
recorded as a failure -- never silently promoted to a pass.
"""
import requests, json, time, csv, re, os

H = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
KEY = "R6PYYNEX4CNFAXX4YX3K8W4NXSBGGG4QGJ"
DATA = "/home/user/test111/data"

# Blue-chip / well-established Ethereum-mainnet tokens. This is a hygiene filter,
# not the primary age/liquidity screen (enrich.py already applied that on
# pairCreatedAt) -- it exists because an old, huge-cap token can still show up
# via a freshly-created pool (new UniV3 fee tier, new Curve pool, etc.) and pass
# the age filter on POOL age even though the TOKEN itself is not a "new project".
# Addresses verified on-chain via symbol() through the public RPC before use.
MAJORS = {a.lower() for a in [
 "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # WETH
 "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",  # USDC
 "0xdAC17F958D2ee523a2206206994597C13D831ec7",  # USDT
 "0x6B175474E89094C44Da98b954EedeAC495271d0F",  # DAI
 "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",  # WBTC
 "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84",  # stETH
 "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0",  # wstETH
 "0xCd5fE23C85820F7B72D0926FC9b05b43E359b7ee",  # weETH
 "0xae78736Cd615f374D3085123A210448E74Fc6393",  # rETH
 "0xBe9895146f7AF43049ca1c1AE358B0541Ea49704",  # cbETH
 "0x514910771AF9Ca656af840dff83E8264EcF986CA",  # LINK
 "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",  # UNI
 "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9",  # AAVE
 "0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2",  # MKR
 "0xD533a949740bb3306d119CC777fa900bA034cd52",  # CRV
 "0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32",  # LDO
 "0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F",  # SNX
 "0xc00e94Cb662C3520282E6f5717214004A7f26888",  # COMP
 "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e",  # YFI
 "0x6B3595068778DD592e39A122f4f5a5cF09C90fE2",  # SUSHI
 "0xba100000625a3754423978a60c9317c58a424e3D",  # BAL
 "0x111111111117dC0aa78b770fA6A738034120C302",  # 1INCH
 "0xC18360217D8F7Ab5e7c516566761Ea12Ce7F9D72",  # ENS
 "0xc944E90C64B2c07662A292be6244BDf05Cda44a7",  # GRT
 "0x3432B6A60D23Ca0dFCa7761B7ab56459D9C964D0",  # FXS
 "0x853d955aCEf822Db058eb8505911ED77F175b99e",  # FRAX
 "0x45804880De22913dAFE09f4980848ECE6EcbAf78",  # PAXG
 "0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE",  # SHIB
 "0x6982508145454Ce325dDbE47a25d4ec3d2311933",  # PEPE
 "0x6De037ef9aD2725EB40118Bb1702EBb27e4Aeb24",  # RENDER/RNDR
 "0xF57e7e7C23978C3cAEC3C3548E3D615c346e79fF",  # IMX
 "0x0F5D2fB29fb7d3CFeE444a200298f468908cC942",  # MANA
 "0x3845badAde8e6dFF049820680d1F14bD3903a5d0",  # SAND
 "0x4d224452801ACEd8B2F0aebE155379bb5D594381",  # APE
 "0x15D4c048F83bd7e37d49eA4C83a07267Ec4203dA",  # GALA
 "0x57e114B691Db790C35207b2e685D4A43181e6061",  # ENA
 "0xFe0c30065B384F05761f15d0CC899D4F9F9Cc0eB",  # ETHFI
 "0x808507121B80c02388fAd14726482e061B8da827",  # PENDLE
 "0xfAbA6f8e4a5E8Ab82F62fe7C39859FA577269BE3",  # ONDO
 "0xD33526068D116cE69F19A9ee46F0bd304F21A51f",  # RPL
 "0x4c9EDD5852cd905f086C759E8383e09bff1E68B3",  # USDe
 "0x83F20F44975D03b1b09e64809B757c47f942BEeA",  # sDAI
 "0x9D39A5DE30e57443BfF2A8307A4256c8797A3497",  # sUSDe
 "0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf",  # cbBTC
 "0x0000000000085d4780B73119b644AE5ecd22b376",  # TUSD
 "0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B",  # CVX (Convex)
 "0x84158fcfE687221d27C49734167D95f1Fb2C1Aa5",  # CVX (alt liquidity venue, same symbol)
 "0x5f98805A4E8be255a32880FDeC7F6728C6568bA0",  # LUSD
 "0x40D16FC0246aD3160Ccc09B8D0D3A2cD28aE6C2f",  # GHO
 "0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0",  # MATIC (legacy)
 "0xB50721BCf8d664c30412Cfbc6cf7a15145234ad1",  # ARB
 "0x0000000000000000000000000000000000000000",
]}

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

d = json.load(open(f"{DATA}/eth_ds_qualifying.json"))
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

    # --- provider 1: honeypot.is (as requested) ---
    hp = get("https://api.honeypot.is/v2/IsHoneypot", {"address": tok, "chainID": 1}, pause=0.3)
    hp_state, hp_honey, hp_risk, hp_buy, hp_sell = "failed", None, None, None, None
    if isinstance(hp, dict) and hp.get("__http") == 404:
        hp_state = "not_indexed"
    elif isinstance(hp, dict) and hp:
        hr, sr, sm = hp.get("honeypotResult") or {}, hp.get("simulationResult") or {}, hp.get("summary") or {}
        hp_state, hp_honey, hp_risk = "ok", hr.get("isHoneypot"), sm.get("risk")
        hp_buy, hp_sell = sr.get("buyTax"), sr.get("sellTax")   # percent units

    # --- provider 2: GoPlus (single address = on-demand scan) ---
    gp = get("https://api.gopluslabs.io/api/v1/token_security/1",
             {"contract_addresses": tok}, pause=1.9)
    g = ((gp or {}).get("result") or {}).get(tok.lower()) if isinstance(gp, dict) else None
    gp_state = "ok" if g else "failed"
    g = g or {}
    gp_honey = g.get("is_honeypot")
    gp_buy, gp_sell = fnum(g.get("buy_tax")), fnum(g.get("sell_tax"))   # fractional units

    # --- provider 3: Etherscan source verification ---
    sc = get("https://api.etherscan.io/v2/api",
             dict(chainid=1, module="contract", action="getsourcecode",
                  address=tok, apikey=KEY), pause=0.22)
    verified, cname = None, None
    if isinstance(sc, dict) and str(sc.get("status")) == "1":
        r0 = (sc.get("result") or [{}])[0]
        verified, cname = bool(r0.get("SourceCode")), r0.get("ContractName") or None

    name = p["baseToken"].get("name") or ""
    sym = p["baseToken"].get("symbol") or ""
    has_web, has_soc = bool(sites), bool(socials)
    memeish = bool(MEME_KW.search(f"{name} {sym}"))

    # unify tax units to percent
    sell_pct = hp_sell if isinstance(hp_sell, (int, float)) else (gp_sell * 100 if gp_sell is not None else None)
    buy_pct  = hp_buy  if isinstance(hp_buy, (int, float))  else (gp_buy  * 100 if gp_buy  is not None else None)
    screened = (hp_state == "ok") or (gp_state == "ok")

    drop, why = False, []
    if hp_honey is True or str(gp_honey) == "1":
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

json.dump(rows, open(f"{DATA}/eth_classified.json", "w"), indent=1)
kept = [r for r in rows if not r["dropped"]]
drp = [r for r in rows if r["dropped"]]
print(f"\nscreened {len(rows)} | KEPT {len(kept)} | dropped {len(drp)}")
print(f"  honeypot.is usable: {sum(1 for r in rows if r['honeypot_is_state']=='ok')}"
      f" | not indexed: {sum(1 for r in rows if r['honeypot_is_state']=='not_indexed')}"
      f" | failed: {sum(1 for r in rows if r['honeypot_is_state']=='failed')}")
print(f"  GoPlus usable: {sum(1 for r in rows if r['goplus_state']=='ok')}")
print(f"  NO safety data at all (kept, flagged): {sum(1 for r in kept if not r['screened'])}")

cols = ["name","symbol","token_address","pair_address","liquidity_usd","age_days","dex","quote",
        "quote_address","labels","vol24h_usd","txns24h","fdv_usd","market_cap_usd","websites","socials",
        "qualifying_pairs","dexscreener_url","screened","honeypot_is_state","honeypot_is_result",
        "honeypot_is_risk","goplus_state","goplus_is_honeypot","buy_tax_pct","sell_tax_pct",
        "holder_count","lp_holder_count","owner_percent","creator_percent","src_verified",
        "contract_name","risk_flags","memeish_name"]
with open(f"{DATA}/eth_new_projects.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader()
    for r in kept: w.writerow(r)
with open(f"{DATA}/eth_excluded.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols+["drop_reason"], extrasaction="ignore"); w.writeheader()
    for r in drp: w.writerow(r)
print("wrote eth_new_projects.csv and eth_excluded.csv")
