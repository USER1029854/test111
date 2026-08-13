# BSC New-Project Discovery

Finds recently-deployed BNB Smart Chain tokens/protocols that have real liquidity —
the kind of launch that is too new to appear on DefiLlama.

**Selection criteria:** liquidity >= $100,000 USD and pair age < 60 days, measured
from DEXScreener, after removing honeypots and product-less memecoins.

## Data sources and why

| Source | Role | Notes |
|---|---|---|
| **DEXScreener** | **Source of record** | Every reported metric (name, symbol, liquidity, age, DEX, socials) comes from a DEXScreener API response. |
| GeckoTerminal | Address index only | DEXScreener publishes no "new pairs by chain" endpoint, and its internal screener API is Cloudflare-blocked (403). GeckoTerminal is the one free BSC-wide pool enumeration. Its numbers are used **only** to shortlist candidates, never reported. |
| honeypot.is | Safety screen | Sell/buy tax, honeypot simulation, risk flags. |
| BscScan (Etherscan V2, chain 56) | Source verification | On the free tier this key only authorises `contract.getsourcecode`; `logs`, `account`, `block`, `stats` and `token` all return *"Free API access is not supported for this chain"*. That rules out on-chain `PairCreated` enumeration, so the key is used for contract-verification status. |

## Measured API constraints

These were verified empirically, not assumed:

- `GET /latest/dex/tokens/{addrs}` **hard-caps at 30 pairs total** regardless of how many
  addresses are supplied — passing 10 tokens returned pairs covering only 6 of them.
  Batching there silently drops tokens, so the pipeline does not use it for bulk reads.
- `GET /latest/dex/pairs/bsc/{addrs}` **is true 1:1** (24 requested -> 24 returned, 0 missing).
  This is the bulk-read path.
- GeckoTerminal pool addresses that are 64-hex are **PancakeSwap Infinity singleton pool IDs**,
  not contracts; DEXScreener cannot resolve them by that ID. Those are resolved by base token instead.
- GeckoTerminal only permits `sort=h24_volume_usd_desc` or `h24_tx_count_desc`, and caps
  pagination at 10 pages; `new_pools` therefore only reaches ~2 hours back. Coverage is
  recovered by sweeping many DEXes and both sort orders.

## Pipeline

```
scripts/discover.py       # net A: GeckoTerminal BSC-wide pool enumeration
scripts/search_sweep.py   # net B: DEXScreener search, ~931 terms (independent host)
scripts/enrich.py         # merge nets -> authoritative DEXScreener read -> apply liq/age filter
scripts/classify.py       # honeypot.is + BscScan verification + junk filter -> CSV
scripts/report.py         # render final markdown table
scripts/verify.py         # QA: re-fetch a sample live and diff against the CSV
```

Run in that order. Intermediate state lands in `data/`.

## Filter posture

Deliberately loose, so real projects are not lost to over-filtering. A token is dropped
**only** on an unambiguous signal:

1. honeypot.is confirms `isHoneypot = true`
2. sell tax >= 50% (effectively unsellable)
3. meme-style name **and** zero website **and** zero socials

Anything uncertain is kept and flagged. Tokens whose honeypot check *failed* are kept and
marked as unverified rather than being treated as passing — a failed check is never
recorded as a clean one.

## Result of the 2026-08-13 run

| Stage | Count |
|---|---|
| Pools discovered (net A: GeckoTerminal) | 5,707 |
| Pools discovered (net B: DEXScreener search) | 2,064 (1,836 unique to this net) |
| Merged discovery universe | 7,543 |
| Pairs read authoritatively from DEXScreener | 4,192 (655 calls, 0 failures) |
| Pairs meeting liquidity >= $100k and age < 60d | 120 |
| Distinct tokens | 112 |
| Dropped (confirmed honeypots) | 3 |
| **Kept** | **109** |

QA: 12 rows re-fetched live from DEXScreener, 12/12 matched (max drift 4.5%).

### Screening coverage

honeypot.is could screen only **3 of 112** tokens; the other 109 returned
`404 pair not found`. GoPlus covered 111 of 112. One token has no usable safety
data from either provider and is kept with a `SAFETY_CHECK_UNAVAILABLE` flag.

### Caveats worth carrying into any use of this list

- **74 of 109 have neither a website nor socials on DEXScreener.** Liquidity and age
  are objective; "is a real project" is not, and the loose filter keeps them.
- **20 of 109 are quoted against an obscure token rather than a major asset**
  (e.g. CDAO/Pro, NEX/AIC). Liquidity denominated in a thin quote token can be
  circular, so the headline USD figure is softer for those rows.
- A cluster of tickers imitates real equities (NVDAB, AAPLB, TSLAB, MSFTB, GOOGLB,
  BABAB, GMEB, SKHYB). These are lookalike tokens, not equity products.
- 35 of 109 have both a web presence and a verified contract — the strictest subset,
  reachable by filtering the CSV on `websites`/`socials` and `src_verified`.

## Output

- `data/bsc_new_projects.csv` — the 109 kept projects
- `data/bsc_excluded.csv` — everything dropped, with `drop_reason`, so the filter is auditable
