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

## Output

- `data/bsc_new_projects.csv` — the kept projects
- `data/bsc_excluded.csv` — everything dropped, with `drop_reason`, so the filter is auditable
