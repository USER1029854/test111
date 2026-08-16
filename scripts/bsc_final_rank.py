"""Phase 5 (BSC): merge on-chain verification onto bsc_contract_logic.csv and produce
the final ranked candidate list, with exclusions justified in-line rather than silently
dropped.

Two exclusions applied here, beyond the exploited-STY row already flagged upstream:
  * CDAO -- its only qualifying pool is CDAO/Pro. Pro was itself drained via a missing-
    access-control bug on 2026-07-28 (see EXPLOIT dict in final_output.py) and has no
    discoverable USD price on GeckoTerminal at all. The $10.8M headline is circular
    pricing against a token with no real independent market -- exactly the trap the
    brief warned about. Recorded as EXCLUDED, not silently dropped.
  * The 11-member "bStocks" beacon-proxy family (SPCXB/NVDAB/TSLAB/AAPLB/GOOGLB/BABAB/
    GMEB/SKHYB/MSFTB/QQQB/SPYB, impl 0xcfed6c46...) -- identified via web research as
    Binance-affiliated tokenized-equity products already integrated as collateral into
    Venus Protocol's Core Pool. These pass every mechanical filter (age, liquidity,
    custom logic, even a striking clone-family signal) but fail the brief's actual
    target profile: "largely unwatched... nobody has reviewed them and nobody has
    warned the team." A backed product already live inside a major lending protocol is
    the opposite of that. Excluded from the ranked candidate list; kept as a separate
    structural note (single EOA holds upgrade authority over the whole family) since
    that's a real observation, just not a cold-outreach candidate.
"""
import csv, json

DATA = "/home/user/test111/data"
rows = list(csv.DictReader(open(f"{DATA}/bsc_contract_logic.csv")))
verify = json.load(open("/tmp/claude-0/-home-user-test111/958631bf-a002-5f41-98f2-bf8502fbeec3/scratchpad/bsc_verify_results.json"))
vby = {v["token"].lower(): v for v in verify}

BSTOCKS_IMPL = "0xcfed6c4679297ea4889f8183bc057b4a86c64e46"
EXCLUDE = {
    "0xa9d33e9203e7d4b9ea8f37eca73cfe810c5d7cd0": "circular liquidity: only pool is CDAO/Pro, "
        "Pro was drained 2026-07-28 (missing access control) and has no discoverable USD price "
        "on GeckoTerminal -- the $10.8M headline is not real, backing traces to a dead token",
    "0xd6a4f5aadd88eba9a170acf67f737bd488142857": "already exploited 2026-07-30 (~$625K, leaked "
        "off-chain signer key) -- not a forward-looking candidate",
}

MAJORS = {"WBNB","USDT","USDC","BTCB","ETH","CAKE","FDUSD","BUSD","BNB"}
out = []
for r in rows:
    a = r["token_address"].lower()
    if a in EXCLUDE:
        continue
    if r.get("effective_implementation","").lower() == BSTOCKS_IMPL:
        continue
    v = vby.get(a, {})
    onchain = v.get("onchain_liq_usd_2x_quote_side")
    quote_major = (r["quote"] or "").upper() in MAJORS
    out.append({
        **r,
        "onchain_verified_liq_usd": onchain,
        "liq_verification": (
            "on-chain confirmed" if onchain and quote_major else
            "on-chain quote-side read but quote asset not a major -- USD figure soft" if onchain else
            "not independently verified -- carried through from DEXScreener only"
        ),
    })

# rank: prefer on-chain-verified figure when we have it, else fall back to reported
def rank_liq(r):
    return float(r["onchain_verified_liq_usd"] or r["liquidity_usd"])

out.sort(key=lambda r: -rank_liq(r))

cols = ["symbol","name","token_address","pair_address","dex","quote","age_days",
        "liquidity_usd","onchain_verified_liq_usd","liq_verification",
        "contract_name","is_proxy","minimal_proxy_clone","effective_implementation",
        "impl_shared_by_n_tokens","keep_categories","fund_fns","admin_setter_fns",
        "admin_mover_fns","bridge_fns","controls_reserve_treasury_pool_vault",
        "reserve_identifiers","holder_count","risk_flags","websites","socials",
        "exploit_status","exploit_detail"]
with open(f"{DATA}/bsc_final_candidates.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    for r in out: w.writerow(r)

print(f"final BSC candidate list: {len(out)} (from {len(rows)} in contract-logic pass)")
print(f"excluded: {len(EXCLUDE)} circular/exploited + 11 bStocks (backed/already-integrated, not unwatched)")
print(f"on-chain confirmed: {sum(1 for r in out if r['liq_verification']=='on-chain confirmed')}")
print("wrote bsc_final_candidates.csv")
