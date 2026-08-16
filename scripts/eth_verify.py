"""QA: re-fetch a sample of final rows straight from DEXScreener and confirm the
CSV matches live API values. Guards against stale or mis-joined data."""
import json, requests, time, random, csv
H={"User-Agent":"Mozilla/5.0","Accept":"application/json"}
DATA="/home/user/test111/data"
rows=[r for r in json.load(open(f"{DATA}/eth_classified.json")) if not r["dropped"]]
random.seed(7)
sample=random.sample(rows, min(12,len(rows)))
NOW=time.time(); bad=0
print(f"verifying {len(sample)} of {len(rows)} rows against live DEXScreener\n")
for r in sample:
    d=requests.get(f"https://api.dexscreener.com/latest/dex/pairs/ethereum/{r['pair_address']}",timeout=30,headers=H).json()
    ps=d.get("pairs") or []
    if not ps:
        print(f"  {r['symbol']:>10}  NO DATA RETURNED on re-fetch"); bad+=1; continue
    p=ps[0]
    liq=float((p.get("liquidity") or {}).get("usd") or 0)
    age=(NOW-p["pairCreatedAt"]/1000)/86400 if p.get("pairCreatedAt") else None
    dl=abs(liq-r["liquidity_usd"])/max(r["liquidity_usd"],1)*100
    ok_sym = p["baseToken"]["symbol"]==r["symbol"]
    ok_age = age is not None and abs(age-r["age_days"])<1.5
    flag = "" if (dl<25 and ok_sym and ok_age) else "  <-- CHECK"
    if flag: bad+=1
    print(f"  {r['symbol']:>10}  csv=${r['liquidity_usd']:>12,.0f}  live=${liq:>12,.0f}  Δ{dl:5.1f}%  age csv={r['age_days']:.1f} live={age:.1f}  sym_ok={ok_sym}{flag}")
    time.sleep(0.3)
print(f"\n{len(sample)-bad}/{len(sample)} rows verified clean (liquidity moves between runs; <25% drift expected)")
