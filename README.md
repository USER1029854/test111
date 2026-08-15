# DeFi exploit-candidate screen — BNB Chain · Ethereum · Arbitrum · Base

A defensive, pre-emptive target list: recently-deployed DeFi projects that are **shaped like the ones
that get exploited** — small, newer, largely unwatched, carrying **custom money-moving logic** nobody
has audited yet, with enough real liquidity to be worth an attacker's effort. The goal is to hand the
mapping/audit step a ranked set of individual targets, each with its chain, address, qualifying
liquidity and age, the custom logic that makes it a candidate, and whether it shares a codebase with
others.

> **What this is and is not.** This is a **risk-ranking of a population**, not a prediction that any
> single contract will be hit. Most never will be; some real future victims are *not* here because of
> structural blind spots (see the last section). Every figure traces to on-chain or market data captured
> in `data/`; anything that could not be verified is marked, not guessed.

---

## Headline

| Chain | Pools enumerated | Qualifying pairs (≥$100k, <60d) | Distinct candidate tokens | **Custom-logic candidates (ranked)** |
|:--|--:|--:|--:|--:|
| BNB Chain | ~7,543 | 120 | 112 | **95** |
| Ethereum | 1,026 | 56 | 38 | **28** |
| Base | 1,091 | 12 | 12 | **3** |
| Arbitrum | 783 | 4 | 4 | **1** |
| **Total** | — | **192** | **166** | **127** |

Of the 127 ranked candidates: **37 belong to a shared-codebase family**, **30 are proxies** (swappable
logic), **51 control a reserve / treasury / pool / vault**. A further **8** were set aside for
inflated/circular liquidity, **0** as honeypots, and **2** BSC contracts were **already exploited during
the window** (validation, below).

**The ranking is led by Ethereum synthetic-dollar staking vaults** (Ethena `USDe`/`sUSDe`-fork
lineage), then two large **BNB Chain factory-clone families**. Full list: `data/exploit_candidates_ranked.csv`.

---

## What makes something a candidate (the filter that matters)

A candidate is **not** "a token that trades a lot." A plain token — one whose only state change is
moving balances with ordinary ERC-20 transfer machinery — has essentially nothing to exploit at the
contract level, no matter its volume. Those are dropped.

A candidate carries **custom money-moving logic of its own**, confirmed by reading what the verified
source actually does (not by function names):

- mint / burn on its own terms, reflection / rebase / reward accounting
- staking, vaults, deposits, withdrawals, claims, redemptions
- cross-chain movement (LayerZero OFT `send`/`lzReceive`, bridges)
- price / oracle handling, signature-gated transfers (voucher/permit-style)
- swappable logic (upgradeable proxy — owner can replace the whole implementation)
- privileged functions that move funds or reassign control (`rescue`/`sweep`/`drain`, treasury/pool/
  signer setters, blacklist/pause/mint authority)

Each kept contract is one that, if its custom logic is wrong or its access control is weak, can **leak
funds it holds or steers** — which is what an exploit is.

---

## Ranked candidates (top 30 of 127)

Ranked by an ordinal **exploit-likelihood score** (defined below). `Real liq` is the **quote-side**
reserve (real external money in the pool), not the headline figure. `Custom logic` names the verified
implementation contract where informative. Full 127 with every signal column: `data/exploit_candidates_ranked.csv`.

| # | Score | Chain | Symbol | Address | Real liq | Age | Custom logic | Family | Liq quality |
|--:|--:|:--|:--|:--|--:|--:|:--|:--|:--|
| 1 | 80.8 | eth | strUSD | `0x280839980a7eD0D7717F64125fE241012E5F5815` | $9.76M | 30d | `StakedTrUSD` — fund-ops, admin-setters, admin-mover, lifecycle, upgradeable | FAM03 (×2) | circular-quote |
| 2 | 72.1 | eth | sUSDat | `0xD166337499E176bbC38a1FBd113Ab144e5bd2Df7` | $0.11M | 11d | `StakedUSDat` — fund-ops, sig-gated, admin-setters, admin-mover, lifecycle, upgradeable | — | circular-quote |
| 3 | 67.2 | eth | trUSD | `0xd0580192E98eA6CEB9c7b6191Ed2E27560911697` | $5.15M | 30d | `TrUSD` — fund-ops, admin-setters, admin-mover, lifecycle, upgradeable | FAM03 (×2) | good |
| 4 | 67.1 | eth | STRCx | `0x1Aad217B8F78dbA5E6693460e8470F8b1A3977f3` | $2.74M | 17d | `BackedAutoFeeTokenImplementation` — fund-ops, sig-gated, admin-setters, lifecycle, upgradeable | — | circular-quote |
| 5 | 64.1 | eth | FXRP | `0xCE6170EA245dC8D1f275A710a062b70f125F0110` | $2.93M | 18d | `FXRPOFT` — fund-ops, admin-setters, **bridge**, lifecycle, upgradeable | — | circular-quote |
| 6 | 63.9 | bsc | RT | `0x82BbE7f1864279fc9604267509D6BAe946333919` | $0.24M | 6d | `MainToken` — fund-ops, admin-setters, admin-mover, lifecycle | — | good |
| 7 | 62.3 | bsc | MC | `0x5892B6EE1adEeb7d6169FCB052cfcF6bBc253139` | $0.28M | 6d | `SubToken` — fund-ops, admin-setters, admin-mover, lifecycle | — | circular-quote |
| 8 | 62.3 | bsc | ZT | `0xDd1667eC26684D62B43958D7f161540318720839` | $0.27M | 24d | `ZT` — fund-ops, admin-setters, admin-mover, lifecycle | — | circular-quote |
| 9 | 61.2 | bsc | AUV | `0x59523E38727C2F4E6DABe89dB938779058F2aDAf` | $10.08M | 28d | `AUVToken` — fund-ops, admin-setters, lifecycle | — | good |
| 10 | 60.5 | eth | ALBRH | `0x7AdbFd873084dB714A57eD648ee69Aa4627Cb998` | $0.28M | 3d | `AlberichToken` — fund-ops, admin-mover, lifecycle | — | good |
| 11 | 57.0 | bsc | APEX | `0xC2d2DfBf9A7F27138Ee32b9a4C17a2E5233aAAAA` | $0.28M | 60d | `APEX` — fund-ops, admin-setters, admin-mover, lifecycle | — | good |
| 12 | 56.6 | bsc | TKN | `0xc626AD09B1c30B556705741731879EE95d7C9939` | $0.18M | 22d | `TKNToken` — fund-ops, admin-setters, admin-mover | — | good |
| 13 | 56.0 | bsc | RICH | `0x7a128ff06283307C8492D92fa7961Ad6253E765d` | $3.70M | 32d | `RichToken` — fund-ops, admin-setters, lifecycle | — | good |
| 14 | 55.8 | bsc | XAUt | `0x21cAef8A43163Eea865baeE23b9C2E327696A3bf` | $0.24M | 19d | `TransparentUpgradeableProxy` — fund-ops, sig-gated, **bridge**, lifecycle | — | good |
| 15 | 55.4 | bsc | AFW | `0x398033B5c6c362ed1fDC9d0A66aAb359769A0C4b` | $0.75M | 53d | `AFW` — fund-ops, admin-setters, upgradeable | — | good |
| 16 | 54.0 | bsc | SPCXB | `0xbe9D156892E55e7154BcD3cB0FEA677F9D3103E1` | $1.82M | 12d | `BeaconProxy` — fund-ops, admin-setters, lifecycle | FAM02 (×10) | good |
| 17 | 53.7 | eth | apyUSD | `0x38EEb52F0771140d10c4E9A9a72349A329Fe8a6A` | $0.16M | 15d | `ApyUSD` — fund-ops, admin-setters, lifecycle, upgradeable | — | circular-quote |
| 18 | 53.4 | bsc | GMEB | `0x46cEeFDa28Dd7207059ed19B0acdc026955bb15C` | $0.70M | 2d | `BeaconProxy` — fund-ops, admin-setters, lifecycle | FAM02 (×10) | good |
| 19 | 53.2 | bsc | MarsCoin | `0xFe189E97832DA1573e4e4Ff034F4fFC3a15c7777` | $1.04M | 17d | `FlapTaxTokenV3` — lifecycle | FAM01 (×20) | circular-quote |
| 20 | 53.1 | bsc | 逆袭人生 | `0xceFbf00b3732FE91e46989037E4b2564a4fc7777` | $1.86M | 28d | `FlapTaxTokenV3` — lifecycle | FAM01 (×20) | good |
| 21 | 52.3 | bsc | NVDAB | `0x02Fca66C1D1aFB4E2A7884261eB00F63598a7436` | $0.81M | 16d | `BeaconProxy` — fund-ops, admin-setters, lifecycle | FAM02 (×10) | good |
| 22 | 52.2 | eth | CADD | `0x16F93eBC5320C89EfC8701577efe49d14A276a06` | $0.29M | 39d | `ERC20F` — fund-ops, admin-mover, lifecycle, upgradeable | — | circular-quote |
| 23 | 52.1 | bsc | Asian games | `0x31d19B3633eBdb60Dc9d690b3e9eB1FFF61A7777` | $0.28M | 5d | `FlapTaxTokenV3` — lifecycle | FAM01 (×20) | good |
| 24 | 52.1 | bsc | CBURN | `0x309409237C4dB70Cd66067741eDcF02Bf69E7777` | $0.24M | 2d | `FlapTaxTokenV3` — lifecycle | FAM01 (×20) | good |
| 25 | 51.8 | bsc | 金蝶圣甲 | `0x4f0c550bFe484F957D5C7Dd26f9a630a92A17777` | $0.77M | 26d | `FlapTaxTokenV3` — lifecycle | FAM01 (×20) | good |
| 26 | 51.8 | bsc | GOOGLB | `0x3F53De71c126BdaBAe20f9cD64848d317f6C3238` | $0.55M | 14d | `BeaconProxy` — fund-ops, admin-setters, lifecycle | FAM02 (×10) | good |
| 27 | 51.6 | bsc | CETS | `0xB0c2aB5af4028461acE3f6e1C33a4eE1404E7777` | $0.25M | 8d | `FlapTaxTokenV3` — lifecycle | FAM01 (×20) | circular-quote |
| 28 | 51.5 | bsc | 币有 | `0xe9337Dde3dd9e97f1f45A56412767ce5098E7777` | $0.31M | 13d | `FlapTaxTokenV3` — lifecycle | FAM01 (×20) | circular-quote |
| 29 | 51.3 | eth | apxUSD | `0x98A878b1Cd98131B271883B390f68D2c90674665` | $1.89M | 16d | `ApxUSD` — fund-ops, admin-setters, lifecycle, upgradeable | — | good |
| 30 | 51.1 | bsc | SUMMER | `0xeEb3d73d4dd44e6E4d957d89492f05d5CCeE7777` | $0.18M | 8d | `FlapTaxTokenV3` — lifecycle | FAM01 (×20) | circular-quote |

---

## The finding, read before the table

**Ethereum — Ethena `USDe`/`sUSDe` staking-vault fork lineage (leads the ranking).** The top cluster is a
set of independently-deployed **synthetic-dollar staking vaults** whose verified implementations are
recognisable Ethena forks: `strUSD`→`StakedTrUSD` + `trUSD`→`TrUSD` (one deployer `0xb5afef…`, family
**FAM03**, ~$15.2M combined), plus `sUSDat`→`StakedUSDat`, `apyUSD`→`ApyUSD`, `apxUSD`→`ApxUSD`
(separate deployers, same template — at least **five** USDe-fork deployments). Reading the `StakedTrUSD`
implementation confirms the full Ethena surface — `deposit`/`withdraw`/`redeem`/`unstake`, a cooldown
**silo**, `transferInRewards`, `redistributeLockedAmount`, `seizeCooldown`, UUPS `_authorizeUpgrade`,
`DEFAULT_ADMIN_ROLE`/`TIMELOCK_ADMIN_ROLE`, and `rescueSiloTokens`/`rescueOrphanFunds` admin movers.
Two tells that these are **anonymous forks, not the audited original**: Ethena branding is stripped from
the source, and one role is left as a placeholder `MY_ROLE`. These contracts **custody deposited
assets**, so the real value at risk is the **vault TVL**, not the DEX pool that qualified them — the
mapping step should pull each vault's TVL directly. This is the shared-template point at the
**lineage** level: a modification or access-control slip in one fork is a flaw the whole USDe-fork
population can inherit.

Two more ETH lineages sit just below: `STRCx`→`BackedAutoFeeTokenImplementation` on a `BackedTokenProxy`
(Backed Finance tokenised-RWA template — upgradeable, sig-gated), and `FXRP`→`FXRPOFT` on a
`TransparentUpgradeableProxy` (a **LayerZero OFT** — cross-chain mint/burn). Plus a GULD-ecosystem token
factory: two exact-clone sets, **FAM04** (`ELMT`/`GIVE`/`SWITCH`) and **FAM05** (`GULD`/`CDXR`), all
quoted against the ecosystem's own GULD token (which makes their headline liquidity circular).

**BNB Chain — two large factory-clone families** dominate (carried from the prior run, which covered BSC
exhaustively). One flaw here is a flaw in every member:
- **FAM01 — 20 EIP-1167 minimal-proxy clones**, all vanity `…7777` addresses, all delegating to one
  launchpad implementation `0x024f1829…` (`FlapTaxTokenV3`). ~$6.8M combined. (Includes `PIZZA`, whose
  ticker collides with a 2021 incident but is a different 2026 clone — ruled out, not counted as
  exploited.)
- **FAM02 — 10 beacon-proxy tokenised-equity lookalikes** (`NVDAB`,`AAPLB`,`TSLAB`,`GOOGLB`,`MSFTB`,
  `SPYB`,`QQQB`,`SKHYB`,`GMEB`,`SPCXB`), all sharing one implementation and one admin. ~$6.8M combined.

**Base — three small custom-logic tokens** (`HALO`, `VANRY`, `TAOT`); `TAOT` carries bridge logic,
`VANRY` is mintable+pausable. Six more Base candidates (`NFLXB`,`TOAD`,`DOS`,`PEPETO`,`KII`,`SPX10K`)
are **unverified** — set aside as unanalyzable, not judged.

**Arbitrum — structurally thin.** Of 783 pools enumerated, only 4 cleared the liquidity+age bar and only
**one** carried custom logic: `DUCT` (`DuctToken`). `EURC` is Circle's bridged euro-coin (a major),
`MENY` is unverified, `BXA` is a bare token. An honest floor for the snapshot, not a discovery failure.

### Shared-codebase families (one flaw implicates all members)

| Family | Size | Chain | Linked by | Combined liq | Members |
|:--|--:|:--|:--|--:|:--|
| **FAM01** | 20 | bsc | shared implementation (`FlapTaxTokenV3`, EIP-1167) | $6.80M | 逆袭人生, MarsCoin, 金蝶圣甲, QLM, 币有, Asian games, BoLe, CETS, CBURN, 暴躁牛, SUMMER, Max, VenusCoin, Marvin, Spark, gongsheng, ASTEROID, PIZZA, utility, bStocks |
| **FAM02** | 10 | bsc | shared implementation (beacon proxy) | $6.84M | SPCXB, QQQB, SKHYB, NVDAB, GMEB, GOOGLB, AAPLB, SPYB, TSLAB, MSFTB |
| **FAM04** | 3 | eth | identical bytecode + source | $6.99M | ELMT, GIVE, SWITCH |
| **FAM03** | 2 | eth | same deployer | $15.22M | strUSD, trUSD |
| **FAM05** | 2 | eth | identical bytecode + source | $3.95M | GULD, CDXR |

Beyond these **exact** clone-sets, the ETH `USDe`-fork lineage (FAM03 + sUSDat/apyUSD/apxUSD) and the
Backed-RWA template are **template lineages**: separate deployments of a shared codebase that structural
clustering keeps apart (renamed/recompiled → different bytecode/source/deployer) but that inherit risk
together. No family spans more than one chain in this snapshot.

### Already-exploited cross-check (validation, not prediction)

Two BSC contracts were **exploited during the candidate window** — evidence this population is the right
one to watch, and that the true sink is often a *satellite* contract, not the traded token:
- **STY / Swan Treasury — 2026-07-30, ~$625K.** A leaked off-chain signer key hardcoded as `_signer` in
  the paired **ZhaiquanBuy** contract let an attacker forge signatures, buy ~687k STY at a 100× discount,
  and exit via the STY/USDT pool. Vulnerable code was in ZhaiquanBuy, **not** the STY token.
- **CDAO / Crypto DAO — 2026-07-28, ~$52K.** Missing access control on publicly-callable vault functions
  of the paired **`Pro`** token. Again the sink was the paired contract.

### Excluded — inflated / circular liquidity (headline USD is not real money)

The quote-side guard removed 8 contracts whose headline liquidity is a one-sided pool priced off a
worthless token. The two largest impersonate major assets with a shared `MintBurnTeamToken` template.

| Chain | Symbol | Address | Headline | Real quote-side | Contract |
|:--|:--|:--|--:|--:|:--|
| eth | TAO | `0x819Cef100B177529035D035434CbAc49Fa9660cE` | $2,148,113,384 | **$0** | MintBurnTeamToken |
| eth | HBAR | `0xEA7b2FC6Df1294732B8cf1F95c27b05e6e990E9b` | $1,449,620,085 | **$0** | MintBurnTeamToken |
| eth | TRUU | `0xeE41ED87afAb2682F5688714499EbF4fa5c6fF19` | $3,096,541 | $0 | Truth |
| eth | CHL | `0x0F3ae93C6813cc85C9797b683ff1Db93Ade20F7D` | $3,096,330 | $0 | ChonceIIoon |
| eth | WIN | `0xb10CB07CA2CDac77FbB5707f6690301f9d036F45` | $2,161,020 | $18,058 | Token |
| bsc | BABAB | `0x4eF9d3062c7F6ebA4AAE4990c5036598C6eff4ec` | $139,424 | $35,636 | BeaconProxy |
| base | vAPI | `0xe9f78bCAaA75673f270FdC3FfE4deF7E7Fc6c502` | $281,928 | $1 | TokenERC20 |
| base | xtoken | `0xe0c48Bfa530e3993FFD1a9202E4022327643E15F` | $113,724 | $3,577 | XTokenProxy |

---

## Method — each source in the role it is trustworthy for

| Source | Role |
|:--|:--|
| **GeckoTerminal** | Chain-wide **pool enumeration** (address index only). Never a reported metric. |
| **DEXScreener** | **Source of record** for every liquidity / age / name / socials figure. |
| **Etherscan V2** (per-chain) | Verified **source + ABI** (logic), **bytecode** (clone detection), **creation tx** (deployer). |
| **GoPlus** | Per-token safety flags (honeypot / mintable / pausable / owner concentration). |

Pipeline: enumerate pools → read liquidity+age from DEXScreener → keep pairs with **liquidity ≥ $100k and
pool age < 60 days** → for each distinct non-major base token, pull the verified contract and **classify
custom-logic vs bare token** → apply the **quote-side liquidity guard** → cluster into shared-codebase
families → score by exploit-likelihood. Scripts run in order: `discover_multi.py` → `enrich_multi.py` →
`analyze_multi.py` (per chain), then `rank_report.py` across all four. The BNB Chain tier comes from the
prior committed run (`scripts/discover.py … final_output.py`), integrated as-is.

**The classifier** excludes view/pure functions and ERC-20/ownership boilerplate, and confirms
"admin-only" by locating each function in the source and reading its modifiers (an ABI does not encode
access control). Proxies are resolved to their implementation and the **merged surface** is classified.

**Family clustering** is union-find over four structural keys — shared **implementation** address,
**identical runtime bytecode** (metadata-stripped), **identical normalised source**, and same
**deployer**. A proxy's own bytecode is the generic OZ shell and is *excluded* from bytecode-clustering
(it would falsely merge thousands of unrelated projects); the canonical CREATE2 factory is excluded from
deployer-clustering for the same reason.

**Exploit-likelihood score** (ordinal, additive, weights shown so it can be argued with): fund-ops +12,
controls reserve/treasury/pool/vault +10, swappable/upgradeable logic +14, cross-chain/bridge +8,
signature-gated +8, admin fund-mover (rescue/sweep/drain) +10, treasury/pool/signer setters +6, lifecycle
+5, custom-surface breadth ≤+12, unverified implementation behind a proxy +10, **shared-codebase family
blast radius** up to +35, real quote-side liquidity (log) ≤+6, recency ≤+6, plus GoPlus flags. Confirmed
honeypots are set **aside** (scam-on-buyers, not a contract-exploit victim); an already-exploited contract
is flagged as validation, not scored as a prediction.

**Per-chain capability note.** On the free Etherscan V2 key, Ethereum and Arbitrum expose `getsourcecode`
+ `eth_getCode` + `getcontractcreation`; **Base and BNB Chain expose only `getsourcecode`**. Base bytecode
(→ clone detection) is recovered via a public RPC; Base/BSC **deployer clustering is unavailable** and
those families rest on implementation / source / bytecode overlap.

---

## Honest coverage — and what this is structurally blind to

This comes at the space from several directions and still will not catch all of it:

1. **Pool-centric net.** A protocol is only visible if it has a GeckoTerminal-indexed spot pool. Lending
   markets, perp venues, vaults and bridges that hold real TVL but have **no traded token** do not appear
   here at all. This is the single largest blind spot.
2. **The exploitable contract is often not the traded token.** In both confirmed BSC exploits the
   vulnerable code sat in a *paired* buy/vault contract, not the token this net classifies. And the ETH
   staking vaults' real value is their **TVL**, not the DEX pool. The net points at the token; enumerating
   its satellites (presale, vault, router, treasury) is the mapping step's job by design.
3. **Enumeration recency bias.** GeckoTerminal `new_pools` reaches only ~2h back; older-but-recent pools
   are recovered via top-pools / quote-token / per-DEX sorts by **current** volume, so a 40-day-old pool
   with $150k liquidity but little present volume can be missed.
4. **Reduced DEX-tail coverage on ETH/Arbitrum/Base.** To stay within GeckoTerminal's ~30 req/min limit,
   the exhaustive shallow-all-DEXes pass used on BSC was dropped for the other three chains; venues beyond
   the top ~8 + the chain-wide feeds are under-sampled there.
5. **Verified-source dependency.** Unverified contracts cannot be logic-classified and are set aside as
   *unanalyzable* (6 on Base, 1 on Arbitrum, plus the BSC set) — bytecode still lets us fingerprint/cluster
   them, but not read their logic.
6. **Deployer clustering is ETH/Arbitrum-only** (Base/BSC free-key limitation, above).
7. **Point-in-time snapshot** (2026-08-15). Liquidity and age are as-of this run; pools drain and projects
   migrate.
8. **No live/behavioural intel.** This is a static shape-and-liquidity screen, not a mempool or real-time
   alert feed.
9. **Four chains only.** Polygon, Optimism, and others are out of scope.

**The ceiling.** A risk-ranking of a population, not a prediction about any individual contract. It exists
to prioritise the mapping/audit step, not to certify any target.

---

## Outputs

| File | Contents |
|:--|:--|
| `data/exploit_candidates_ranked.csv` | **The deliverable** — 127 ranked candidates, all four chains, every signal column (score, real/headline liquidity, age, custom-logic categories, family, deployer, bytecode/source fingerprint, exploit status). |
| `data/families.json` | Shared-codebase families with members, plus the inflated-liquidity and honeypot exclusion lists. |
| `data/report_tables.md` | The tables above, regenerated on each run. |
| `data/analysis_{eth,arbitrum,base}.json` | Per-chain classifier output (kept + unanalyzable). |
| `data/bsc_contract_logic.csv` | BNB Chain tier (prior run), integrated here. |
| `scripts/` | `discover_multi` · `enrich_multi` · `analyze_multi` · `rank_report` (+ the original BSC pipeline). |

Consume `exploit_candidates_ranked.csv` top-down; for any family, auditing one member covers the shared
code for all. For the staking-vault and paired-contract cases, pull the **satellite/vault** contract —
that is where the money and the bug usually are.
