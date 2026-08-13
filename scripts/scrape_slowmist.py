"""Scrape the full SlowMist Hacked database (server-rendered HTML, no API).

Pulls every event across all categories -- not just the BSC filter -- because
incidents involving BSC tokens are sometimes filed under Other/Blockchain.
"""
import requests, re, json, time

H = {"User-Agent": "Mozilla/5.0"}
BASE = "https://hacked.slowmist.io/"
OUT = "/home/user/test111/data/slowmist_events.json"

def page(url, tries=4):
    for t in range(tries):
        try:
            r = requests.get(url, timeout=35, headers=H)
            if r.status_code == 200:
                return r.text
            time.sleep(2 * (t + 1))
        except Exception:
            time.sleep(2 * (t + 1))
    return None

def parse(html):
    """Entries render as divs; strip tags and split on the record markers."""
    b = re.sub(r'<script.*?</script>', '', html, flags=re.S)
    b = re.sub(r'<[^>]+>', '\n', b)
    b = re.sub(r'&amp;', '&', b)
    lines = [x.strip() for x in b.split("\n") if x.strip()]
    flat = " ".join(lines)
    out = []
    for m in re.finditer(
        r'(\d{4}-\d{2}-\d{2})\s*Hacked target:\s*(.*?)\s*Description of the event:\s*(.*?)'
        r'(?=\d{4}-\d{2}-\d{2}\s*Hacked target:|Copyright|$)', flat, re.S):
        out.append({"date": m.group(1), "target": m.group(2).strip()[:120],
                    "desc": re.sub(r'\s+', ' ', m.group(3)).strip()[:1200]})
    return out

html = page(BASE)
_flat = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', html))
_m = re.search(r'([\d,]+) hack event', _flat)
if not _m:
    raise SystemExit("could not read event total from landing page -- layout changed")
total = int(_m.group(1).replace(",", ""))
pages = (total + 19) // 20
print(f"total events: {total} -> {pages} pages", flush=True)

events, seen = [], set()
for p in range(1, pages + 1):
    h = page(BASE + f"?page={p}")
    if not h:
        print(f"  page {p}: FAILED", flush=True); continue
    got = parse(h)
    for e in got:
        k = (e["date"], e["target"])
        if k not in seen:
            seen.add(k); events.append(e)
    if p % 20 == 0 or p == pages:
        print(f"  page {p}/{pages} -> {len(events)} events", flush=True)
    time.sleep(0.45)

json.dump({"total_reported": total, "events": events}, open(OUT, "w"), indent=1)
print(f"scraped {len(events)} unique events (site reports {total})")
