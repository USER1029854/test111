# Exploit-candidate reference — per-candidate blocks

Snapshot **2026-08-15**. 127 custom-logic candidates across four chains, ranked by exploit-likelihood score. Each block is self-contained — copy one to hand a single target into the mapping/audit step.

> Risk-ranking of a population, not a prediction about any individual contract. Every value traces to on-chain / DEXScreener data captured in `data/`. `Real liq` is the **quote-side** reserve (real external money), not the headline. For staking-vault / paired-contract cases the real value at risk is the **satellite/vault TVL**, which the mapping step must pull separately.

## Index
- **Ethereum** (28): #1 strUSD, #2 sUSDat, #3 trUSD, #4 STRCx, #5 FXRP, #10 ALBRH, #17 apyUSD, #22 CADD, #29 apxUSD, #58 frxUSD, #60 BBTC, #64 PRISM, #70 FWA, #86 ETHFI, #87 USDe, #88 syrupUSDG, #93 GREEN, #94 H, #98 CDXR, #101 PRD, #102 usocks, #103 ELMT, #104 SWITCH, #107 GIVE, #112 GULD, #115 NES, #117 RALLY, #121 rETH
- **BNB Chain** (95): #6 RT, #7 MC, #8 ZT, #9 AUV, #11 APEX, #12 TKN, #13 RICH, #14 XAUt, #15 AFW, #16 SPCXB, #18 GMEB, #19 MarsCoin, #20 逆袭人生, #21 NVDAB, #23 Asian games, #24 CBURN, #25 金蝶圣甲, #26 GOOGLB, #27 CETS, #28 币有, #30 SUMMER, #31 AFF, #32 QQQB, #33 SKHYB, #34 utility, #35 TSLAB, #36 Marvin, #37 VenusCoin, #38 暴躁牛, #39 Max, #40 bStocks, #41 AAPLB, #42 gongsheng, #43 Spark, #44 ASTEROID, #45 PIZZA, #46 BoLe, #47 QLM, #48 AIGO, #49 VTA, #50 MSFTB, #51 SPYB, #52 HAKE, #53 PEPGEM, #54 功夫女足, #55 GD, #56 67, #57 STY, #59 COSM, #61 DBURN, #62 MAME, #63 ALD, #65 SLC, #66 BF, #67 DS, #68 LC, #69 VL, #72 CSC, #73 JACKET, #74 DOS, #75 JF, #76 SpaceXcoin, #78 NEX, #80 YH, #81 宇树机器人, #82 MIZU, #83 ZX, #84 CDAO, #85 SpaceXcoin, #90 Romantic, #91 BRC, #92 WROON, #95 MC, #96 喵喵币, #97 SFIG, #99 SST, #100 FCO, #105 BTCΞ, #106 WG, #108 CZ, #109 v€, #110 O, #111 BFC, #113 币安宇宙, #114 EP, #116 US, #118 BBD, #119 SPX, #120 关山月, #122 CZ, #123 GPU, #124 GOGOGO, #125 TCC, #126 9, #127 bibi
- **Base** (3): #77 VANRY, #79 HALO, #89 TAOT
- **Arbitrum** (1): #71 DUCT

---

## #1 · strUSD · Ethereum · score 80.8
*Staked trUSD*

- **Chain:** Ethereum
- **Token address:** `0x280839980a7eD0D7717F64125fE241012E5F5815`  ·  [explorer](https://etherscan.io/address/0x280839980a7eD0D7717F64125fE241012E5F5815)
- **Liquidity:** $9,759,221 real quote-side  (headline $10,068,446)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 30 days (≈ deployed 2026-07-17)
- **Custom logic:** impl/contract `StakedTrUSD` — **fund ops, admin treasury pool signer, admin token mover, lifecycle ops, proxy upgrade, admin config gated**
  - key fns → fund: `acceptDefaultAdminTransfer`, `beginDefaultAdminTransfer`, `cancelDefaultAdminTransfer`, `deposit`, `mint`, `redeem`, `redistributeLockedAmount`, `transferInRewards`, `unstake`, `withdraw` · upgrade: `upgradeToAndCall` · fund-mover: `acceptDefaultAdminTransfer`, `beginDefaultAdminTransfer`, `cancelDefaultAdminTransfer`, `rescueOrphanFunds`, `rescueSiloTokens`, `rescueTokens`, `seizeCooldown`
- **Controls reserve/treasury/pool/vault:** yes
- **Proxy / swappable logic:** eip1967 → impl `0x521e98ba48e58d34293d9628e76c1b6e366906ff` (verified)
- **Shared codebase:** **FAM03** — shares a codebase with 1 other(s) via *same_deployer*. A flaw here is a flaw in all 2 members.
  - siblings: trUSD `0xd0580192E98eA6CEB9c7b6191Ed2E27560911697` (eth)
- **Deployer:** `0xb5afef3ae424336de90ec1127ff7fec239b02b72`
- **Market:** curve · quote trUSD · pair `0x25a637C80AD90177d0B3fF28aa2D3F74F7165ccb` · [DexScreener](https://dexscreener.com/ethereum/0x25a637C80AD90177d0B3fF28aa2D3F74F7165ccb)
- **Holders:** 152
- **Why (score 80.8):** fund_ops+12 controls_reserve+10 swappable_logic+14 admin_mover+10 admin_setters+6 lifecycle+5 surface_breadth+12 family_x2+2.8 liquidity+6 recency+3

## #2 · sUSDat · Ethereum · score 72.1
*Staked USDat*

- **Chain:** Ethereum
- **Token address:** `0xD166337499E176bbC38a1FBd113Ab144e5bd2Df7`  ·  [explorer](https://etherscan.io/address/0xD166337499E176bbC38a1FBd113Ab144e5bd2Df7)
- **Liquidity:** $109,327 real quote-side  (headline $379,578)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 11 days (≈ deployed 2026-08-05)
- **Custom logic:** impl/contract `StakedUSDat` — **fund ops, sig gated, admin treasury pool signer, admin token mover, lifecycle ops, proxy upgrade, admin config gated**
  - key fns → fund: `burnQueuedShares`, `claim`, `claimBatch`, `deposit`, `depositWithMinShares`, `depositWithPermit`, `mint`, `mintWithMaxAssets`, `mintWithPermit`, `redistributeLockedAmount`, `requestRedeem`, `setDepositFee`, `setMaxRewardsBps`, `transferInRewards` · upgrade: `upgradeToAndCall` · fund-mover: `rescueTokens` · sig: `depositWithPermit`, `mintWithPermit`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0x2005e0ca201a37694125ff267ae57872bea0a0ce` (verified)
- **Shared codebase:** No exact-clone family, but this is a **Ethena USDe/sUSDe staking-vault fork** — a *template lineage*: separate deployments of a shared codebase that inherit risk together (see README).
- **Deployer:** `0x8cba689b49f15e0a3c8770496df8e88952d6851d`
- **Market:** uniswap · quote apxUSD · pair `0xb3511fc5f98c6d924e80ff4ef400baba00aacb9fb019eafc99ed8450275bc0d7` · [DexScreener](https://dexscreener.com/ethereum/0xb3511fc5f98c6d924e80ff4ef400baba00aacb9fb019eafc99ed8450275bc0d7)
- **Holders:** 1109
- **Why (score 72.1):** fund_ops+12 swappable_logic+14 sig_gated+8 admin_mover+10 admin_setters+6 lifecycle+5 surface_breadth+12 liquidity+0.2 recency+4.9

## #3 · trUSD · Ethereum · score 67.2

- **Chain:** Ethereum
- **Token address:** `0xd0580192E98eA6CEB9c7b6191Ed2E27560911697`  ·  [explorer](https://etherscan.io/address/0xd0580192E98eA6CEB9c7b6191Ed2E27560911697)
- **Liquidity:** $5,150,309 real quote-side
- **Age / qualified by:** 30 days (≈ deployed 2026-07-17)
- **Custom logic:** impl/contract `TrUSD` — **fund ops, admin treasury pool signer, admin token mover, lifecycle ops, proxy upgrade, admin config gated**
  - key fns → fund: `acceptDefaultAdminTransfer`, `beginDefaultAdminTransfer`, `burn`, `burnFrom`, `cancelDefaultAdminTransfer`, `mint`, `setMinter` · upgrade: `upgradeToAndCall` · fund-mover: `acceptDefaultAdminTransfer`, `beginDefaultAdminTransfer`, `cancelDefaultAdminTransfer`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0xb1d133fe29255eb4ac9b05d647d49cd7f05ff631` (verified)
- **Shared codebase:** **FAM03** — shares a codebase with 1 other(s) via *same_deployer*. A flaw here is a flaw in all 2 members.
  - siblings: strUSD `0x280839980a7eD0D7717F64125fE241012E5F5815` (eth)
- **Deployer:** `0xb5afef3ae424336de90ec1127ff7fec239b02b72`
- **Market:** curve · quote USDC · pair `0xb723a224c9ACF3891B20437B4d55dd45600F5FA3` · [DexScreener](https://dexscreener.com/ethereum/0xb723a224c9ACF3891B20437B4d55dd45600F5FA3)
- **Holders:** 330
- **Why (score 67.2):** fund_ops+12 swappable_logic+14 admin_mover+10 admin_setters+6 lifecycle+5 surface_breadth+8.4 family_x2+2.8 liquidity+6 recency+3

## #4 · STRCx · Ethereum · score 67.1
*Strategy PP Variable xStock*

- **Chain:** Ethereum
- **Token address:** `0x1Aad217B8F78dbA5E6693460e8470F8b1A3977f3`  ·  [explorer](https://etherscan.io/address/0x1Aad217B8F78dbA5E6693460e8470F8b1A3977f3)
- **Liquidity:** $2,739,718 real quote-side  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 17 days (≈ deployed 2026-07-30)
- **Custom logic:** impl/contract `BackedAutoFeeTokenImplementation` — **fund ops, sig gated, admin treasury pool signer, lifecycle ops, proxy upgrade, admin config gated**
  - key fns → fund: `burn`, `mint`, `setBurner`, `setMinter` · upgrade: `upgradeTo`, `upgradeToAndCall` · sig: `delegatedTransfer`, `delegatedTransferShares`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0x65c40d624af3b18c109fbf87b7deff34cdc5f19b` (verified)
- **Shared codebase:** No exact-clone family, but this is a **Backed Finance tokenised-RWA template** — a *template lineage*: separate deployments of a shared codebase that inherit risk together (see README).
- **Deployer:** `0x5f7a4c11bde4f218f0025ef444c369d838ffa2ad`
- **Market:** uniswap · quote UDS · pair `0xee0703f70ee7b617b59c4c360cdb0441db6967584cb3f04f3024e093b8b21657` · [DexScreener](https://dexscreener.com/ethereum/0xee0703f70ee7b617b59c4c360cdb0441db6967584cb3f04f3024e093b8b21657)
- **Holders:** 2668
- **Why (score 67.1):** fund_ops+12 swappable_logic+14 sig_gated+8 admin_setters+6 lifecycle+5 surface_breadth+12 liquidity+5.8 recency+4.3

## #5 · FXRP · Ethereum · score 64.1

- **Chain:** Ethereum
- **Token address:** `0xCE6170EA245dC8D1f275A710a062b70f125F0110`  ·  [explorer](https://etherscan.io/address/0xCE6170EA245dC8D1f275A710a062b70f125F0110)
- **Liquidity:** $2,926,375 real quote-side  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 18 days (≈ deployed 2026-07-28)
- **Custom logic:** impl/contract `FXRPOFT` — **fund ops, admin treasury pool signer, bridge ops, lifecycle ops, proxy upgrade**
  - key fns → fund: `withdrawFees` · upgrade: `upgradeTo`, `upgradeToAndCall` · bridge: `lzReceive`, `lzReceiveAndRevert`, `lzReceiveSimulate`, `send`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0x0baf2d2108ea856514136c97612646623a76d024` (verified)
- **Shared codebase:** No exact-clone family, but this is a **LayerZero OFT (cross-chain) template** — a *template lineage*: separate deployments of a shared codebase that inherit risk together (see README).
- **Deployer:** `0xcc52d45087b11b4fdffd1d50fab93d96c467ac12`
- **Market:** uniswap · quote RLUSD · pair `0x42271FcA1FA435B176D46a5544B2698a1E261782` · [DexScreener](https://dexscreener.com/ethereum/0x42271FcA1FA435B176D46a5544B2698a1E261782)
- **Holders:** 69
- **Why (score 64.1):** fund_ops+12 swappable_logic+14 bridge+8 admin_setters+6 lifecycle+5 surface_breadth+9 liquidity+5.9 recency+4.2

## #6 · RT · BNB Chain · score 63.9

- **Chain:** BNB Chain
- **Token address:** `0x82BbE7f1864279fc9604267509D6BAe946333919`  ·  [explorer](https://bscscan.com/address/0x82BbE7f1864279fc9604267509D6BAe946333919)
- **Liquidity:** $236,778 real quote-side  (headline $236,779)
- **Age / qualified by:** 6 days (≈ deployed 2026-08-10)
- **Custom logic:** impl/contract `MainToken` — **fund ops, admin treasury pool signer, admin token mover, lifecycle ops, admin config gated**
  - key fns → fund: `batchSetUserMintValue`, `burnFromPoolToWealth`, `emergencyWithdraw`, `mint`, `setDistributionPercents`, `setMintStartTime`, `setMintingEnabled`, `setUsdtDistributionPercents`, `setUserMintValue` · fund-mover: `emergencyWithdraw`
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0x38CdC7D3A751e5276aE874C9c4114b7876A143c9` · [DexScreener](https://dexscreener.com/bsc/0x38CdC7D3A751e5276aE874C9c4114b7876A143c9)
- **Safety flags:** pausable|blacklist_fn
- **Holders:** 1033
- **Why (score 63.9):** fund_ops+12 controls_reserve+10 admin_mover+10 admin_setters+6 lifecycle+5 surface_breadth+12 liquidity+1.5 recency+5.4 pausable+2

## #7 · MC · BNB Chain · score 62.3

- **Chain:** BNB Chain
- **Token address:** `0x5892B6EE1adEeb7d6169FCB052cfcF6bBc253139`  ·  [explorer](https://bscscan.com/address/0x5892B6EE1adEeb7d6169FCB052cfcF6bBc253139)
- **Liquidity:** $281,749 real quote-side  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 6 days (≈ deployed 2026-08-10)
- **Custom logic:** impl/contract `SubToken` — **fund ops, admin treasury pool signer, admin token mover, lifecycle ops, admin config gated**
  - key fns → fund: `emergencyWithdraw`, `mintByMainToken`, `mintToClaimContract`, `setSubTokenClaim` · fund-mover: `emergencyWithdraw`
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote RT · pair `0x4Cb1B8B701Cd46Bdf8b8CeB78459acbFD842E4fF` · [DexScreener](https://dexscreener.com/bsc/0x4Cb1B8B701Cd46Bdf8b8CeB78459acbFD842E4fF)
- **Safety flags:** blacklist_fn
- **Holders:** 168
- **Why (score 62.3):** fund_ops+12 controls_reserve+10 admin_mover+10 admin_setters+6 lifecycle+5 surface_breadth+12 liquidity+1.8 recency+5.5

## #8 · ZT · BNB Chain · score 62.3

- **Chain:** BNB Chain
- **Token address:** `0xDd1667eC26684D62B43958D7f161540318720839`  ·  [explorer](https://bscscan.com/address/0xDd1667eC26684D62B43958D7f161540318720839)
- **Liquidity:** $267,767 real quote-side  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 24 days (≈ deployed 2026-07-23)
- **Custom logic:** impl/contract `ZT` — **fund ops, admin treasury pool signer, admin token mover, lifecycle ops, admin config gated**
  - key fns → fund: `claim`, `claimBurnDividendTrackerToken`, `claimLPDividendTrackerToken`, `claimToken`, `multiExcludeFromBurnDividends`, `processBurnDividendTracker`, `setBurnClaimWait`, `setBurnMinimumTokenBalanceForDividends`, `setLPClaimWait`, `setRemoveLpBurnInterval`, `setRemoveLpBurnTiers` · fund-mover: `setAirdropNumbs`
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote FIST · pair `0x92f9f7909852E0B9F20C56c481B18010562d034A` · [DexScreener](https://dexscreener.com/bsc/0x92f9f7909852E0B9F20C56c481B18010562d034A)
- **Safety flags:** pausable|blacklist_fn
- **Holders:** 4453
- **Why (score 62.3):** fund_ops+12 controls_reserve+10 admin_mover+10 admin_setters+6 lifecycle+5 surface_breadth+12 liquidity+1.7 recency+3.6 pausable+2

## #9 · AUV · BNB Chain · score 61.2

- **Chain:** BNB Chain
- **Token address:** `0x59523E38727C2F4E6DABe89dB938779058F2aDAf`  ·  [explorer](https://bscscan.com/address/0x59523E38727C2F4E6DABe89dB938779058F2aDAf)
- **Liquidity:** $10,083,509 real quote-side  (headline $10,083,603)
- **Age / qualified by:** 28 days (≈ deployed 2026-07-19)
- **Custom logic:** impl/contract `AUVToken` — **fund ops, admin treasury pool signer, lifecycle ops, admin config gated**
  - key fns → fund: `mintNodeEmission`, `mintStakingEmission`, `setStakingIncentivePool`
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0x54fCD38Ec2f421bBD8d508d3c335b5c39952060f` · [DexScreener](https://dexscreener.com/bsc/0x54fCD38Ec2f421bBD8d508d3c335b5c39952060f)
- **Safety flags:** pausable|hidden_owner
- **Holders:** 12705
- **Why (score 61.2):** fund_ops+12 controls_reserve+10 admin_setters+6 lifecycle+5 surface_breadth+12 liquidity+6 recency+3.2 pausable+2 hidden_owner+5

## #10 · ALBRH · Ethereum · score 60.5
*Alberich Token*

- **Chain:** Ethereum
- **Token address:** `0x7AdbFd873084dB714A57eD648ee69Aa4627Cb998`  ·  [explorer](https://etherscan.io/address/0x7AdbFd873084dB714A57eD648ee69Aa4627Cb998)
- **Liquidity:** $276,702 real quote-side  (headline $276,810)
- **Age / qualified by:** 3 days (≈ deployed 2026-08-12)
- **Custom logic:** impl/contract `AlberichToken` — **fund ops, admin token mover, lifecycle ops, admin config gated**
  - key fns → fund: `claimVestedTokens`, `ringForgedBurn`, `setMinTokensPerPurchase`, `setStakingContract`, `toggleStakingBonusRequirement`, `withdrawETH` · fund-mover: `rescueERC20`
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Deployer:** `0x5ea66460054fbe95ecb1336e23376d4965b83389`
- **Market:** uniswap · quote USDC · pair `0xD227D3D4602F4037839Fff79dC5fD80e9cC45B4E` · [DexScreener](https://dexscreener.com/ethereum/0xD227D3D4602F4037839Fff79dC5fD80e9cC45B4E)
- **Safety flags:** pausable|hidden_owner
- **Holders:** 82
- **Why (score 60.5):** fund_ops+12 controls_reserve+10 admin_mover+10 lifecycle+5 surface_breadth+9 liquidity+1.8 recency+5.7 pausable+2 hidden_owner+5

## #11 · APEX · BNB Chain · score 57.0

- **Chain:** BNB Chain
- **Token address:** `0xC2d2DfBf9A7F27138Ee32b9a4C17a2E5233aAAAA`  ·  [explorer](https://bscscan.com/address/0xC2d2DfBf9A7F27138Ee32b9a4C17a2E5233aAAAA)
- **Liquidity:** $284,707 real quote-side
- **Age / qualified by:** 60 days (≈ deployed 2026-06-17)
- **Custom logic:** impl/contract `APEX` — **fund ops, admin treasury pool signer, admin token mover, lifecycle ops, admin config gated**
  - key fns → fund: `addTotalRewards`, `setVault` · fund-mover: `rescueERC20`, `rescueETH`
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote WBNB · pair `0x4366cA77B9B561aC2EE7A683F6088a368d900Bf8` · [DexScreener](https://dexscreener.com/bsc/0x4366cA77B9B561aC2EE7A683F6088a368d900Bf8)
- **Safety flags:** pausable
- **Holders:** 51295
- **Why (score 57.0):** fund_ops+12 controls_reserve+10 admin_mover+10 admin_setters+6 lifecycle+5 surface_breadth+10.2 liquidity+1.8 pausable+2

## #12 · TKN · BNB Chain · score 56.6
*Terra Kinetic Network*

- **Chain:** BNB Chain
- **Token address:** `0xc626AD09B1c30B556705741731879EE95d7C9939`  ·  [explorer](https://bscscan.com/address/0xc626AD09B1c30B556705741731879EE95d7C9939)
- **Liquidity:** $179,423 real quote-side  (headline $179,426)
- **Age / qualified by:** 22 days (≈ deployed 2026-07-25)
- **Custom logic:** impl/contract `TKNToken` — **fund ops, admin treasury pool signer, admin token mover, admin config gated**
  - key fns → fund: `burn`, `burnFrom`, `emergencyWithdraw`, `executeDailyLPBurn` · fund-mover: `emergencyWithdraw`
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote WBNB · pair `0xd91D7B5c971202eE2693Ad30b217CDad0009e33D` · [DexScreener](https://dexscreener.com/bsc/0xd91D7B5c971202eE2693Ad30b217CDad0009e33D)
- **Safety flags:** mintable
- **Holders:** 829
- **Why (score 56.6):** fund_ops+12 controls_reserve+10 admin_mover+10 admin_setters+6 surface_breadth+10.8 liquidity+1 recency+3.8 mintable+3

## #13 · RICH · BNB Chain · score 56.0

- **Chain:** BNB Chain
- **Token address:** `0x7a128ff06283307C8492D92fa7961Ad6253E765d`  ·  [explorer](https://bscscan.com/address/0x7a128ff06283307C8492D92fa7961Ad6253E765d)
- **Liquidity:** $3,699,974 real quote-side  (headline $3,699,974)
- **Age / qualified by:** 32 days (≈ deployed 2026-07-14)
- **Custom logic:** impl/contract `RichToken` — **fund ops, admin treasury pool signer, lifecycle ops, admin config gated**
  - key fns → fund: `recycle`, `recycleGame`, `setStaking`
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0xcc27A355f473993b496D45A4c0260f350f366592` · [DexScreener](https://dexscreener.com/bsc/0xcc27A355f473993b496D45A4c0260f350f366592)
- **Safety flags:** pausable|hidden_owner|blacklist_fn
- **Holders:** 880
- **Why (score 56.0):** fund_ops+12 controls_reserve+10 admin_setters+6 lifecycle+5 surface_breadth+7.2 liquidity+6 recency+2.8 pausable+2 hidden_owner+5

## #14 · XAUt · BNB Chain · score 55.8
*Tether Gold*

- **Chain:** BNB Chain
- **Token address:** `0x21cAef8A43163Eea865baeE23b9C2E327696A3bf`  ·  [explorer](https://bscscan.com/address/0x21cAef8A43163Eea865baeE23b9C2E327696A3bf)
- **Liquidity:** $236,173 real quote-side
- **Age / qualified by:** 19 days (≈ deployed 2026-07-28)
- **Custom logic:** impl/contract `TransparentUpgradeableProxy` — **fund ops, sig gated, bridge ops, lifecycle ops, admin config gated**
  - key fns → fund: `crosschainBurn`, `crosschainMint`, `mint`, `redeem` · bridge: `crosschainBurn`, `crosschainMint` · sig: `cancelAuthorization`, `receiveWithAuthorization`, `transferWithAuthorization`
- **Controls reserve/treasury/pool/vault:** yes
- **Proxy / swappable logic:** eip1967 → impl `0x9151434b16b9763660705744891fa906f660ecc5` (verified)
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote BTCB · pair `0x10e8d7A9e36cBf06e5070f61c73bc67132dEB2ff` · [DexScreener](https://dexscreener.com/bsc/0x10e8d7A9e36cBf06e5070f61c73bc67132dEB2ff)
- **Holders:** 14367
- **Why (score 55.8):** fund_ops+12 controls_reserve+10 bridge+8 sig_gated+8 lifecycle+5 surface_breadth+7.2 liquidity+1.5 recency+4.1

## #15 · AFW · BNB Chain · score 55.4

- **Chain:** BNB Chain
- **Token address:** `0x398033B5c6c362ed1fDC9d0A66aAb359769A0C4b`  ·  [explorer](https://bscscan.com/address/0x398033B5c6c362ed1fDC9d0A66aAb359769A0C4b)
- **Liquidity:** $748,684 real quote-side  (headline $749,012)
- **Age / qualified by:** 53 days (≈ deployed 2026-06-23)
- **Custom logic:** impl/contract `AFW` — **fund ops, admin treasury pool signer, proxy upgrade, admin config gated**
  - key fns → fund: `burnDay`, `setBurnInfo`, `withdrawEthToken` · upgrade: `setCodeInfo`
- **Controls reserve/treasury/pool/vault:** yes
- **Proxy / swappable logic:** custom_setImplementation → impl `?` ()
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote WBNB · pair `0xC6EA899c6D3B5869786983A9A29e3c380202CC40` · [DexScreener](https://dexscreener.com/bsc/0xC6EA899c6D3B5869786983A9A29e3c380202CC40)
- **Safety flags:** hidden_owner
- **Holders:** 3778
- **Why (score 55.4):** fund_ops+12 controls_reserve+10 swappable_logic+14 admin_setters+6 surface_breadth+4.2 liquidity+3.5 recency+0.7 hidden_owner+5

## #16 · SPCXB · BNB Chain · score 54.0
*SpaceX*

- **Chain:** BNB Chain
- **Token address:** `0xbe9D156892E55e7154BcD3cB0FEA677F9D3103E1`  ·  [explorer](https://bscscan.com/address/0xbe9D156892E55e7154BcD3cB0FEA677F9D3103E1)
- **Liquidity:** $1,815,294 real quote-side
- **Age / qualified by:** 12 days (≈ deployed 2026-08-03)
- **Custom logic:** **fund ops, admin treasury pool signer, lifecycle ops, admin config gated**
  - key fns → fund: `burn`, `mint`, `setBurnEnabled`, `setMintEnabled`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0xcfed6c4679297ea4889f8183bc057b4a86c64e46` (verified)
- **Shared codebase:** **FAM02** — shares a codebase with 9 other(s) via *shared_implementation*. A flaw here is a flaw in all 10 members.
  - siblings: QQQB `0x205812CdBed920aFf76C6580abD681a46D11efc7` (bsc); SKHYB `0xCA750eF65f295BBECd685Abf54e82CAf297BDB61` (bsc); NVDAB `0x02Fca66C1D1aFB4E2A7884261eB00F63598a7436` (bsc); GMEB `0x46cEeFDa28Dd7207059ed19B0acdc026955bb15C` (bsc); GOOGLB `0x3F53De71c126BdaBAe20f9cD64848d317f6C3238` (bsc); AAPLB `0x431a3BEE82E2ca41e49895CbECE5bB0F76A89b7A` (bsc); SPYB `0x7138b48df7D98D7e3cc221BfE7192D0a178182D8` (bsc); TSLAB `0x5b1910eAaD6450E50f816082Aa078C41F10C292f` (bsc); MSFTB `0x80106cb3EAD06659A5ad19DF39D9b4733863B9b0` (bsc)
- **Market:** pancakeswap · quote WBNB · pair `0x66faaD27cf481f82d0089ec8156B3AA3636010C7` · [DexScreener](https://dexscreener.com/bsc/0x66faaD27cf481f82d0089ec8156B3AA3636010C7)
- **Holders:** 131598
- **Why (score 54.0):** fund_ops+12 admin_setters+6 lifecycle+5 surface_breadth+7.2 family_x10+14 liquidity+5 recency+4.8

## #17 · apyUSD · Ethereum · score 53.7

- **Chain:** Ethereum
- **Token address:** `0x38EEb52F0771140d10c4E9A9a72349A329Fe8a6A`  ·  [explorer](https://etherscan.io/address/0x38EEb52F0771140d10c4E9A9a72349A329Fe8a6A)
- **Liquidity:** $161,065 real quote-side  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 15 days (≈ deployed 2026-08-01)
- **Custom logic:** impl/contract `ApyUSD` — **fund ops, admin treasury pool signer, lifecycle ops, proxy upgrade**
  - key fns → fund: `burnWithAssets`, `burnWithAssetsFrom`, `deposit`, `depositForMinShares`, `mint`, `mintForMaxAssets`, `redeem`, `redeemForMinAssets`, `redeemForReceipt`, `withdraw`, `withdrawForMaxShares`, `withdrawForReceipt` · upgrade: `upgradeToAndCall`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0xfd616567ecc1607f61073951a1e822f7315bb112` (verified)
- **Shared codebase:** No exact-clone family, but this is a **Ethena USDe/sUSDe fork (base minter)** — a *template lineage*: separate deployments of a shared codebase that inherit risk together (see README).
- **Deployer:** `0x5db416bcfc1a8b5b921f55c1e078d1f39194e99f`
- **Market:** uniswap · quote apxUSD · pair `0x824c1c88a46e3ef82487cd785759c277c03ee935bb9cac8bb9ada6990bb3a15a` · [DexScreener](https://dexscreener.com/ethereum/0x824c1c88a46e3ef82487cd785759c277c03ee935bb9cac8bb9ada6990bb3a15a)
- **Holders:** 1274
- **Why (score 53.7):** fund_ops+12 swappable_logic+14 admin_setters+6 lifecycle+5 surface_breadth+11.4 liquidity+0.8 recency+4.5

## #18 · GMEB · BNB Chain · score 53.4
*GameStop*

- **Chain:** BNB Chain
- **Token address:** `0x46cEeFDa28Dd7207059ed19B0acdc026955bb15C`  ·  [explorer](https://bscscan.com/address/0x46cEeFDa28Dd7207059ed19B0acdc026955bb15C)
- **Liquidity:** $701,015 real quote-side  (headline $712,351)
- **Age / qualified by:** 2 days (≈ deployed 2026-08-13)
- **Custom logic:** **fund ops, admin treasury pool signer, lifecycle ops, admin config gated**
  - key fns → fund: `burn`, `mint`, `setBurnEnabled`, `setMintEnabled`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0xcfed6c4679297ea4889f8183bc057b4a86c64e46` (verified)
- **Shared codebase:** **FAM02** — shares a codebase with 9 other(s) via *shared_implementation*. A flaw here is a flaw in all 10 members.
  - siblings: SPCXB `0xbe9D156892E55e7154BcD3cB0FEA677F9D3103E1` (bsc); QQQB `0x205812CdBed920aFf76C6580abD681a46D11efc7` (bsc); SKHYB `0xCA750eF65f295BBECd685Abf54e82CAf297BDB61` (bsc); NVDAB `0x02Fca66C1D1aFB4E2A7884261eB00F63598a7436` (bsc); GOOGLB `0x3F53De71c126BdaBAe20f9cD64848d317f6C3238` (bsc); AAPLB `0x431a3BEE82E2ca41e49895CbECE5bB0F76A89b7A` (bsc); SPYB `0x7138b48df7D98D7e3cc221BfE7192D0a178182D8` (bsc); TSLAB `0x5b1910eAaD6450E50f816082Aa078C41F10C292f` (bsc); MSFTB `0x80106cb3EAD06659A5ad19DF39D9b4733863B9b0` (bsc)
- **Market:** pancakeswap · quote USDT · pair `0x908d49048EB3a7bEdfd238972403842805EAF2bE` · [DexScreener](https://dexscreener.com/bsc/0x908d49048EB3a7bEdfd238972403842805EAF2bE)
- **Holders:** 10729
- **Why (score 53.4):** fund_ops+12 admin_setters+6 lifecycle+5 surface_breadth+7.2 family_x10+14 liquidity+3.4 recency+5.8

## #19 · MarsCoin · BNB Chain · score 53.2

- **Chain:** BNB Chain
- **Token address:** `0xFe189E97832DA1573e4e4Ff034F4fFC3a15c7777`  ·  [explorer](https://bscscan.com/address/0xFe189E97832DA1573e4e4Ff034F4fFC3a15c7777)
- **Liquidity:** $1,035,422 real quote-side  (headline $1,037,209)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 17 days (≈ deployed 2026-07-29)
- **Custom logic:** impl/contract `FlapTaxTokenV3` — **lifecycle ops**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** **FAM01** — shares a codebase with 19 other(s) via *shared_implementation*. A flaw here is a flaw in all 20 members.
  - siblings: 逆袭人生 `0xceFbf00b3732FE91e46989037E4b2564a4fc7777` (bsc); 金蝶圣甲 `0x4f0c550bFe484F957D5C7Dd26f9a630a92A17777` (bsc); QLM `0x1Df197D03967eD707E5AABc2c6Cf0c0d62cb7777` (bsc); 币有 `0xe9337Dde3dd9e97f1f45A56412767ce5098E7777` (bsc); Asian games `0x31d19B3633eBdb60Dc9d690b3e9eB1FFF61A7777` (bsc); BoLe `0x5e4538460E07A12ea756fe1B774bf5C006797777` (bsc); CETS `0xB0c2aB5af4028461acE3f6e1C33a4eE1404E7777` (bsc); CBURN `0x309409237C4dB70Cd66067741eDcF02Bf69E7777` (bsc); 暴躁牛 `0x3A51dAE2Dc3D901A2cEfeD3Ad128116bf31C7777` (bsc); SUMMER `0xeEb3d73d4dd44e6E4d957d89492f05d5CCeE7777` (bsc); Max `0xe9Bc5C6A86caA44fD7b469bf3cc7c563E4F77777` (bsc); VenusCoin `0x5460b5E88799D27bbdf8A210926C17Dec18d7777` (bsc); Marvin `0xC6Bff31BbFa84d3c05AD61D8Ec47bE8B31517777` (bsc); Spark `0xC1073C967E323F2E197fA3975EC3b279974d7777` (bsc); gongsheng `0x70F7B593148283e7d84CeAB31407Bae0b5317777` (bsc); ASTEROID `0x330990DaE53BCa4C5811C5362B44C33a47db7777` (bsc); PIZZA `0x8554D38b95E4F7Ca11D391008627Df30B2b07777` (bsc); utility `0xEde00776439f9C49C592e43EeE34777a51847777` (bsc); bStocks `0x244B112Cf746e62A5DF723cbDe9906a6dEfd7777` (bsc)
- **Market:** pancakeswap · quote SPCXB · pair `0x94F3ed36706c746ad59fAdCAF271b7431AB1D8F1` · [DexScreener](https://dexscreener.com/bsc/0x94F3ed36706c746ad59fAdCAF271b7431AB1D8F1)
- **Holders:** 30843
- **Why (score 53.2):** controls_reserve+10 lifecycle+5 surface_breadth+1.8 family_x20+28 liquidity+4.1 recency+4.3

## #20 · 逆袭人生 · BNB Chain · score 53.1
*NIXI*

- **Chain:** BNB Chain
- **Token address:** `0xceFbf00b3732FE91e46989037E4b2564a4fc7777`  ·  [explorer](https://bscscan.com/address/0xceFbf00b3732FE91e46989037E4b2564a4fc7777)
- **Liquidity:** $1,856,221 real quote-side  (headline $1,857,113)
- **Age / qualified by:** 28 days (≈ deployed 2026-07-19)
- **Custom logic:** impl/contract `FlapTaxTokenV3` — **lifecycle ops**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** **FAM01** — shares a codebase with 19 other(s) via *shared_implementation*. A flaw here is a flaw in all 20 members.
  - siblings: MarsCoin `0xFe189E97832DA1573e4e4Ff034F4fFC3a15c7777` (bsc); 金蝶圣甲 `0x4f0c550bFe484F957D5C7Dd26f9a630a92A17777` (bsc); QLM `0x1Df197D03967eD707E5AABc2c6Cf0c0d62cb7777` (bsc); 币有 `0xe9337Dde3dd9e97f1f45A56412767ce5098E7777` (bsc); Asian games `0x31d19B3633eBdb60Dc9d690b3e9eB1FFF61A7777` (bsc); BoLe `0x5e4538460E07A12ea756fe1B774bf5C006797777` (bsc); CETS `0xB0c2aB5af4028461acE3f6e1C33a4eE1404E7777` (bsc); CBURN `0x309409237C4dB70Cd66067741eDcF02Bf69E7777` (bsc); 暴躁牛 `0x3A51dAE2Dc3D901A2cEfeD3Ad128116bf31C7777` (bsc); SUMMER `0xeEb3d73d4dd44e6E4d957d89492f05d5CCeE7777` (bsc); Max `0xe9Bc5C6A86caA44fD7b469bf3cc7c563E4F77777` (bsc); VenusCoin `0x5460b5E88799D27bbdf8A210926C17Dec18d7777` (bsc); Marvin `0xC6Bff31BbFa84d3c05AD61D8Ec47bE8B31517777` (bsc); Spark `0xC1073C967E323F2E197fA3975EC3b279974d7777` (bsc); gongsheng `0x70F7B593148283e7d84CeAB31407Bae0b5317777` (bsc); ASTEROID `0x330990DaE53BCa4C5811C5362B44C33a47db7777` (bsc); PIZZA `0x8554D38b95E4F7Ca11D391008627Df30B2b07777` (bsc); utility `0xEde00776439f9C49C592e43EeE34777a51847777` (bsc); bStocks `0x244B112Cf746e62A5DF723cbDe9906a6dEfd7777` (bsc)
- **Market:** pancakeswap · quote WBNB · pair `0x79cB334149a030643c26980De323b842ac981567` · [DexScreener](https://dexscreener.com/bsc/0x79cB334149a030643c26980De323b842ac981567)
- **Holders:** 26068
- **Why (score 53.1):** controls_reserve+10 lifecycle+5 surface_breadth+1.8 family_x20+28 liquidity+5.1 recency+3.2

## #21 · NVDAB · BNB Chain · score 52.3
*NVIDIA Corp*

- **Chain:** BNB Chain
- **Token address:** `0x02Fca66C1D1aFB4E2A7884261eB00F63598a7436`  ·  [explorer](https://bscscan.com/address/0x02Fca66C1D1aFB4E2A7884261eB00F63598a7436)
- **Liquidity:** $805,750 real quote-side
- **Age / qualified by:** 16 days (≈ deployed 2026-07-31)
- **Custom logic:** **fund ops, admin treasury pool signer, lifecycle ops, admin config gated**
  - key fns → fund: `burn`, `mint`, `setBurnEnabled`, `setMintEnabled`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0xcfed6c4679297ea4889f8183bc057b4a86c64e46` (verified)
- **Shared codebase:** **FAM02** — shares a codebase with 9 other(s) via *shared_implementation*. A flaw here is a flaw in all 10 members.
  - siblings: SPCXB `0xbe9D156892E55e7154BcD3cB0FEA677F9D3103E1` (bsc); QQQB `0x205812CdBed920aFf76C6580abD681a46D11efc7` (bsc); SKHYB `0xCA750eF65f295BBECd685Abf54e82CAf297BDB61` (bsc); GMEB `0x46cEeFDa28Dd7207059ed19B0acdc026955bb15C` (bsc); GOOGLB `0x3F53De71c126BdaBAe20f9cD64848d317f6C3238` (bsc); AAPLB `0x431a3BEE82E2ca41e49895CbECE5bB0F76A89b7A` (bsc); SPYB `0x7138b48df7D98D7e3cc221BfE7192D0a178182D8` (bsc); TSLAB `0x5b1910eAaD6450E50f816082Aa078C41F10C292f` (bsc); MSFTB `0x80106cb3EAD06659A5ad19DF39D9b4733863B9b0` (bsc)
- **Market:** pancakeswap · quote USDT · pair `0x8FB4243b553aC29BA088aCf00B9B7dA24bD6690C` · [DexScreener](https://dexscreener.com/bsc/0x8FB4243b553aC29BA088aCf00B9B7dA24bD6690C)
- **Holders:** 27026
- **Why (score 52.3):** fund_ops+12 admin_setters+6 lifecycle+5 surface_breadth+7.2 family_x10+14 liquidity+3.6 recency+4.5

## #22 · CADD · Ethereum · score 52.2
*CAD Digital Inc*

- **Chain:** Ethereum
- **Token address:** `0x16F93eBC5320C89EfC8701577efe49d14A276a06`  ·  [explorer](https://etherscan.io/address/0x16F93eBC5320C89EfC8701577efe49d14A276a06)
- **Liquidity:** $294,742 real quote-side  (headline $304,890)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 39 days (≈ deployed 2026-07-08)
- **Custom logic:** impl/contract `ERC20F` — **fund ops, admin token mover, lifecycle ops, proxy upgrade, admin config gated**
  - key fns → fund: `burn`, `mint` · upgrade: `upgradeTo`, `upgradeToAndCall` · fund-mover: `recoverTokens`, `salvageERC20`, `salvageGas`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0x0f25045d15c163478bb67c56c5d9d602628f4f62` (verified)
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Deployer:** `0x9367b51c7833f4ea32898079e7f4318e4f412b78`
- **Market:** curve · quote frxUSD · pair `0x384CA8992F955009Bdd94849488E580559590157` · [DexScreener](https://dexscreener.com/ethereum/0x384CA8992F955009Bdd94849488E580559590157)
- **Holders:** 103
- **Why (score 52.2):** fund_ops+12 swappable_logic+14 admin_mover+10 lifecycle+5 surface_breadth+7.2 liquidity+1.9 recency+2.1

## #23 · Asian games · BNB Chain · score 52.1

- **Chain:** BNB Chain
- **Token address:** `0x31d19B3633eBdb60Dc9d690b3e9eB1FFF61A7777`  ·  [explorer](https://bscscan.com/address/0x31d19B3633eBdb60Dc9d690b3e9eB1FFF61A7777)
- **Liquidity:** $280,692 real quote-side
- **Age / qualified by:** 5 days (≈ deployed 2026-08-10)
- **Custom logic:** impl/contract `FlapTaxTokenV3` — **lifecycle ops**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** **FAM01** — shares a codebase with 19 other(s) via *shared_implementation*. A flaw here is a flaw in all 20 members.
  - siblings: 逆袭人生 `0xceFbf00b3732FE91e46989037E4b2564a4fc7777` (bsc); MarsCoin `0xFe189E97832DA1573e4e4Ff034F4fFC3a15c7777` (bsc); 金蝶圣甲 `0x4f0c550bFe484F957D5C7Dd26f9a630a92A17777` (bsc); QLM `0x1Df197D03967eD707E5AABc2c6Cf0c0d62cb7777` (bsc); 币有 `0xe9337Dde3dd9e97f1f45A56412767ce5098E7777` (bsc); BoLe `0x5e4538460E07A12ea756fe1B774bf5C006797777` (bsc); CETS `0xB0c2aB5af4028461acE3f6e1C33a4eE1404E7777` (bsc); CBURN `0x309409237C4dB70Cd66067741eDcF02Bf69E7777` (bsc); 暴躁牛 `0x3A51dAE2Dc3D901A2cEfeD3Ad128116bf31C7777` (bsc); SUMMER `0xeEb3d73d4dd44e6E4d957d89492f05d5CCeE7777` (bsc); Max `0xe9Bc5C6A86caA44fD7b469bf3cc7c563E4F77777` (bsc); VenusCoin `0x5460b5E88799D27bbdf8A210926C17Dec18d7777` (bsc); Marvin `0xC6Bff31BbFa84d3c05AD61D8Ec47bE8B31517777` (bsc); Spark `0xC1073C967E323F2E197fA3975EC3b279974d7777` (bsc); gongsheng `0x70F7B593148283e7d84CeAB31407Bae0b5317777` (bsc); ASTEROID `0x330990DaE53BCa4C5811C5362B44C33a47db7777` (bsc); PIZZA `0x8554D38b95E4F7Ca11D391008627Df30B2b07777` (bsc); utility `0xEde00776439f9C49C592e43EeE34777a51847777` (bsc); bStocks `0x244B112Cf746e62A5DF723cbDe9906a6dEfd7777` (bsc)
- **Market:** pancakeswap · quote WBNB · pair `0xC338a9cA7577370826e8e58F096F657178Fd1b5c` · [DexScreener](https://dexscreener.com/bsc/0xC338a9cA7577370826e8e58F096F657178Fd1b5c)
- **Holders:** 6826
- **Why (score 52.1):** controls_reserve+10 lifecycle+5 surface_breadth+1.8 family_x20+28 liquidity+1.8 recency+5.5

## #24 · CBURN · BNB Chain · score 52.1
*CZBURN*

- **Chain:** BNB Chain
- **Token address:** `0x309409237C4dB70Cd66067741eDcF02Bf69E7777`  ·  [explorer](https://bscscan.com/address/0x309409237C4dB70Cd66067741eDcF02Bf69E7777)
- **Liquidity:** $236,141 real quote-side
- **Age / qualified by:** 2 days (≈ deployed 2026-08-13)
- **Custom logic:** impl/contract `FlapTaxTokenV3` — **lifecycle ops**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** **FAM01** — shares a codebase with 19 other(s) via *shared_implementation*. A flaw here is a flaw in all 20 members.
  - siblings: 逆袭人生 `0xceFbf00b3732FE91e46989037E4b2564a4fc7777` (bsc); MarsCoin `0xFe189E97832DA1573e4e4Ff034F4fFC3a15c7777` (bsc); 金蝶圣甲 `0x4f0c550bFe484F957D5C7Dd26f9a630a92A17777` (bsc); QLM `0x1Df197D03967eD707E5AABc2c6Cf0c0d62cb7777` (bsc); 币有 `0xe9337Dde3dd9e97f1f45A56412767ce5098E7777` (bsc); Asian games `0x31d19B3633eBdb60Dc9d690b3e9eB1FFF61A7777` (bsc); BoLe `0x5e4538460E07A12ea756fe1B774bf5C006797777` (bsc); CETS `0xB0c2aB5af4028461acE3f6e1C33a4eE1404E7777` (bsc); 暴躁牛 `0x3A51dAE2Dc3D901A2cEfeD3Ad128116bf31C7777` (bsc); SUMMER `0xeEb3d73d4dd44e6E4d957d89492f05d5CCeE7777` (bsc); Max `0xe9Bc5C6A86caA44fD7b469bf3cc7c563E4F77777` (bsc); VenusCoin `0x5460b5E88799D27bbdf8A210926C17Dec18d7777` (bsc); Marvin `0xC6Bff31BbFa84d3c05AD61D8Ec47bE8B31517777` (bsc); Spark `0xC1073C967E323F2E197fA3975EC3b279974d7777` (bsc); gongsheng `0x70F7B593148283e7d84CeAB31407Bae0b5317777` (bsc); ASTEROID `0x330990DaE53BCa4C5811C5362B44C33a47db7777` (bsc); PIZZA `0x8554D38b95E4F7Ca11D391008627Df30B2b07777` (bsc); utility `0xEde00776439f9C49C592e43EeE34777a51847777` (bsc); bStocks `0x244B112Cf746e62A5DF723cbDe9906a6dEfd7777` (bsc)
- **Market:** pancakeswap · quote WBNB · pair `0x0B72bf3C70531E04d58783b2DD12fb71180744De` · [DexScreener](https://dexscreener.com/bsc/0x0B72bf3C70531E04d58783b2DD12fb71180744De)
- **Holders:** 2964
- **Why (score 52.1):** controls_reserve+10 lifecycle+5 surface_breadth+1.8 family_x20+28 liquidity+1.5 recency+5.8

## #25 · 金蝶圣甲 · BNB Chain · score 51.8

- **Chain:** BNB Chain
- **Token address:** `0x4f0c550bFe484F957D5C7Dd26f9a630a92A17777`  ·  [explorer](https://bscscan.com/address/0x4f0c550bFe484F957D5C7Dd26f9a630a92A17777)
- **Liquidity:** $773,776 real quote-side
- **Age / qualified by:** 26 days (≈ deployed 2026-07-20)
- **Custom logic:** impl/contract `FlapTaxTokenV3` — **lifecycle ops**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** **FAM01** — shares a codebase with 19 other(s) via *shared_implementation*. A flaw here is a flaw in all 20 members.
  - siblings: 逆袭人生 `0xceFbf00b3732FE91e46989037E4b2564a4fc7777` (bsc); MarsCoin `0xFe189E97832DA1573e4e4Ff034F4fFC3a15c7777` (bsc); QLM `0x1Df197D03967eD707E5AABc2c6Cf0c0d62cb7777` (bsc); 币有 `0xe9337Dde3dd9e97f1f45A56412767ce5098E7777` (bsc); Asian games `0x31d19B3633eBdb60Dc9d690b3e9eB1FFF61A7777` (bsc); BoLe `0x5e4538460E07A12ea756fe1B774bf5C006797777` (bsc); CETS `0xB0c2aB5af4028461acE3f6e1C33a4eE1404E7777` (bsc); CBURN `0x309409237C4dB70Cd66067741eDcF02Bf69E7777` (bsc); 暴躁牛 `0x3A51dAE2Dc3D901A2cEfeD3Ad128116bf31C7777` (bsc); SUMMER `0xeEb3d73d4dd44e6E4d957d89492f05d5CCeE7777` (bsc); Max `0xe9Bc5C6A86caA44fD7b469bf3cc7c563E4F77777` (bsc); VenusCoin `0x5460b5E88799D27bbdf8A210926C17Dec18d7777` (bsc); Marvin `0xC6Bff31BbFa84d3c05AD61D8Ec47bE8B31517777` (bsc); Spark `0xC1073C967E323F2E197fA3975EC3b279974d7777` (bsc); gongsheng `0x70F7B593148283e7d84CeAB31407Bae0b5317777` (bsc); ASTEROID `0x330990DaE53BCa4C5811C5362B44C33a47db7777` (bsc); PIZZA `0x8554D38b95E4F7Ca11D391008627Df30B2b07777` (bsc); utility `0xEde00776439f9C49C592e43EeE34777a51847777` (bsc); bStocks `0x244B112Cf746e62A5DF723cbDe9906a6dEfd7777` (bsc)
- **Market:** pancakeswap · quote WBNB · pair `0x3E86832b28854B5C7A86E8666Ac4aB92cdA1843e` · [DexScreener](https://dexscreener.com/bsc/0x3E86832b28854B5C7A86E8666Ac4aB92cdA1843e)
- **Holders:** 12830
- **Why (score 51.8):** controls_reserve+10 lifecycle+5 surface_breadth+1.8 family_x20+28 liquidity+3.6 recency+3.4

## #26 · GOOGLB · BNB Chain · score 51.8
*Alphabet*

- **Chain:** BNB Chain
- **Token address:** `0x3F53De71c126BdaBAe20f9cD64848d317f6C3238`  ·  [explorer](https://bscscan.com/address/0x3F53De71c126BdaBAe20f9cD64848d317f6C3238)
- **Liquidity:** $546,050 real quote-side
- **Age / qualified by:** 14 days (≈ deployed 2026-08-02)
- **Custom logic:** **fund ops, admin treasury pool signer, lifecycle ops, admin config gated**
  - key fns → fund: `burn`, `mint`, `setBurnEnabled`, `setMintEnabled`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0xcfed6c4679297ea4889f8183bc057b4a86c64e46` (verified)
- **Shared codebase:** **FAM02** — shares a codebase with 9 other(s) via *shared_implementation*. A flaw here is a flaw in all 10 members.
  - siblings: SPCXB `0xbe9D156892E55e7154BcD3cB0FEA677F9D3103E1` (bsc); QQQB `0x205812CdBed920aFf76C6580abD681a46D11efc7` (bsc); SKHYB `0xCA750eF65f295BBECd685Abf54e82CAf297BDB61` (bsc); NVDAB `0x02Fca66C1D1aFB4E2A7884261eB00F63598a7436` (bsc); GMEB `0x46cEeFDa28Dd7207059ed19B0acdc026955bb15C` (bsc); AAPLB `0x431a3BEE82E2ca41e49895CbECE5bB0F76A89b7A` (bsc); SPYB `0x7138b48df7D98D7e3cc221BfE7192D0a178182D8` (bsc); TSLAB `0x5b1910eAaD6450E50f816082Aa078C41F10C292f` (bsc); MSFTB `0x80106cb3EAD06659A5ad19DF39D9b4733863B9b0` (bsc)
- **Market:** pancakeswap · quote USDT · pair `0x89001D846f7CA36EE089F73eEFC25657E1798144` · [DexScreener](https://dexscreener.com/bsc/0x89001D846f7CA36EE089F73eEFC25657E1798144)
- **Holders:** 1226
- **Why (score 51.8):** fund_ops+12 admin_setters+6 lifecycle+5 surface_breadth+7.2 family_x10+14 liquidity+2.9 recency+4.7

## #27 · CETS · BNB Chain · score 51.6
*Cets On Gold*

- **Chain:** BNB Chain
- **Token address:** `0xB0c2aB5af4028461acE3f6e1C33a4eE1404E7777`  ·  [explorer](https://bscscan.com/address/0xB0c2aB5af4028461acE3f6e1C33a4eE1404E7777)
- **Liquidity:** $252,177 real quote-side  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 8 days (≈ deployed 2026-08-08)
- **Custom logic:** impl/contract `FlapTaxTokenV3` — **lifecycle ops**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** **FAM01** — shares a codebase with 19 other(s) via *shared_implementation*. A flaw here is a flaw in all 20 members.
  - siblings: 逆袭人生 `0xceFbf00b3732FE91e46989037E4b2564a4fc7777` (bsc); MarsCoin `0xFe189E97832DA1573e4e4Ff034F4fFC3a15c7777` (bsc); 金蝶圣甲 `0x4f0c550bFe484F957D5C7Dd26f9a630a92A17777` (bsc); QLM `0x1Df197D03967eD707E5AABc2c6Cf0c0d62cb7777` (bsc); 币有 `0xe9337Dde3dd9e97f1f45A56412767ce5098E7777` (bsc); Asian games `0x31d19B3633eBdb60Dc9d690b3e9eB1FFF61A7777` (bsc); BoLe `0x5e4538460E07A12ea756fe1B774bf5C006797777` (bsc); CBURN `0x309409237C4dB70Cd66067741eDcF02Bf69E7777` (bsc); 暴躁牛 `0x3A51dAE2Dc3D901A2cEfeD3Ad128116bf31C7777` (bsc); SUMMER `0xeEb3d73d4dd44e6E4d957d89492f05d5CCeE7777` (bsc); Max `0xe9Bc5C6A86caA44fD7b469bf3cc7c563E4F77777` (bsc); VenusCoin `0x5460b5E88799D27bbdf8A210926C17Dec18d7777` (bsc); Marvin `0xC6Bff31BbFa84d3c05AD61D8Ec47bE8B31517777` (bsc); Spark `0xC1073C967E323F2E197fA3975EC3b279974d7777` (bsc); gongsheng `0x70F7B593148283e7d84CeAB31407Bae0b5317777` (bsc); ASTEROID `0x330990DaE53BCa4C5811C5362B44C33a47db7777` (bsc); PIZZA `0x8554D38b95E4F7Ca11D391008627Df30B2b07777` (bsc); utility `0xEde00776439f9C49C592e43EeE34777a51847777` (bsc); bStocks `0x244B112Cf746e62A5DF723cbDe9906a6dEfd7777` (bsc)
- **Market:** pancakeswap · quote XAUt · pair `0xdabbd019c0174BDAE6354f32b158D42e4A0E7489` · [DexScreener](https://dexscreener.com/bsc/0xdabbd019c0174BDAE6354f32b158D42e4A0E7489)
- **Holders:** 1902
- **Why (score 51.6):** controls_reserve+10 lifecycle+5 surface_breadth+1.8 family_x20+28 liquidity+1.6 recency+5.2

## #28 · 币有 · BNB Chain · score 51.5
*何必东奔西走 币安全部都有*

- **Chain:** BNB Chain
- **Token address:** `0xe9337Dde3dd9e97f1f45A56412767ce5098E7777`  ·  [explorer](https://bscscan.com/address/0xe9337Dde3dd9e97f1f45A56412767ce5098E7777)
- **Liquidity:** $309,794 real quote-side  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 13 days (≈ deployed 2026-08-02)
- **Custom logic:** impl/contract `FlapTaxTokenV3` — **lifecycle ops**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** **FAM01** — shares a codebase with 19 other(s) via *shared_implementation*. A flaw here is a flaw in all 20 members.
  - siblings: 逆袭人生 `0xceFbf00b3732FE91e46989037E4b2564a4fc7777` (bsc); MarsCoin `0xFe189E97832DA1573e4e4Ff034F4fFC3a15c7777` (bsc); 金蝶圣甲 `0x4f0c550bFe484F957D5C7Dd26f9a630a92A17777` (bsc); QLM `0x1Df197D03967eD707E5AABc2c6Cf0c0d62cb7777` (bsc); Asian games `0x31d19B3633eBdb60Dc9d690b3e9eB1FFF61A7777` (bsc); BoLe `0x5e4538460E07A12ea756fe1B774bf5C006797777` (bsc); CETS `0xB0c2aB5af4028461acE3f6e1C33a4eE1404E7777` (bsc); CBURN `0x309409237C4dB70Cd66067741eDcF02Bf69E7777` (bsc); 暴躁牛 `0x3A51dAE2Dc3D901A2cEfeD3Ad128116bf31C7777` (bsc); SUMMER `0xeEb3d73d4dd44e6E4d957d89492f05d5CCeE7777` (bsc); Max `0xe9Bc5C6A86caA44fD7b469bf3cc7c563E4F77777` (bsc); VenusCoin `0x5460b5E88799D27bbdf8A210926C17Dec18d7777` (bsc); Marvin `0xC6Bff31BbFa84d3c05AD61D8Ec47bE8B31517777` (bsc); Spark `0xC1073C967E323F2E197fA3975EC3b279974d7777` (bsc); gongsheng `0x70F7B593148283e7d84CeAB31407Bae0b5317777` (bsc); ASTEROID `0x330990DaE53BCa4C5811C5362B44C33a47db7777` (bsc); PIZZA `0x8554D38b95E4F7Ca11D391008627Df30B2b07777` (bsc); utility `0xEde00776439f9C49C592e43EeE34777a51847777` (bsc); bStocks `0x244B112Cf746e62A5DF723cbDe9906a6dEfd7777` (bsc)
- **Market:** pancakeswap · quote SPYB · pair `0x44Ea468B40ec3f9DE546Fd5Da9C3AF7A9D23833A` · [DexScreener](https://dexscreener.com/bsc/0x44Ea468B40ec3f9DE546Fd5Da9C3AF7A9D23833A)
- **Holders:** 7275
- **Why (score 51.5):** controls_reserve+10 lifecycle+5 surface_breadth+1.8 family_x20+28 liquidity+2 recency+4.7

## #29 · apxUSD · Ethereum · score 51.3

- **Chain:** Ethereum
- **Token address:** `0x98A878b1Cd98131B271883B390f68D2c90674665`  ·  [explorer](https://etherscan.io/address/0x98A878b1Cd98131B271883B390f68D2c90674665)
- **Liquidity:** $1,892,128 real quote-side  (headline $6,947,646)
- **Age / qualified by:** 16 days (≈ deployed 2026-07-31)
- **Custom logic:** impl/contract `ApxUSD` — **fund ops, admin treasury pool signer, lifecycle ops, proxy upgrade**
  - key fns → fund: `burn`, `burnFrom`, `mint` · upgrade: `upgradeToAndCall`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0xdd71fd677fde2ed2579a3c45204f41a11016ccb4` (verified)
- **Shared codebase:** No exact-clone family, but this is a **Ethena USDe/sUSDe fork (base minter)** — a *template lineage*: separate deployments of a shared codebase that inherit risk together (see README).
- **Deployer:** `0x0442cc5bbfbc4b7dc3a14f9766c21c82b45f0024`
- **Market:** curve · quote USDC · pair `0x6F63deEDc9870D6c16FC644C6654748352cdc87c` · [DexScreener](https://dexscreener.com/ethereum/0x6F63deEDc9870D6c16FC644C6654748352cdc87c)
- **Holders:** 1855
- **Why (score 51.3):** fund_ops+12 swappable_logic+14 admin_setters+6 lifecycle+5 surface_breadth+4.8 liquidity+5.1 recency+4.4

## #30 · SUMMER · BNB Chain · score 51.1

- **Chain:** BNB Chain
- **Token address:** `0xeEb3d73d4dd44e6E4d957d89492f05d5CCeE7777`  ·  [explorer](https://bscscan.com/address/0xeEb3d73d4dd44e6E4d957d89492f05d5CCeE7777)
- **Liquidity:** $183,667 real quote-side  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 8 days (≈ deployed 2026-08-07)
- **Custom logic:** impl/contract `FlapTaxTokenV3` — **lifecycle ops**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** **FAM01** — shares a codebase with 19 other(s) via *shared_implementation*. A flaw here is a flaw in all 20 members.
  - siblings: 逆袭人生 `0xceFbf00b3732FE91e46989037E4b2564a4fc7777` (bsc); MarsCoin `0xFe189E97832DA1573e4e4Ff034F4fFC3a15c7777` (bsc); 金蝶圣甲 `0x4f0c550bFe484F957D5C7Dd26f9a630a92A17777` (bsc); QLM `0x1Df197D03967eD707E5AABc2c6Cf0c0d62cb7777` (bsc); 币有 `0xe9337Dde3dd9e97f1f45A56412767ce5098E7777` (bsc); Asian games `0x31d19B3633eBdb60Dc9d690b3e9eB1FFF61A7777` (bsc); BoLe `0x5e4538460E07A12ea756fe1B774bf5C006797777` (bsc); CETS `0xB0c2aB5af4028461acE3f6e1C33a4eE1404E7777` (bsc); CBURN `0x309409237C4dB70Cd66067741eDcF02Bf69E7777` (bsc); 暴躁牛 `0x3A51dAE2Dc3D901A2cEfeD3Ad128116bf31C7777` (bsc); Max `0xe9Bc5C6A86caA44fD7b469bf3cc7c563E4F77777` (bsc); VenusCoin `0x5460b5E88799D27bbdf8A210926C17Dec18d7777` (bsc); Marvin `0xC6Bff31BbFa84d3c05AD61D8Ec47bE8B31517777` (bsc); Spark `0xC1073C967E323F2E197fA3975EC3b279974d7777` (bsc); gongsheng `0x70F7B593148283e7d84CeAB31407Bae0b5317777` (bsc); ASTEROID `0x330990DaE53BCa4C5811C5362B44C33a47db7777` (bsc); PIZZA `0x8554D38b95E4F7Ca11D391008627Df30B2b07777` (bsc); utility `0xEde00776439f9C49C592e43EeE34777a51847777` (bsc); bStocks `0x244B112Cf746e62A5DF723cbDe9906a6dEfd7777` (bsc)
- **Market:** pancakeswap · quote SPYB · pair `0x84307D86E8C367a98aCDcaB707eBE741E1F2C412` · [DexScreener](https://dexscreener.com/bsc/0x84307D86E8C367a98aCDcaB707eBE741E1F2C412)
- **Holders:** 2995
- **Why (score 51.1):** controls_reserve+10 lifecycle+5 surface_breadth+1.8 family_x20+28 liquidity+1.1 recency+5.2

## #31 · AFF · BNB Chain · score 51.0
*AiFu*

- **Chain:** BNB Chain
- **Token address:** `0xf1a05A63bc33269fc5dA861385B28ab6671a921b`  ·  [explorer](https://bscscan.com/address/0xf1a05A63bc33269fc5dA861385B28ab6671a921b)
- **Liquidity:** $458,710 real quote-side  (headline $458,772)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 46 days (≈ deployed 2026-07-01)
- **Custom logic:** impl/contract `AFFToken` — **fund ops, admin treasury pool signer, lifecycle ops, admin config gated**
  - key fns → fund: `initTokenDistributors`, `setMainBurnBps`, `setRewardGas`, `userClaimMint`
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote AiFi · pair `0x63F3c275b8d8a786f43ce64496decc5B3a1d6856` · [DexScreener](https://dexscreener.com/bsc/0x63F3c275b8d8a786f43ce64496decc5B3a1d6856)
- **Safety flags:** pausable|blacklist_fn
- **Holders:** 8750
- **Why (score 51.0):** fund_ops+12 controls_reserve+10 admin_setters+6 lifecycle+5 surface_breadth+12 liquidity+2.6 recency+1.4 pausable+2

## #32 · QQQB · BNB Chain · score 50.8
*Invesqo QQQ*

- **Chain:** BNB Chain
- **Token address:** `0x205812CdBed920aFf76C6580abD681a46D11efc7`  ·  [explorer](https://bscscan.com/address/0x205812CdBed920aFf76C6580abD681a46D11efc7)
- **Liquidity:** $1,084,445 real quote-side
- **Age / qualified by:** 34 days (≈ deployed 2026-07-12)
- **Custom logic:** **fund ops, admin treasury pool signer, lifecycle ops, admin config gated**
  - key fns → fund: `burn`, `mint`, `setBurnEnabled`, `setMintEnabled`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0xcfed6c4679297ea4889f8183bc057b4a86c64e46` (verified)
- **Shared codebase:** **FAM02** — shares a codebase with 9 other(s) via *shared_implementation*. A flaw here is a flaw in all 10 members.
  - siblings: SPCXB `0xbe9D156892E55e7154BcD3cB0FEA677F9D3103E1` (bsc); SKHYB `0xCA750eF65f295BBECd685Abf54e82CAf297BDB61` (bsc); NVDAB `0x02Fca66C1D1aFB4E2A7884261eB00F63598a7436` (bsc); GMEB `0x46cEeFDa28Dd7207059ed19B0acdc026955bb15C` (bsc); GOOGLB `0x3F53De71c126BdaBAe20f9cD64848d317f6C3238` (bsc); AAPLB `0x431a3BEE82E2ca41e49895CbECE5bB0F76A89b7A` (bsc); SPYB `0x7138b48df7D98D7e3cc221BfE7192D0a178182D8` (bsc); TSLAB `0x5b1910eAaD6450E50f816082Aa078C41F10C292f` (bsc); MSFTB `0x80106cb3EAD06659A5ad19DF39D9b4733863B9b0` (bsc)
- **Market:** pancakeswap · quote USDT · pair `0xe531fcb1F5a195de7608B9F4f9518544C2cdB693` · [DexScreener](https://dexscreener.com/bsc/0xe531fcb1F5a195de7608B9F4f9518544C2cdB693)
- **Holders:** 15682
- **Why (score 50.8):** fund_ops+12 admin_setters+6 lifecycle+5 surface_breadth+7.2 family_x10+14 liquidity+4.1 recency+2.5

## #33 · SKHYB · BNB Chain · score 50.8
*SK Hynix*

- **Chain:** BNB Chain
- **Token address:** `0xCA750eF65f295BBECd685Abf54e82CAf297BDB61`  ·  [explorer](https://bscscan.com/address/0xCA750eF65f295BBECd685Abf54e82CAf297BDB61)
- **Liquidity:** $835,043 real quote-side
- **Age / qualified by:** 30 days (≈ deployed 2026-07-16)
- **Custom logic:** **fund ops, admin treasury pool signer, lifecycle ops, admin config gated**
  - key fns → fund: `burn`, `mint`, `setBurnEnabled`, `setMintEnabled`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0xcfed6c4679297ea4889f8183bc057b4a86c64e46` (verified)
- **Shared codebase:** **FAM02** — shares a codebase with 9 other(s) via *shared_implementation*. A flaw here is a flaw in all 10 members.
  - siblings: SPCXB `0xbe9D156892E55e7154BcD3cB0FEA677F9D3103E1` (bsc); QQQB `0x205812CdBed920aFf76C6580abD681a46D11efc7` (bsc); NVDAB `0x02Fca66C1D1aFB4E2A7884261eB00F63598a7436` (bsc); GMEB `0x46cEeFDa28Dd7207059ed19B0acdc026955bb15C` (bsc); GOOGLB `0x3F53De71c126BdaBAe20f9cD64848d317f6C3238` (bsc); AAPLB `0x431a3BEE82E2ca41e49895CbECE5bB0F76A89b7A` (bsc); SPYB `0x7138b48df7D98D7e3cc221BfE7192D0a178182D8` (bsc); TSLAB `0x5b1910eAaD6450E50f816082Aa078C41F10C292f` (bsc); MSFTB `0x80106cb3EAD06659A5ad19DF39D9b4733863B9b0` (bsc)
- **Market:** pancakeswap · quote USDT · pair `0xD7d30F434b12F7Ed9b0Ae11fF1C754745a10aD52` · [DexScreener](https://dexscreener.com/bsc/0xD7d30F434b12F7Ed9b0Ae11fF1C754745a10aD52)
- **Holders:** 3907
- **Why (score 50.8):** fund_ops+12 admin_setters+6 lifecycle+5 surface_breadth+7.2 family_x10+14 liquidity+3.7 recency+2.9

## #34 · utility · BNB Chain · score 50.8
*utility token*

- **Chain:** BNB Chain
- **Token address:** `0xEde00776439f9C49C592e43EeE34777a51847777`  ·  [explorer](https://bscscan.com/address/0xEde00776439f9C49C592e43EeE34777a51847777)
- **Liquidity:** $105,636 real quote-side
- **Age / qualified by:** 1 days (≈ deployed 2026-08-15)
- **Custom logic:** impl/contract `FlapTaxTokenV3` — **lifecycle ops**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** **FAM01** — shares a codebase with 19 other(s) via *shared_implementation*. A flaw here is a flaw in all 20 members.
  - siblings: 逆袭人生 `0xceFbf00b3732FE91e46989037E4b2564a4fc7777` (bsc); MarsCoin `0xFe189E97832DA1573e4e4Ff034F4fFC3a15c7777` (bsc); 金蝶圣甲 `0x4f0c550bFe484F957D5C7Dd26f9a630a92A17777` (bsc); QLM `0x1Df197D03967eD707E5AABc2c6Cf0c0d62cb7777` (bsc); 币有 `0xe9337Dde3dd9e97f1f45A56412767ce5098E7777` (bsc); Asian games `0x31d19B3633eBdb60Dc9d690b3e9eB1FFF61A7777` (bsc); BoLe `0x5e4538460E07A12ea756fe1B774bf5C006797777` (bsc); CETS `0xB0c2aB5af4028461acE3f6e1C33a4eE1404E7777` (bsc); CBURN `0x309409237C4dB70Cd66067741eDcF02Bf69E7777` (bsc); 暴躁牛 `0x3A51dAE2Dc3D901A2cEfeD3Ad128116bf31C7777` (bsc); SUMMER `0xeEb3d73d4dd44e6E4d957d89492f05d5CCeE7777` (bsc); Max `0xe9Bc5C6A86caA44fD7b469bf3cc7c563E4F77777` (bsc); VenusCoin `0x5460b5E88799D27bbdf8A210926C17Dec18d7777` (bsc); Marvin `0xC6Bff31BbFa84d3c05AD61D8Ec47bE8B31517777` (bsc); Spark `0xC1073C967E323F2E197fA3975EC3b279974d7777` (bsc); gongsheng `0x70F7B593148283e7d84CeAB31407Bae0b5317777` (bsc); ASTEROID `0x330990DaE53BCa4C5811C5362B44C33a47db7777` (bsc); PIZZA `0x8554D38b95E4F7Ca11D391008627Df30B2b07777` (bsc); bStocks `0x244B112Cf746e62A5DF723cbDe9906a6dEfd7777` (bsc)
- **Market:** pancakeswap · quote USDT · pair `0xD9265bB5A2552eCFB0Da6d5eDc7874d71156ec4c` · [DexScreener](https://dexscreener.com/bsc/0xD9265bB5A2552eCFB0Da6d5eDc7874d71156ec4c)
- **Holders:** 2737
- **Why (score 50.8):** controls_reserve+10 lifecycle+5 surface_breadth+1.8 family_x20+28 liquidity+0.1 recency+5.9

## #35 · TSLAB · BNB Chain · score 50.6
*Tesla, Inc. *

- **Chain:** BNB Chain
- **Token address:** `0x5b1910eAaD6450E50f816082Aa078C41F10C292f`  ·  [explorer](https://bscscan.com/address/0x5b1910eAaD6450E50f816082Aa078C41F10C292f)
- **Liquidity:** $267,186 real quote-side
- **Age / qualified by:** 14 days (≈ deployed 2026-08-02)
- **Custom logic:** **fund ops, admin treasury pool signer, lifecycle ops, admin config gated**
  - key fns → fund: `burn`, `mint`, `setBurnEnabled`, `setMintEnabled`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0xcfed6c4679297ea4889f8183bc057b4a86c64e46` (verified)
- **Shared codebase:** **FAM02** — shares a codebase with 9 other(s) via *shared_implementation*. A flaw here is a flaw in all 10 members.
  - siblings: SPCXB `0xbe9D156892E55e7154BcD3cB0FEA677F9D3103E1` (bsc); QQQB `0x205812CdBed920aFf76C6580abD681a46D11efc7` (bsc); SKHYB `0xCA750eF65f295BBECd685Abf54e82CAf297BDB61` (bsc); NVDAB `0x02Fca66C1D1aFB4E2A7884261eB00F63598a7436` (bsc); GMEB `0x46cEeFDa28Dd7207059ed19B0acdc026955bb15C` (bsc); GOOGLB `0x3F53De71c126BdaBAe20f9cD64848d317f6C3238` (bsc); AAPLB `0x431a3BEE82E2ca41e49895CbECE5bB0F76A89b7A` (bsc); SPYB `0x7138b48df7D98D7e3cc221BfE7192D0a178182D8` (bsc); MSFTB `0x80106cb3EAD06659A5ad19DF39D9b4733863B9b0` (bsc)
- **Market:** pancakeswap · quote USDT · pair `0xB0f5E5400E8F0F7C242F2b7740C004f020579c41` · [DexScreener](https://dexscreener.com/bsc/0xB0f5E5400E8F0F7C242F2b7740C004f020579c41)
- **Holders:** 19366
- **Why (score 50.6):** fund_ops+12 admin_setters+6 lifecycle+5 surface_breadth+7.2 family_x10+14 liquidity+1.7 recency+4.7

## #36 · Marvin · BNB Chain · score 50.6
*The Martian Dog*

- **Chain:** BNB Chain
- **Token address:** `0xC6Bff31BbFa84d3c05AD61D8Ec47bE8B31517777`  ·  [explorer](https://bscscan.com/address/0xC6Bff31BbFa84d3c05AD61D8Ec47bE8B31517777)
- **Liquidity:** $136,424 real quote-side  (headline $136,455)
- **Age / qualified by:** 7 days (≈ deployed 2026-08-08)
- **Custom logic:** impl/contract `FlapTaxTokenV3` — **lifecycle ops**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** **FAM01** — shares a codebase with 19 other(s) via *shared_implementation*. A flaw here is a flaw in all 20 members.
  - siblings: 逆袭人生 `0xceFbf00b3732FE91e46989037E4b2564a4fc7777` (bsc); MarsCoin `0xFe189E97832DA1573e4e4Ff034F4fFC3a15c7777` (bsc); 金蝶圣甲 `0x4f0c550bFe484F957D5C7Dd26f9a630a92A17777` (bsc); QLM `0x1Df197D03967eD707E5AABc2c6Cf0c0d62cb7777` (bsc); 币有 `0xe9337Dde3dd9e97f1f45A56412767ce5098E7777` (bsc); Asian games `0x31d19B3633eBdb60Dc9d690b3e9eB1FFF61A7777` (bsc); BoLe `0x5e4538460E07A12ea756fe1B774bf5C006797777` (bsc); CETS `0xB0c2aB5af4028461acE3f6e1C33a4eE1404E7777` (bsc); CBURN `0x309409237C4dB70Cd66067741eDcF02Bf69E7777` (bsc); 暴躁牛 `0x3A51dAE2Dc3D901A2cEfeD3Ad128116bf31C7777` (bsc); SUMMER `0xeEb3d73d4dd44e6E4d957d89492f05d5CCeE7777` (bsc); Max `0xe9Bc5C6A86caA44fD7b469bf3cc7c563E4F77777` (bsc); VenusCoin `0x5460b5E88799D27bbdf8A210926C17Dec18d7777` (bsc); Spark `0xC1073C967E323F2E197fA3975EC3b279974d7777` (bsc); gongsheng `0x70F7B593148283e7d84CeAB31407Bae0b5317777` (bsc); ASTEROID `0x330990DaE53BCa4C5811C5362B44C33a47db7777` (bsc); PIZZA `0x8554D38b95E4F7Ca11D391008627Df30B2b07777` (bsc); utility `0xEde00776439f9C49C592e43EeE34777a51847777` (bsc); bStocks `0x244B112Cf746e62A5DF723cbDe9906a6dEfd7777` (bsc)
- **Market:** pancakeswap · quote WBNB · pair `0xd05df375Fd50726A0680ffDC295A9bA56A7295C9` · [DexScreener](https://dexscreener.com/bsc/0xd05df375Fd50726A0680ffDC295A9bA56A7295C9)
- **Holders:** 5732
- **Why (score 50.6):** controls_reserve+10 lifecycle+5 surface_breadth+1.8 family_x20+28 liquidity+0.5 recency+5.3

## #37 · VenusCoin · BNB Chain · score 50.5

- **Chain:** BNB Chain
- **Token address:** `0x5460b5E88799D27bbdf8A210926C17Dec18d7777`  ·  [explorer](https://bscscan.com/address/0x5460b5E88799D27bbdf8A210926C17Dec18d7777)
- **Liquidity:** $137,592 real quote-side  (headline $137,657)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 9 days (≈ deployed 2026-08-07)
- **Custom logic:** impl/contract `FlapTaxTokenV3` — **lifecycle ops**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** **FAM01** — shares a codebase with 19 other(s) via *shared_implementation*. A flaw here is a flaw in all 20 members.
  - siblings: 逆袭人生 `0xceFbf00b3732FE91e46989037E4b2564a4fc7777` (bsc); MarsCoin `0xFe189E97832DA1573e4e4Ff034F4fFC3a15c7777` (bsc); 金蝶圣甲 `0x4f0c550bFe484F957D5C7Dd26f9a630a92A17777` (bsc); QLM `0x1Df197D03967eD707E5AABc2c6Cf0c0d62cb7777` (bsc); 币有 `0xe9337Dde3dd9e97f1f45A56412767ce5098E7777` (bsc); Asian games `0x31d19B3633eBdb60Dc9d690b3e9eB1FFF61A7777` (bsc); BoLe `0x5e4538460E07A12ea756fe1B774bf5C006797777` (bsc); CETS `0xB0c2aB5af4028461acE3f6e1C33a4eE1404E7777` (bsc); CBURN `0x309409237C4dB70Cd66067741eDcF02Bf69E7777` (bsc); 暴躁牛 `0x3A51dAE2Dc3D901A2cEfeD3Ad128116bf31C7777` (bsc); SUMMER `0xeEb3d73d4dd44e6E4d957d89492f05d5CCeE7777` (bsc); Max `0xe9Bc5C6A86caA44fD7b469bf3cc7c563E4F77777` (bsc); Marvin `0xC6Bff31BbFa84d3c05AD61D8Ec47bE8B31517777` (bsc); Spark `0xC1073C967E323F2E197fA3975EC3b279974d7777` (bsc); gongsheng `0x70F7B593148283e7d84CeAB31407Bae0b5317777` (bsc); ASTEROID `0x330990DaE53BCa4C5811C5362B44C33a47db7777` (bsc); PIZZA `0x8554D38b95E4F7Ca11D391008627Df30B2b07777` (bsc); utility `0xEde00776439f9C49C592e43EeE34777a51847777` (bsc); bStocks `0x244B112Cf746e62A5DF723cbDe9906a6dEfd7777` (bsc)
- **Market:** pancakeswap · quote XAUt · pair `0x12cd92372983c4d60Fd40ae6c7545bbc5EBc8cA7` · [DexScreener](https://dexscreener.com/bsc/0x12cd92372983c4d60Fd40ae6c7545bbc5EBc8cA7)
- **Holders:** 6904
- **Why (score 50.5):** controls_reserve+10 lifecycle+5 surface_breadth+1.8 family_x20+28 liquidity+0.6 recency+5.1

## #38 · 暴躁牛 · BNB Chain · score 50.2

- **Chain:** BNB Chain
- **Token address:** `0x3A51dAE2Dc3D901A2cEfeD3Ad128116bf31C7777`  ·  [explorer](https://bscscan.com/address/0x3A51dAE2Dc3D901A2cEfeD3Ad128116bf31C7777)
- **Liquidity:** $209,016 real quote-side
- **Age / qualified by:** 19 days (≈ deployed 2026-07-27)
- **Custom logic:** impl/contract `FlapTaxTokenV3` — **lifecycle ops**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** **FAM01** — shares a codebase with 19 other(s) via *shared_implementation*. A flaw here is a flaw in all 20 members.
  - siblings: 逆袭人生 `0xceFbf00b3732FE91e46989037E4b2564a4fc7777` (bsc); MarsCoin `0xFe189E97832DA1573e4e4Ff034F4fFC3a15c7777` (bsc); 金蝶圣甲 `0x4f0c550bFe484F957D5C7Dd26f9a630a92A17777` (bsc); QLM `0x1Df197D03967eD707E5AABc2c6Cf0c0d62cb7777` (bsc); 币有 `0xe9337Dde3dd9e97f1f45A56412767ce5098E7777` (bsc); Asian games `0x31d19B3633eBdb60Dc9d690b3e9eB1FFF61A7777` (bsc); BoLe `0x5e4538460E07A12ea756fe1B774bf5C006797777` (bsc); CETS `0xB0c2aB5af4028461acE3f6e1C33a4eE1404E7777` (bsc); CBURN `0x309409237C4dB70Cd66067741eDcF02Bf69E7777` (bsc); SUMMER `0xeEb3d73d4dd44e6E4d957d89492f05d5CCeE7777` (bsc); Max `0xe9Bc5C6A86caA44fD7b469bf3cc7c563E4F77777` (bsc); VenusCoin `0x5460b5E88799D27bbdf8A210926C17Dec18d7777` (bsc); Marvin `0xC6Bff31BbFa84d3c05AD61D8Ec47bE8B31517777` (bsc); Spark `0xC1073C967E323F2E197fA3975EC3b279974d7777` (bsc); gongsheng `0x70F7B593148283e7d84CeAB31407Bae0b5317777` (bsc); ASTEROID `0x330990DaE53BCa4C5811C5362B44C33a47db7777` (bsc); PIZZA `0x8554D38b95E4F7Ca11D391008627Df30B2b07777` (bsc); utility `0xEde00776439f9C49C592e43EeE34777a51847777` (bsc); bStocks `0x244B112Cf746e62A5DF723cbDe9906a6dEfd7777` (bsc)
- **Market:** pancakeswap · quote WBNB · pair `0xfBb04B4D5F8610D09cc6973b1Efd44C0fE51bbAc` · [DexScreener](https://dexscreener.com/bsc/0xfBb04B4D5F8610D09cc6973b1Efd44C0fE51bbAc)
- **Holders:** 9182
- **Why (score 50.2):** controls_reserve+10 lifecycle+5 surface_breadth+1.8 family_x20+28 liquidity+1.3 recency+4.1

## #39 · Max · BNB Chain · score 50.2
*Giggle Mascot*

- **Chain:** BNB Chain
- **Token address:** `0xe9Bc5C6A86caA44fD7b469bf3cc7c563E4F77777`  ·  [explorer](https://bscscan.com/address/0xe9Bc5C6A86caA44fD7b469bf3cc7c563E4F77777)
- **Liquidity:** $140,099 real quote-side  (headline $140,118)
- **Age / qualified by:** 12 days (≈ deployed 2026-08-03)
- **Custom logic:** impl/contract `FlapTaxTokenV3` — **lifecycle ops**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** **FAM01** — shares a codebase with 19 other(s) via *shared_implementation*. A flaw here is a flaw in all 20 members.
  - siblings: 逆袭人生 `0xceFbf00b3732FE91e46989037E4b2564a4fc7777` (bsc); MarsCoin `0xFe189E97832DA1573e4e4Ff034F4fFC3a15c7777` (bsc); 金蝶圣甲 `0x4f0c550bFe484F957D5C7Dd26f9a630a92A17777` (bsc); QLM `0x1Df197D03967eD707E5AABc2c6Cf0c0d62cb7777` (bsc); 币有 `0xe9337Dde3dd9e97f1f45A56412767ce5098E7777` (bsc); Asian games `0x31d19B3633eBdb60Dc9d690b3e9eB1FFF61A7777` (bsc); BoLe `0x5e4538460E07A12ea756fe1B774bf5C006797777` (bsc); CETS `0xB0c2aB5af4028461acE3f6e1C33a4eE1404E7777` (bsc); CBURN `0x309409237C4dB70Cd66067741eDcF02Bf69E7777` (bsc); 暴躁牛 `0x3A51dAE2Dc3D901A2cEfeD3Ad128116bf31C7777` (bsc); SUMMER `0xeEb3d73d4dd44e6E4d957d89492f05d5CCeE7777` (bsc); VenusCoin `0x5460b5E88799D27bbdf8A210926C17Dec18d7777` (bsc); Marvin `0xC6Bff31BbFa84d3c05AD61D8Ec47bE8B31517777` (bsc); Spark `0xC1073C967E323F2E197fA3975EC3b279974d7777` (bsc); gongsheng `0x70F7B593148283e7d84CeAB31407Bae0b5317777` (bsc); ASTEROID `0x330990DaE53BCa4C5811C5362B44C33a47db7777` (bsc); PIZZA `0x8554D38b95E4F7Ca11D391008627Df30B2b07777` (bsc); utility `0xEde00776439f9C49C592e43EeE34777a51847777` (bsc); bStocks `0x244B112Cf746e62A5DF723cbDe9906a6dEfd7777` (bsc)
- **Market:** pancakeswap · quote WBNB · pair `0xa2b1926Cb477e92445Cf70602f1A7200361F761D` · [DexScreener](https://dexscreener.com/bsc/0xa2b1926Cb477e92445Cf70602f1A7200361F761D)
- **Holders:** 2495
- **Why (score 50.2):** controls_reserve+10 lifecycle+5 surface_breadth+1.8 family_x20+28 liquidity+0.6 recency+4.8

## #40 · bStocks · BNB Chain · score 50.2
*bStocks Never Sleep*

- **Chain:** BNB Chain
- **Token address:** `0x244B112Cf746e62A5DF723cbDe9906a6dEfd7777`  ·  [explorer](https://bscscan.com/address/0x244B112Cf746e62A5DF723cbDe9906a6dEfd7777)
- **Liquidity:** $101,719 real quote-side  (headline $101,723)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 6 days (≈ deployed 2026-08-09)
- **Custom logic:** impl/contract `FlapTaxTokenV3` — **lifecycle ops**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** **FAM01** — shares a codebase with 19 other(s) via *shared_implementation*. A flaw here is a flaw in all 20 members.
  - siblings: 逆袭人生 `0xceFbf00b3732FE91e46989037E4b2564a4fc7777` (bsc); MarsCoin `0xFe189E97832DA1573e4e4Ff034F4fFC3a15c7777` (bsc); 金蝶圣甲 `0x4f0c550bFe484F957D5C7Dd26f9a630a92A17777` (bsc); QLM `0x1Df197D03967eD707E5AABc2c6Cf0c0d62cb7777` (bsc); 币有 `0xe9337Dde3dd9e97f1f45A56412767ce5098E7777` (bsc); Asian games `0x31d19B3633eBdb60Dc9d690b3e9eB1FFF61A7777` (bsc); BoLe `0x5e4538460E07A12ea756fe1B774bf5C006797777` (bsc); CETS `0xB0c2aB5af4028461acE3f6e1C33a4eE1404E7777` (bsc); CBURN `0x309409237C4dB70Cd66067741eDcF02Bf69E7777` (bsc); 暴躁牛 `0x3A51dAE2Dc3D901A2cEfeD3Ad128116bf31C7777` (bsc); SUMMER `0xeEb3d73d4dd44e6E4d957d89492f05d5CCeE7777` (bsc); Max `0xe9Bc5C6A86caA44fD7b469bf3cc7c563E4F77777` (bsc); VenusCoin `0x5460b5E88799D27bbdf8A210926C17Dec18d7777` (bsc); Marvin `0xC6Bff31BbFa84d3c05AD61D8Ec47bE8B31517777` (bsc); Spark `0xC1073C967E323F2E197fA3975EC3b279974d7777` (bsc); gongsheng `0x70F7B593148283e7d84CeAB31407Bae0b5317777` (bsc); ASTEROID `0x330990DaE53BCa4C5811C5362B44C33a47db7777` (bsc); PIZZA `0x8554D38b95E4F7Ca11D391008627Df30B2b07777` (bsc); utility `0xEde00776439f9C49C592e43EeE34777a51847777` (bsc)
- **Market:** pancakeswap · quote SPYB · pair `0x45DCB68A2ddcCF00271B6941cFfe70676e5C8247` · [DexScreener](https://dexscreener.com/bsc/0x45DCB68A2ddcCF00271B6941cFfe70676e5C8247)
- **Holders:** 4990
- **Why (score 50.2):** controls_reserve+10 lifecycle+5 surface_breadth+1.8 family_x20+28 recency+5.4

## #41 · AAPLB · BNB Chain · score 50.1
*Apple*

- **Chain:** BNB Chain
- **Token address:** `0x431a3BEE82E2ca41e49895CbECE5bB0F76A89b7A`  ·  [explorer](https://bscscan.com/address/0x431a3BEE82E2ca41e49895CbECE5bB0F76A89b7A)
- **Liquidity:** $223,174 real quote-side  (headline $319,065)
- **Age / qualified by:** 15 days (≈ deployed 2026-08-01)
- **Custom logic:** **fund ops, admin treasury pool signer, lifecycle ops, admin config gated**
  - key fns → fund: `burn`, `mint`, `setBurnEnabled`, `setMintEnabled`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0xcfed6c4679297ea4889f8183bc057b4a86c64e46` (verified)
- **Shared codebase:** **FAM02** — shares a codebase with 9 other(s) via *shared_implementation*. A flaw here is a flaw in all 10 members.
  - siblings: SPCXB `0xbe9D156892E55e7154BcD3cB0FEA677F9D3103E1` (bsc); QQQB `0x205812CdBed920aFf76C6580abD681a46D11efc7` (bsc); SKHYB `0xCA750eF65f295BBECd685Abf54e82CAf297BDB61` (bsc); NVDAB `0x02Fca66C1D1aFB4E2A7884261eB00F63598a7436` (bsc); GMEB `0x46cEeFDa28Dd7207059ed19B0acdc026955bb15C` (bsc); GOOGLB `0x3F53De71c126BdaBAe20f9cD64848d317f6C3238` (bsc); SPYB `0x7138b48df7D98D7e3cc221BfE7192D0a178182D8` (bsc); TSLAB `0x5b1910eAaD6450E50f816082Aa078C41F10C292f` (bsc); MSFTB `0x80106cb3EAD06659A5ad19DF39D9b4733863B9b0` (bsc)
- **Market:** pancakeswap · quote USDT · pair `0xe9b9998B2EC5430D2246c7f1F8D9f298c97D7365` · [DexScreener](https://dexscreener.com/bsc/0xe9b9998B2EC5430D2246c7f1F8D9f298c97D7365)
- **Holders:** 5530
- **Why (score 50.1):** fund_ops+12 admin_setters+6 lifecycle+5 surface_breadth+7.2 family_x10+14 liquidity+1.4 recency+4.5

## #42 · gongsheng · BNB Chain · score 50.0
*共生    *

- **Chain:** BNB Chain
- **Token address:** `0x70F7B593148283e7d84CeAB31407Bae0b5317777`  ·  [explorer](https://bscscan.com/address/0x70F7B593148283e7d84CeAB31407Bae0b5317777)
- **Liquidity:** $119,927 real quote-side  (headline $119,956)
- **Age / qualified by:** 11 days (≈ deployed 2026-08-04)
- **Custom logic:** impl/contract `FlapTaxTokenV3` — **lifecycle ops**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** **FAM01** — shares a codebase with 19 other(s) via *shared_implementation*. A flaw here is a flaw in all 20 members.
  - siblings: 逆袭人生 `0xceFbf00b3732FE91e46989037E4b2564a4fc7777` (bsc); MarsCoin `0xFe189E97832DA1573e4e4Ff034F4fFC3a15c7777` (bsc); 金蝶圣甲 `0x4f0c550bFe484F957D5C7Dd26f9a630a92A17777` (bsc); QLM `0x1Df197D03967eD707E5AABc2c6Cf0c0d62cb7777` (bsc); 币有 `0xe9337Dde3dd9e97f1f45A56412767ce5098E7777` (bsc); Asian games `0x31d19B3633eBdb60Dc9d690b3e9eB1FFF61A7777` (bsc); BoLe `0x5e4538460E07A12ea756fe1B774bf5C006797777` (bsc); CETS `0xB0c2aB5af4028461acE3f6e1C33a4eE1404E7777` (bsc); CBURN `0x309409237C4dB70Cd66067741eDcF02Bf69E7777` (bsc); 暴躁牛 `0x3A51dAE2Dc3D901A2cEfeD3Ad128116bf31C7777` (bsc); SUMMER `0xeEb3d73d4dd44e6E4d957d89492f05d5CCeE7777` (bsc); Max `0xe9Bc5C6A86caA44fD7b469bf3cc7c563E4F77777` (bsc); VenusCoin `0x5460b5E88799D27bbdf8A210926C17Dec18d7777` (bsc); Marvin `0xC6Bff31BbFa84d3c05AD61D8Ec47bE8B31517777` (bsc); Spark `0xC1073C967E323F2E197fA3975EC3b279974d7777` (bsc); ASTEROID `0x330990DaE53BCa4C5811C5362B44C33a47db7777` (bsc); PIZZA `0x8554D38b95E4F7Ca11D391008627Df30B2b07777` (bsc); utility `0xEde00776439f9C49C592e43EeE34777a51847777` (bsc); bStocks `0x244B112Cf746e62A5DF723cbDe9906a6dEfd7777` (bsc)
- **Market:** pancakeswap · quote WBNB · pair `0xFfb73F02924B524bd1508408AC6BF5fC9E8e9173` · [DexScreener](https://dexscreener.com/bsc/0xFfb73F02924B524bd1508408AC6BF5fC9E8e9173)
- **Holders:** 30584
- **Why (score 50.0):** controls_reserve+10 lifecycle+5 surface_breadth+1.8 family_x20+28 liquidity+0.3 recency+4.9

## #43 · Spark · BNB Chain · score 49.8
*SPK*

- **Chain:** BNB Chain
- **Token address:** `0xC1073C967E323F2E197fA3975EC3b279974d7777`  ·  [explorer](https://bscscan.com/address/0xC1073C967E323F2E197fA3975EC3b279974d7777)
- **Liquidity:** $122,559 real quote-side  (headline $122,559)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 14 days (≈ deployed 2026-08-02)
- **Custom logic:** impl/contract `FlapTaxTokenV3` — **lifecycle ops**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** **FAM01** — shares a codebase with 19 other(s) via *shared_implementation*. A flaw here is a flaw in all 20 members.
  - siblings: 逆袭人生 `0xceFbf00b3732FE91e46989037E4b2564a4fc7777` (bsc); MarsCoin `0xFe189E97832DA1573e4e4Ff034F4fFC3a15c7777` (bsc); 金蝶圣甲 `0x4f0c550bFe484F957D5C7Dd26f9a630a92A17777` (bsc); QLM `0x1Df197D03967eD707E5AABc2c6Cf0c0d62cb7777` (bsc); 币有 `0xe9337Dde3dd9e97f1f45A56412767ce5098E7777` (bsc); Asian games `0x31d19B3633eBdb60Dc9d690b3e9eB1FFF61A7777` (bsc); BoLe `0x5e4538460E07A12ea756fe1B774bf5C006797777` (bsc); CETS `0xB0c2aB5af4028461acE3f6e1C33a4eE1404E7777` (bsc); CBURN `0x309409237C4dB70Cd66067741eDcF02Bf69E7777` (bsc); 暴躁牛 `0x3A51dAE2Dc3D901A2cEfeD3Ad128116bf31C7777` (bsc); SUMMER `0xeEb3d73d4dd44e6E4d957d89492f05d5CCeE7777` (bsc); Max `0xe9Bc5C6A86caA44fD7b469bf3cc7c563E4F77777` (bsc); VenusCoin `0x5460b5E88799D27bbdf8A210926C17Dec18d7777` (bsc); Marvin `0xC6Bff31BbFa84d3c05AD61D8Ec47bE8B31517777` (bsc); gongsheng `0x70F7B593148283e7d84CeAB31407Bae0b5317777` (bsc); ASTEROID `0x330990DaE53BCa4C5811C5362B44C33a47db7777` (bsc); PIZZA `0x8554D38b95E4F7Ca11D391008627Df30B2b07777` (bsc); utility `0xEde00776439f9C49C592e43EeE34777a51847777` (bsc); bStocks `0x244B112Cf746e62A5DF723cbDe9906a6dEfd7777` (bsc)
- **Market:** pancakeswap · quote SPCXB · pair `0x1176b6Ee898e1B2AeE1C8860FC4b6FE17859EeA8` · [DexScreener](https://dexscreener.com/bsc/0x1176b6Ee898e1B2AeE1C8860FC4b6FE17859EeA8)
- **Holders:** 1500
- **Why (score 49.8):** controls_reserve+10 lifecycle+5 surface_breadth+1.8 family_x20+28 liquidity+0.4 recency+4.6

## #44 · ASTEROID · BNB Chain · score 49.8
*Asteroid Shiba*

- **Chain:** BNB Chain
- **Token address:** `0x330990DaE53BCa4C5811C5362B44C33a47db7777`  ·  [explorer](https://bscscan.com/address/0x330990DaE53BCa4C5811C5362B44C33a47db7777)
- **Liquidity:** $119,736 real quote-side  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 13 days (≈ deployed 2026-08-03)
- **Custom logic:** impl/contract `FlapTaxTokenV3` — **lifecycle ops**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** **FAM01** — shares a codebase with 19 other(s) via *shared_implementation*. A flaw here is a flaw in all 20 members.
  - siblings: 逆袭人生 `0xceFbf00b3732FE91e46989037E4b2564a4fc7777` (bsc); MarsCoin `0xFe189E97832DA1573e4e4Ff034F4fFC3a15c7777` (bsc); 金蝶圣甲 `0x4f0c550bFe484F957D5C7Dd26f9a630a92A17777` (bsc); QLM `0x1Df197D03967eD707E5AABc2c6Cf0c0d62cb7777` (bsc); 币有 `0xe9337Dde3dd9e97f1f45A56412767ce5098E7777` (bsc); Asian games `0x31d19B3633eBdb60Dc9d690b3e9eB1FFF61A7777` (bsc); BoLe `0x5e4538460E07A12ea756fe1B774bf5C006797777` (bsc); CETS `0xB0c2aB5af4028461acE3f6e1C33a4eE1404E7777` (bsc); CBURN `0x309409237C4dB70Cd66067741eDcF02Bf69E7777` (bsc); 暴躁牛 `0x3A51dAE2Dc3D901A2cEfeD3Ad128116bf31C7777` (bsc); SUMMER `0xeEb3d73d4dd44e6E4d957d89492f05d5CCeE7777` (bsc); Max `0xe9Bc5C6A86caA44fD7b469bf3cc7c563E4F77777` (bsc); VenusCoin `0x5460b5E88799D27bbdf8A210926C17Dec18d7777` (bsc); Marvin `0xC6Bff31BbFa84d3c05AD61D8Ec47bE8B31517777` (bsc); Spark `0xC1073C967E323F2E197fA3975EC3b279974d7777` (bsc); gongsheng `0x70F7B593148283e7d84CeAB31407Bae0b5317777` (bsc); PIZZA `0x8554D38b95E4F7Ca11D391008627Df30B2b07777` (bsc); utility `0xEde00776439f9C49C592e43EeE34777a51847777` (bsc); bStocks `0x244B112Cf746e62A5DF723cbDe9906a6dEfd7777` (bsc)
- **Market:** pancakeswap · quote SPCXB · pair `0x60c04117753E634fE2D0587493613aACCDD0329c` · [DexScreener](https://dexscreener.com/bsc/0x60c04117753E634fE2D0587493613aACCDD0329c)
- **Holders:** 8703
- **Why (score 49.8):** controls_reserve+10 lifecycle+5 surface_breadth+1.8 family_x20+28 liquidity+0.3 recency+4.7

## #45 · PIZZA · BNB Chain · score 49.8  ⚠️ **ALREADY EXPLOITED**

- **Chain:** BNB Chain
- **Token address:** `0x8554D38b95E4F7Ca11D391008627Df30B2b07777`  ·  [explorer](https://bscscan.com/address/0x8554D38b95E4F7Ca11D391008627Df30B2b07777)
- **Liquidity:** $111,022 real quote-side
- **Age / qualified by:** 12 days (≈ deployed 2026-08-04)
- **Custom logic:** impl/contract `FlapTaxTokenV3` — **lifecycle ops**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** **FAM01** — shares a codebase with 19 other(s) via *shared_implementation*. A flaw here is a flaw in all 20 members.
  - siblings: 逆袭人生 `0xceFbf00b3732FE91e46989037E4b2564a4fc7777` (bsc); MarsCoin `0xFe189E97832DA1573e4e4Ff034F4fFC3a15c7777` (bsc); 金蝶圣甲 `0x4f0c550bFe484F957D5C7Dd26f9a630a92A17777` (bsc); QLM `0x1Df197D03967eD707E5AABc2c6Cf0c0d62cb7777` (bsc); 币有 `0xe9337Dde3dd9e97f1f45A56412767ce5098E7777` (bsc); Asian games `0x31d19B3633eBdb60Dc9d690b3e9eB1FFF61A7777` (bsc); BoLe `0x5e4538460E07A12ea756fe1B774bf5C006797777` (bsc); CETS `0xB0c2aB5af4028461acE3f6e1C33a4eE1404E7777` (bsc); CBURN `0x309409237C4dB70Cd66067741eDcF02Bf69E7777` (bsc); 暴躁牛 `0x3A51dAE2Dc3D901A2cEfeD3Ad128116bf31C7777` (bsc); SUMMER `0xeEb3d73d4dd44e6E4d957d89492f05d5CCeE7777` (bsc); Max `0xe9Bc5C6A86caA44fD7b469bf3cc7c563E4F77777` (bsc); VenusCoin `0x5460b5E88799D27bbdf8A210926C17Dec18d7777` (bsc); Marvin `0xC6Bff31BbFa84d3c05AD61D8Ec47bE8B31517777` (bsc); Spark `0xC1073C967E323F2E197fA3975EC3b279974d7777` (bsc); gongsheng `0x70F7B593148283e7d84CeAB31407Bae0b5317777` (bsc); ASTEROID `0x330990DaE53BCa4C5811C5362B44C33a47db7777` (bsc); utility `0xEde00776439f9C49C592e43EeE34777a51847777` (bsc); bStocks `0x244B112Cf746e62A5DF723cbDe9906a6dEfd7777` (bsc)
- **Market:** pancakeswap · quote BTCB · pair `0xE5380b1848e71cBfCD1974d92BD4b76659C67534` · [DexScreener](https://dexscreener.com/bsc/0xE5380b1848e71cBfCD1974d92BD4b76659C67534)
- **Holders:** 4727
- **Exploit status:** ticker collision - ruled out
- **Why (score 49.8):** controls_reserve+10 lifecycle+5 surface_breadth+1.8 family_x20+28 liquidity+0.2 recency+4.8

## #46 · BoLe · BNB Chain · score 49.5

- **Chain:** BNB Chain
- **Token address:** `0x5e4538460E07A12ea756fe1B774bf5C006797777`  ·  [explorer](https://bscscan.com/address/0x5e4538460E07A12ea756fe1B774bf5C006797777)
- **Liquidity:** $252,816 real quote-side  (headline $252,844)
- **Age / qualified by:** 29 days (≈ deployed 2026-07-17)
- **Custom logic:** impl/contract `FlapTaxTokenV3` — **lifecycle ops**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** **FAM01** — shares a codebase with 19 other(s) via *shared_implementation*. A flaw here is a flaw in all 20 members.
  - siblings: 逆袭人生 `0xceFbf00b3732FE91e46989037E4b2564a4fc7777` (bsc); MarsCoin `0xFe189E97832DA1573e4e4Ff034F4fFC3a15c7777` (bsc); 金蝶圣甲 `0x4f0c550bFe484F957D5C7Dd26f9a630a92A17777` (bsc); QLM `0x1Df197D03967eD707E5AABc2c6Cf0c0d62cb7777` (bsc); 币有 `0xe9337Dde3dd9e97f1f45A56412767ce5098E7777` (bsc); Asian games `0x31d19B3633eBdb60Dc9d690b3e9eB1FFF61A7777` (bsc); CETS `0xB0c2aB5af4028461acE3f6e1C33a4eE1404E7777` (bsc); CBURN `0x309409237C4dB70Cd66067741eDcF02Bf69E7777` (bsc); 暴躁牛 `0x3A51dAE2Dc3D901A2cEfeD3Ad128116bf31C7777` (bsc); SUMMER `0xeEb3d73d4dd44e6E4d957d89492f05d5CCeE7777` (bsc); Max `0xe9Bc5C6A86caA44fD7b469bf3cc7c563E4F77777` (bsc); VenusCoin `0x5460b5E88799D27bbdf8A210926C17Dec18d7777` (bsc); Marvin `0xC6Bff31BbFa84d3c05AD61D8Ec47bE8B31517777` (bsc); Spark `0xC1073C967E323F2E197fA3975EC3b279974d7777` (bsc); gongsheng `0x70F7B593148283e7d84CeAB31407Bae0b5317777` (bsc); ASTEROID `0x330990DaE53BCa4C5811C5362B44C33a47db7777` (bsc); PIZZA `0x8554D38b95E4F7Ca11D391008627Df30B2b07777` (bsc); utility `0xEde00776439f9C49C592e43EeE34777a51847777` (bsc); bStocks `0x244B112Cf746e62A5DF723cbDe9906a6dEfd7777` (bsc)
- **Market:** pancakeswap · quote WBNB · pair `0x2D473fCF1113888a76e678bDf808e557422833a6` · [DexScreener](https://dexscreener.com/bsc/0x2D473fCF1113888a76e678bDf808e557422833a6)
- **Holders:** 21473
- **Why (score 49.5):** controls_reserve+10 lifecycle+5 surface_breadth+1.8 family_x20+28 liquidity+1.6 recency+3.1

## #47 · QLM · BNB Chain · score 49.2
*千里马*

- **Chain:** BNB Chain
- **Token address:** `0x1Df197D03967eD707E5AABc2c6Cf0c0d62cb7777`  ·  [explorer](https://bscscan.com/address/0x1Df197D03967eD707E5AABc2c6Cf0c0d62cb7777)
- **Liquidity:** $310,946 real quote-side  (headline $311,094)
- **Age / qualified by:** 36 days (≈ deployed 2026-07-10)
- **Custom logic:** impl/contract `FlapTaxTokenV3` — **lifecycle ops**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** **FAM01** — shares a codebase with 19 other(s) via *shared_implementation*. A flaw here is a flaw in all 20 members.
  - siblings: 逆袭人生 `0xceFbf00b3732FE91e46989037E4b2564a4fc7777` (bsc); MarsCoin `0xFe189E97832DA1573e4e4Ff034F4fFC3a15c7777` (bsc); 金蝶圣甲 `0x4f0c550bFe484F957D5C7Dd26f9a630a92A17777` (bsc); 币有 `0xe9337Dde3dd9e97f1f45A56412767ce5098E7777` (bsc); Asian games `0x31d19B3633eBdb60Dc9d690b3e9eB1FFF61A7777` (bsc); BoLe `0x5e4538460E07A12ea756fe1B774bf5C006797777` (bsc); CETS `0xB0c2aB5af4028461acE3f6e1C33a4eE1404E7777` (bsc); CBURN `0x309409237C4dB70Cd66067741eDcF02Bf69E7777` (bsc); 暴躁牛 `0x3A51dAE2Dc3D901A2cEfeD3Ad128116bf31C7777` (bsc); SUMMER `0xeEb3d73d4dd44e6E4d957d89492f05d5CCeE7777` (bsc); Max `0xe9Bc5C6A86caA44fD7b469bf3cc7c563E4F77777` (bsc); VenusCoin `0x5460b5E88799D27bbdf8A210926C17Dec18d7777` (bsc); Marvin `0xC6Bff31BbFa84d3c05AD61D8Ec47bE8B31517777` (bsc); Spark `0xC1073C967E323F2E197fA3975EC3b279974d7777` (bsc); gongsheng `0x70F7B593148283e7d84CeAB31407Bae0b5317777` (bsc); ASTEROID `0x330990DaE53BCa4C5811C5362B44C33a47db7777` (bsc); PIZZA `0x8554D38b95E4F7Ca11D391008627Df30B2b07777` (bsc); utility `0xEde00776439f9C49C592e43EeE34777a51847777` (bsc); bStocks `0x244B112Cf746e62A5DF723cbDe9906a6dEfd7777` (bsc)
- **Market:** pancakeswap · quote WBNB · pair `0xfC76cc56C5f0962fDBa127F5a582Df37FDA9CE71` · [DexScreener](https://dexscreener.com/bsc/0xfC76cc56C5f0962fDBa127F5a582Df37FDA9CE71)
- **Holders:** 11539
- **Why (score 49.2):** controls_reserve+10 lifecycle+5 surface_breadth+1.8 family_x20+28 liquidity+2 recency+2.4

## #48 · AIGO · BNB Chain · score 48.9

- **Chain:** BNB Chain
- **Token address:** `0xa6344A67780e2da01928FEFd9E558D792d7986dc`  ·  [explorer](https://bscscan.com/address/0xa6344A67780e2da01928FEFd9E558D792d7986dc)
- **Liquidity:** $2,918,876 real quote-side  (headline $2,920,686)
- **Age / qualified by:** 20 days (≈ deployed 2026-07-26)
- **Custom logic:** impl/contract `AIGOToken` — **fund ops, admin treasury pool signer, admin token mover, lifecycle ops, admin config gated**
  - key fns → fund: `emergencyWithdrawERC20`, `mint`, `setDailyLpBurnBps`, `triggerLiquidityBurn` · fund-mover: `emergencyWithdrawERC20`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0x55062dFf43cDBEa250c00368Fc9b5d279d3673CB` · [DexScreener](https://dexscreener.com/bsc/0x55062dFf43cDBEa250c00368Fc9b5d279d3673CB)
- **Holders:** 15341
- **Why (score 48.9):** fund_ops+12 admin_mover+10 admin_setters+6 lifecycle+5 surface_breadth+6 liquidity+5.9 recency+4

## #49 · VTA · BNB Chain · score 48.9
*VANTA*

- **Chain:** BNB Chain
- **Token address:** `0x57ecFb01f2FA4e8A768AaaE2B9fB4DC0CF9effff`  ·  [explorer](https://bscscan.com/address/0x57ecFb01f2FA4e8A768AaaE2B9fB4DC0CF9effff)
- **Liquidity:** $351,461 real quote-side
- **Age / qualified by:** 57 days (≈ deployed 2026-06-19)
- **Custom logic:** **fund ops, admin treasury pool signer, admin token mover, lifecycle ops, admin config gated**
  - key fns → fund: `setDistributionSettings` · fund-mover: `setAirdropNumbs`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote WBNB · pair `0xB745780A2Ae327dd4CCbA179a88836ecEe42cd56` · [DexScreener](https://dexscreener.com/bsc/0xB745780A2Ae327dd4CCbA179a88836ecEe42cd56)
- **Safety flags:** pausable|blacklist_fn
- **Holders:** 9735
- **Why (score 48.9):** fund_ops+12 admin_mover+10 admin_setters+6 lifecycle+5 surface_breadth+11.4 liquidity+2.2 recency+0.3 pausable+2

## #50 · MSFTB · BNB Chain · score 48.5
*Microsoft*

- **Chain:** BNB Chain
- **Token address:** `0x80106cb3EAD06659A5ad19DF39D9b4733863B9b0`  ·  [explorer](https://bscscan.com/address/0x80106cb3EAD06659A5ad19DF39D9b4733863B9b0)
- **Liquidity:** $145,563 real quote-side
- **Age / qualified by:** 24 days (≈ deployed 2026-07-22)
- **Custom logic:** **fund ops, admin treasury pool signer, lifecycle ops, admin config gated**
  - key fns → fund: `burn`, `mint`, `setBurnEnabled`, `setMintEnabled`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0xcfed6c4679297ea4889f8183bc057b4a86c64e46` (verified)
- **Shared codebase:** **FAM02** — shares a codebase with 9 other(s) via *shared_implementation*. A flaw here is a flaw in all 10 members.
  - siblings: SPCXB `0xbe9D156892E55e7154BcD3cB0FEA677F9D3103E1` (bsc); QQQB `0x205812CdBed920aFf76C6580abD681a46D11efc7` (bsc); SKHYB `0xCA750eF65f295BBECd685Abf54e82CAf297BDB61` (bsc); NVDAB `0x02Fca66C1D1aFB4E2A7884261eB00F63598a7436` (bsc); GMEB `0x46cEeFDa28Dd7207059ed19B0acdc026955bb15C` (bsc); GOOGLB `0x3F53De71c126BdaBAe20f9cD64848d317f6C3238` (bsc); AAPLB `0x431a3BEE82E2ca41e49895CbECE5bB0F76A89b7A` (bsc); SPYB `0x7138b48df7D98D7e3cc221BfE7192D0a178182D8` (bsc); TSLAB `0x5b1910eAaD6450E50f816082Aa078C41F10C292f` (bsc)
- **Market:** pancakeswap · quote USDT · pair `0x5018b018cEB7645c927c5Cf246786F89ebCbe7Ea` · [DexScreener](https://dexscreener.com/bsc/0x5018b018cEB7645c927c5Cf246786F89ebCbe7Ea)
- **Holders:** 3896
- **Why (score 48.5):** fund_ops+12 admin_setters+6 lifecycle+5 surface_breadth+7.2 family_x10+14 liquidity+0.7 recency+3.6

## #51 · SPYB · BNB Chain · score 48.4
*SPY*

- **Chain:** BNB Chain
- **Token address:** `0x7138b48df7D98D7e3cc221BfE7192D0a178182D8`  ·  [explorer](https://bscscan.com/address/0x7138b48df7D98D7e3cc221BfE7192D0a178182D8)
- **Liquidity:** $305,849 real quote-side
- **Age / qualified by:** 37 days (≈ deployed 2026-07-10)
- **Custom logic:** **fund ops, admin treasury pool signer, lifecycle ops, admin config gated**
  - key fns → fund: `burn`, `mint`, `setBurnEnabled`, `setMintEnabled`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0xcfed6c4679297ea4889f8183bc057b4a86c64e46` (verified)
- **Shared codebase:** **FAM02** — shares a codebase with 9 other(s) via *shared_implementation*. A flaw here is a flaw in all 10 members.
  - siblings: SPCXB `0xbe9D156892E55e7154BcD3cB0FEA677F9D3103E1` (bsc); QQQB `0x205812CdBed920aFf76C6580abD681a46D11efc7` (bsc); SKHYB `0xCA750eF65f295BBECd685Abf54e82CAf297BDB61` (bsc); NVDAB `0x02Fca66C1D1aFB4E2A7884261eB00F63598a7436` (bsc); GMEB `0x46cEeFDa28Dd7207059ed19B0acdc026955bb15C` (bsc); GOOGLB `0x3F53De71c126BdaBAe20f9cD64848d317f6C3238` (bsc); AAPLB `0x431a3BEE82E2ca41e49895CbECE5bB0F76A89b7A` (bsc); TSLAB `0x5b1910eAaD6450E50f816082Aa078C41F10C292f` (bsc); MSFTB `0x80106cb3EAD06659A5ad19DF39D9b4733863B9b0` (bsc)
- **Market:** pancakeswap · quote USDT · pair `0x7aA6d92Fc369A8C1EDc631A3aAc44eFB0808ddbF` · [DexScreener](https://dexscreener.com/bsc/0x7aA6d92Fc369A8C1EDc631A3aAc44eFB0808ddbF)
- **Holders:** 36685
- **Why (score 48.4):** fund_ops+12 admin_setters+6 lifecycle+5 surface_breadth+7.2 family_x10+14 liquidity+1.9 recency+2.3

## #52 · HAKE · BNB Chain · score 48.2

- **Chain:** BNB Chain
- **Token address:** `0x6F161448740241b01B034cB5c6B2fc34223Fad02`  ·  [explorer](https://bscscan.com/address/0x6F161448740241b01B034cB5c6B2fc34223Fad02)
- **Liquidity:** $421,182 real quote-side  (headline $421,188)
- **Age / qualified by:** 25 days (≈ deployed 2026-07-21)
- **Custom logic:** impl/contract `HAKE` — **fund ops, admin treasury pool signer, lifecycle ops, admin config gated**
  - key fns → fund: `claimBalance`, `claimToken`
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0xcffc8C19cfD66b445C612339C668Fa8cE1d2Ea19` · [DexScreener](https://dexscreener.com/bsc/0xcffc8C19cfD66b445C612339C668Fa8cE1d2Ea19)
- **Safety flags:** pausable|blacklist_fn
- **Holders:** 16595
- **Why (score 48.2):** fund_ops+12 controls_reserve+10 admin_setters+6 lifecycle+5 surface_breadth+7.2 liquidity+2.5 recency+3.5 pausable+2

## #53 · PEPGEM · BNB Chain · score 47.0

- **Chain:** BNB Chain
- **Token address:** `0x0fD1eBe9200DC1E587B8Ee82Ccbd2a13413532f2`  ·  [explorer](https://bscscan.com/address/0x0fD1eBe9200DC1E587B8Ee82Ccbd2a13413532f2)
- **Liquidity:** $247,198 real quote-side  (headline $247,200)
- **Age / qualified by:** 20 days (≈ deployed 2026-07-26)
- **Custom logic:** impl/contract `PEPGEMToken` — **fund ops, admin treasury pool signer, admin config gated**
  - key fns → fund: `setBurnDividendDistributor`, `setBurnExitMultiplier`, `setCommunityRewardsWallet`, `setDividendDistributor`, `setMaxBurnUSDPerTx`, `setMinBurnUSD`, `setNFTMinter`, `setPeppaBurnWallet`, `setReferralBurnDividend`
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0x3a4B1Ff7EFe14d16D353A862cD9e9d1fd4781D0e` · [DexScreener](https://dexscreener.com/bsc/0x3a4B1Ff7EFe14d16D353A862cD9e9d1fd4781D0e)
- **Safety flags:** pausable
- **Holders:** 10262
- **Why (score 47.0):** fund_ops+12 controls_reserve+10 admin_setters+6 surface_breadth+11.4 liquidity+1.6 recency+4 pausable+2

## #54 · 功夫女足 · BNB Chain · score 46.0

- **Chain:** BNB Chain
- **Token address:** `0x7122af246EBd72899268DcFa486d2E437A419527`  ·  [explorer](https://bscscan.com/address/0x7122af246EBd72899268DcFa486d2E437A419527)
- **Liquidity:** $257,435 real quote-side  (headline $257,507)
- **Age / qualified by:** 2 days (≈ deployed 2026-08-13)
- **Custom logic:** impl/contract `KungFuWomenFootballToken` — **fund ops, admin treasury pool signer, lifecycle ops, admin config gated**
  - key fns → fund: `setPumpVault`
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote WBNB · pair `0x3dC984dF68520E3269243Db6Adca691a031473E7` · [DexScreener](https://dexscreener.com/bsc/0x3dC984dF68520E3269243Db6Adca691a031473E7)
- **Safety flags:** pausable
- **Holders:** 10465
- **Why (score 46.0):** fund_ops+12 controls_reserve+10 admin_setters+6 lifecycle+5 surface_breadth+3.6 liquidity+1.6 recency+5.8 pausable+2

## #55 · GD · BNB Chain · score 45.9
*Golden Dragon*

- **Chain:** BNB Chain
- **Token address:** `0xe44D996fF1C6D9720C13C45431E665Afa9F88888`  ·  [explorer](https://bscscan.com/address/0xe44D996fF1C6D9720C13C45431E665Afa9F88888)
- **Liquidity:** $3,957,201 real quote-side
- **Age / qualified by:** 57 days (≈ deployed 2026-06-20)
- **Custom logic:** impl/contract `GD` — **fund ops, admin treasury pool signer, lifecycle ops, admin config gated**
  - key fns → fund: `claimToken`, `startMint`
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote WBNB · pair `0xbc01D46f8283A7b40c99E342C77AF733233511cE` · [DexScreener](https://dexscreener.com/bsc/0xbc01D46f8283A7b40c99E342C77AF733233511cE)
- **Holders:** 15677
- **Why (score 45.9):** fund_ops+12 controls_reserve+10 admin_setters+6 lifecycle+5 surface_breadth+6.6 liquidity+6 recency+0.3

## #56 · 67 · BNB Chain · score 44.8
*SIXSEVEN*

- **Chain:** BNB Chain
- **Token address:** `0xE7E569417D315Ef260778C09d289d7966213C452`  ·  [explorer](https://bscscan.com/address/0xE7E569417D315Ef260778C09d289d7966213C452)
- **Liquidity:** $142,128 real quote-side
- **Age / qualified by:** 20 days (≈ deployed 2026-07-26)
- **Custom logic:** impl/contract `TransparentUpgradeableProxy` — **admin treasury pool signer, bridge ops, lifecycle ops, proxy upgrade**
  - key fns → upgrade: `upgradeTo`, `upgradeToAndCall` · bridge: `lzReceive`, `lzReceiveAndRevert`, `lzReceiveSimulate`, `send`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0x658aeeb42a5232852797c0528304e949bb8d38cd` (verified)
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0xFfe68427490247F4151A7E8ef744c59f4fc98a13` · [DexScreener](https://dexscreener.com/bsc/0xFfe68427490247F4151A7E8ef744c59f4fc98a13)
- **Holders:** 2178
- **Why (score 44.8):** swappable_logic+14 bridge+8 admin_setters+6 lifecycle+5 surface_breadth+7.2 liquidity+0.6 recency+4

## #57 · STY · BNB Chain · score 44.3  ⚠️ **ALREADY EXPLOITED**
*SWAN TREASURY*

- **Chain:** BNB Chain
- **Token address:** `0xD6A4F5AADD88ebA9A170AcF67f737BD488142857`  ·  [explorer](https://bscscan.com/address/0xD6A4F5AADD88ebA9A170AcF67f737BD488142857)
- **Liquidity:** $3,106,397 real quote-side  (headline $3,111,297)
- **Age / qualified by:** 49 days (≈ deployed 2026-06-27)
- **Custom logic:** impl/contract `STYTOKEN` — **fund ops, admin treasury pool signer, lifecycle ops, admin config gated**
  - key fns → fund: `burn`, `burnFrom`, `cutAmmPoolToMinerReward`, `setMinerRewardContract`
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0x2BE23D76F423bf464F310aD98749d82691Ecc830` · [DexScreener](https://dexscreener.com/bsc/0x2BE23D76F423bf464F310aD98749d82691Ecc830)
- **Holders:** 5504
- **Exploit status:** EXPLOITED
- **Why (score 44.3):** fund_ops+12 controls_reserve+10 admin_setters+6 lifecycle+5 surface_breadth+4.2 liquidity+6 recency+1.1

## #58 · frxUSD · Ethereum · score 44.1
*Frax USD*

- **Chain:** Ethereum
- **Token address:** `0xCAcd6fd266aF91b8AeD52aCCc382b4e165586E29`  ·  [explorer](https://etherscan.io/address/0xCAcd6fd266aF91b8AeD52aCCc382b4e165586E29)
- **Liquidity:** $4,643,738 real quote-side  (headline $4,880,992)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 25 days (≈ deployed 2026-07-22)
- **Custom logic:** impl/contract `FrxUSD` — **fund ops, sig gated, lifecycle ops, admin config gated**
  - key fns → fund: `addMinter`, `burn`, `burnFrom`, `burnMany`, `minter_burn_from`, `minter_mint`, `removeMinter` · sig: `cancelAuthorization`, `receiveWithAuthorization`, `transferWithAuthorization`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0x0000000048d2c8baf31742f6765383278bada4d5` (verified)
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Deployer:** `0x5b35dbefb8b4918799246664ed3a7fe099619814`
- **Market:** curve · quote trUSD · pair `0xd1D954BC94c843815EC7b8119f2de00AF27Fa6Ff` · [DexScreener](https://dexscreener.com/ethereum/0xd1D954BC94c843815EC7b8119f2de00AF27Fa6Ff)
- **Holders:** 1777
- **Why (score 44.1):** fund_ops+12 sig_gated+8 lifecycle+5 surface_breadth+9.6 liquidity+6 recency+3.5

## #59 · COSM · BNB Chain · score 43.7

- **Chain:** BNB Chain
- **Token address:** `0x0D6aE45c96eC4df860300087462266e19140F6dc`  ·  [explorer](https://bscscan.com/address/0x0D6aE45c96eC4df860300087462266e19140F6dc)
- **Liquidity:** $124,367 real quote-side  (headline $124,381)
- **Age / qualified by:** 21 days (≈ deployed 2026-07-25)
- **Custom logic:** impl/contract `FatToken` — **admin treasury pool signer, admin token mover, lifecycle ops, admin config gated**
  - key fns → fund-mover: `setAirDropEnable`, `setAirdropNumbs`
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote WBNB · pair `0x40DdB4dd313615a255c59abD1aEf32Ba3f2222b5` · [DexScreener](https://dexscreener.com/bsc/0x40DdB4dd313615a255c59abD1aEf32Ba3f2222b5)
- **Safety flags:** owner_holds_100pct
- **Holders:** 391436
- **Why (score 43.7):** controls_reserve+10 admin_mover+10 admin_setters+6 lifecycle+5 surface_breadth+8.4 liquidity+0.4 recency+3.9

## #60 · BBTC · Ethereum · score 43.0
*Binance Wrapped BTC*

- **Chain:** Ethereum
- **Token address:** `0x9BE89D2a4cd102D8Fecc6BF9dA793be995C22541`  ·  [explorer](https://etherscan.io/address/0x9BE89D2a4cd102D8Fecc6BF9dA793be995C22541)
- **Liquidity:** $201,325 real quote-side  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 12 days (≈ deployed 2026-08-04)
- **Custom logic:** impl/contract `BinancePeggyToken` — **fund ops, lifecycle ops, proxy upgrade**
  - key fns → fund: `burn`, `claimOwnership`, `finishMinting`, `mint`, `reclaimToken` · upgrade: `upgradeTo`, `upgradeToAndCall`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0x9f344834752cb3a8c54c3ddcd41da4042b10d0b9` (verified)
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Deployer:** `0xa31556a0d64f2d022f553b6419d2de19ceaf802d`
- **Market:** uniswap · quote cbBTC · pair `0xa4dCDb1BCf688BcAA53B24f15cA859cFB83A3921` · [DexScreener](https://dexscreener.com/ethereum/0xa4dCDb1BCf688BcAA53B24f15cA859cFB83A3921)
- **Holders:** 52648
- **Why (score 43.0):** fund_ops+12 swappable_logic+14 lifecycle+5 surface_breadth+6 liquidity+1.2 recency+4.8

## #61 · DBURN · BNB Chain · score 42.3

- **Chain:** BNB Chain
- **Token address:** `0xDD2FeE7fc438AEA520e2678E9dDBebC5B7b63333`  ·  [explorer](https://bscscan.com/address/0xDD2FeE7fc438AEA520e2678E9dDBebC5B7b63333)
- **Liquidity:** $236,864 real quote-side
- **Age / qualified by:** 6 days (≈ deployed 2026-08-09)
- **Custom logic:** impl/contract `BurnToken` — **fund ops, admin treasury pool signer, lifecycle ops**
  - key fns → fund: `executePoolBurn`
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote WBNB · pair `0x12CA5BdF5fAE4B0fE7D2855c6799ae09218D6874` · [DexScreener](https://dexscreener.com/bsc/0x12CA5BdF5fAE4B0fE7D2855c6799ae09218D6874)
- **Holders:** 3215
- **Why (score 42.3):** fund_ops+12 controls_reserve+10 admin_setters+6 lifecycle+5 surface_breadth+2.4 liquidity+1.5 recency+5.4

## #62 · MAME · BNB Chain · score 42.1
*Mame Inu*

- **Chain:** BNB Chain
- **Token address:** `0xe92F7Fe3EAf61DF28b7B75f3FaAB199333c42302`  ·  [explorer](https://bscscan.com/address/0xe92F7Fe3EAf61DF28b7B75f3FaAB199333c42302)
- **Liquidity:** $805,510 real quote-side  (headline $805,510)
- **Age / qualified by:** 53 days (≈ deployed 2026-06-23)
- **Custom logic:** impl/contract `MAMEINU` — **fund ops, admin treasury pool signer, admin token mover, lifecycle ops**
  - key fns → fund: `excludeFromReward` · fund-mover: `rescueForeignToken`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote WBNB · pair `0x924F1a4422a89900FAaFa3F886721FDCcD6e086a` · [DexScreener](https://dexscreener.com/bsc/0x924F1a4422a89900FAaFa3F886721FDCcD6e086a)
- **Holders:** 8712
- **Why (score 42.1):** fund_ops+12 admin_mover+10 admin_setters+6 lifecycle+5 surface_breadth+4.8 liquidity+3.6 recency+0.7

## #63 · ALD · BNB Chain · score 40.4

- **Chain:** BNB Chain
- **Token address:** `0x3cBd513239d9E5538A4CAEd8ed53eF77009Df473`  ·  [explorer](https://bscscan.com/address/0x3cBd513239d9E5538A4CAEd8ed53eF77009Df473)
- **Liquidity:** $1,231,060 real quote-side
- **Age / qualified by:** 54 days (≈ deployed 2026-06-22)
- **Custom logic:** impl/contract `PandaToken` — **fund ops, admin treasury pool signer, lifecycle ops**
  - key fns → fund: `setClaims`
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote WBNB · pair `0xA25B52492B7177D115feEc6DC09084B1C3952F93` · [DexScreener](https://dexscreener.com/bsc/0xA25B52492B7177D115feEc6DC09084B1C3952F93)
- **Holders:** 8602
- **Why (score 40.4):** fund_ops+12 controls_reserve+10 admin_setters+6 lifecycle+5 surface_breadth+2.4 liquidity+4.4 recency+0.6

## #64 · PRISM · Ethereum · score 39.8

- **Chain:** Ethereum
- **Token address:** `0xCf4d29f14Cc585DDd1167F956092852AF844e040`  ·  [explorer](https://etherscan.io/address/0xCf4d29f14Cc585DDd1167F956092852AF844e040)
- **Liquidity:** $288,595 real quote-side  (headline $302,367)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 16 days (≈ deployed 2026-07-31)
- **Custom logic:** impl/contract `PrismHookV2` — **fund ops, lifecycle ops**
  - key fns → fund: `claim`, `claimMany`, `withdrawPending`, `withdrawPendingTo`
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Deployer:** `0xfe76f05a01163e5c90329a0d1a2c8e389fd0f110`
- **Market:** uniswap · quote ETH · pair `0x30850e19afc43b95e41b1fe35185762b4b631e63d07e91b0300c6e0c8cbf7146` · [DexScreener](https://dexscreener.com/ethereum/0x30850e19afc43b95e41b1fe35185762b4b631e63d07e91b0300c6e0c8cbf7146)
- **Safety flags:** external_call
- **Holders:** 770
- **Why (score 39.8):** fund_ops+12 controls_reserve+10 lifecycle+5 surface_breadth+3.6 liquidity+1.8 recency+4.4 external_call+3

## #65 · SLC · BNB Chain · score 39.6
*StarLink*

- **Chain:** BNB Chain
- **Token address:** `0x8AC96df1D3Dbd7c99A54CB4e50599cE129015E50`  ·  [explorer](https://bscscan.com/address/0x8AC96df1D3Dbd7c99A54CB4e50599cE129015E50)
- **Liquidity:** $11,164,260 real quote-side  (headline $11,168,114)
- **Age / qualified by:** 32 days (≈ deployed 2026-07-14)
- **Custom logic:** impl/contract `SLC` — **fund ops, admin treasury pool signer, admin config gated**
  - key fns → fund: `burn`, `burnFrom`, `mint`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0x6d7d33aB0D492aCC7122e0918dF54e2DCF35fb28` · [DexScreener](https://dexscreener.com/bsc/0x6d7d33aB0D492aCC7122e0918dF54e2DCF35fb28)
- **Safety flags:** mintable|hidden_owner
- **Holders:** 5926
- **Why (score 39.6):** fund_ops+12 admin_setters+6 surface_breadth+4.8 liquidity+6 recency+2.8 mintable+3 hidden_owner+5

## #66 · BF · BNB Chain · score 39.4

- **Chain:** BNB Chain
- **Token address:** `0x670225Aa919952c630764F5A7d36837c9f866666`  ·  [explorer](https://bscscan.com/address/0x670225Aa919952c630764F5A7d36837c9f866666)
- **Liquidity:** $239,644 real quote-side  (headline $239,647)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 33 days (≈ deployed 2026-07-13)
- **Custom logic:** impl/contract `BFToken` — **fund ops, admin treasury pool signer, admin config gated**
  - key fns → fund: `batchInitialDepositMotherFor`, `claimPendingNodeReward`, `claimPendingTeamReward`, `depositFor`, `distributeReleaseBatch`, `fundReleaseReserve`, `setDepositOperator`, `triggerLpReserveRelease`, `withdrawLP`
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote 都踏马得来 · pair `0x0D2Ecc05f8F38129d4Ff21585f050821F17De5cC` · [DexScreener](https://dexscreener.com/bsc/0x0D2Ecc05f8F38129d4Ff21585f050821F17De5cC)
- **Safety flags:** blacklist_fn
- **Holders:** 551
- **Why (score 39.4):** fund_ops+12 controls_reserve+10 admin_setters+6 surface_breadth+7.2 liquidity+1.5 recency+2.7

## #67 · DS · BNB Chain · score 38.8

- **Chain:** BNB Chain
- **Token address:** `0xEB112E3feb273fFC3ea6532724d53ec8EE388888`  ·  [explorer](https://bscscan.com/address/0xEB112E3feb273fFC3ea6532724d53ec8EE388888)
- **Liquidity:** $169,162 real quote-side  (headline $169,219)
- **Age / qualified by:** 11 days (≈ deployed 2026-08-05)
- **Custom logic:** impl/contract `DSToken` — **fund ops, admin treasury pool signer, admin config gated**
  - key fns → fund: `recycle`, `setStakePoolAddress`
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote WBNB · pair `0xca00fe1A387EcB65CbDd6E5aea3C4dea0eC18ad9` · [DexScreener](https://dexscreener.com/bsc/0xca00fe1A387EcB65CbDd6E5aea3C4dea0eC18ad9)
- **Safety flags:** pausable
- **Holders:** 3
- **Why (score 38.8):** fund_ops+12 controls_reserve+10 admin_setters+6 surface_breadth+3 liquidity+0.9 recency+4.9 pausable+2

## #68 · LC · BNB Chain · score 38.6
*LC Token*

- **Chain:** BNB Chain
- **Token address:** `0xe7ED99DDc65Ce315F187ac9CCdf59576E89DD82E`  ·  [explorer](https://bscscan.com/address/0xe7ED99DDc65Ce315F187ac9CCdf59576E89DD82E)
- **Liquidity:** $4,005,892 real quote-side  (headline $4,006,377)
- **Age / qualified by:** 24 days (≈ deployed 2026-07-22)
- **Custom logic:** impl/contract `ERC20TokenX` — **fund ops, admin treasury pool signer**
  - key fns → fund: `_burnFrom`, `burn`, `burnFrom`, `mint`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0xAaDf6272ba63E89926B691030143437996467E04` · [DexScreener](https://dexscreener.com/bsc/0xAaDf6272ba63E89926B691030143437996467E04)
- **Safety flags:** mintable|hidden_owner
- **Holders:** 26854
- **Why (score 38.6):** fund_ops+12 admin_setters+6 surface_breadth+3 liquidity+6 recency+3.6 mintable+3 hidden_owner+5

## #69 · VL · BNB Chain · score 38.5

- **Chain:** BNB Chain
- **Token address:** `0x87e22C22EE71788c3aba5F86372B0DbdB88A889e`  ·  [explorer](https://bscscan.com/address/0x87e22C22EE71788c3aba5F86372B0DbdB88A889e)
- **Liquidity:** $354,878 real quote-side  (headline $354,878)
- **Age / qualified by:** 43 days (≈ deployed 2026-07-03)
- **Custom logic:** impl/contract `VLToken` — **admin treasury pool signer, admin token mover, lifecycle ops, admin config gated**
  - key fns → fund-mover: `rescueBalance`, `rescuetoken`
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0xD20e3c6611c8Ed506ECA4e3C3a0E4437BC76eB85` · [DexScreener](https://dexscreener.com/bsc/0xD20e3c6611c8Ed506ECA4e3C3a0E4437BC76eB85)
- **Safety flags:** blacklist_fn
- **Holders:** 2014
- **Why (score 38.5):** controls_reserve+10 admin_mover+10 admin_setters+6 lifecycle+5 surface_breadth+3.6 liquidity+2.2 recency+1.7

## #70 · FWA · Ethereum · score 38.0
*Fake World Assets*

- **Chain:** Ethereum
- **Token address:** `0xa0Df17B5aC76ABaBA36E1450E2cbCd18A620C845`  ·  [explorer](https://etherscan.io/address/0xa0Df17B5aC76ABaBA36E1450E2cbCd18A620C845)
- **Liquidity:** $992,004 real quote-side  (headline $1,015,750)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 30 days (≈ deployed 2026-07-17)
- **Custom logic:** impl/contract `FWAToken` — **fund ops, admin treasury pool signer, admin config gated**
  - key fns → fund: `burn`, `setDistributor`
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Deployer:** `0x019817ad02a31b990433542097be29d97613e8cb`
- **Market:** uniswap · quote ETH · pair `0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d` · [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d)
- **Holders:** 3073
- **Why (score 38.0):** fund_ops+12 controls_reserve+10 admin_setters+6 surface_breadth+3 liquidity+4 recency+3

## #71 · DUCT · Arbitrum · score 37.4
*Dylan Utility And Community Token*

- **Chain:** Arbitrum
- **Token address:** `0xE004F86692780eC2717Ef402233fdE9D23d654D8`  ·  [explorer](https://arbiscan.io/address/0xE004F86692780eC2717Ef402233fdE9D23d654D8)
- **Liquidity:** $263,866 real quote-side  (headline $263,906)
- **Age / qualified by:** 13 days (≈ deployed 2026-08-02)
- **Custom logic:** impl/contract `DuctToken` — **fund ops, admin token mover**
  - key fns → fund: `approveRenounceMint`, `burn`, `cancelMintRequest`, `cancelRenounceMint`, `executeMint`, `executeRenounceMint`, `guardianApproveMint`, `requestMint`, `requestRenounceMint` · fund-mover: `recoverERC20`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Deployer:** `0xa1dbe7fac63c5c9a04c90d94a026d5568053798c`
- **Market:** uniswap · quote USDC · pair `0x48431ae417558Ce4653ecB0dBa5409713cf00c4C` · [DexScreener](https://dexscreener.com/arbitrum/0x48431ae417558Ce4653ecB0dBa5409713cf00c4C)
- **Safety flags:** mintable
- **Holders:** 62
- **Why (score 37.4):** fund_ops+12 admin_mover+10 surface_breadth+6 liquidity+1.7 recency+4.7 mintable+3

## #72 · CSC · BNB Chain · score 35.7
*Cubus Store Coin*

- **Chain:** BNB Chain
- **Token address:** `0x02962e4188902E05C4B1856E065551BCce10FFFf`  ·  [explorer](https://bscscan.com/address/0x02962e4188902E05C4B1856E065551BCce10FFFf)
- **Liquidity:** $834,317 real quote-side  (headline $834,556)
- **Age / qualified by:** 26 days (≈ deployed 2026-07-20)
- **Custom logic:** **fund ops, bridge ops, lifecycle ops, admin config gated**
  - key fns → fund: `claimFee` · bridge: `sendFee`, `sendToken`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote WBNB · pair `0xf55C23A434426B985D512E2e5519114A5d0249B6` · [DexScreener](https://dexscreener.com/bsc/0xf55C23A434426B985D512E2e5519114A5d0249B6)
- **Holders:** 1462
- **Why (score 35.7):** fund_ops+12 bridge+8 lifecycle+5 surface_breadth+3.6 liquidity+3.7 recency+3.4

## #73 · JACKET · BNB Chain · score 35.5
*REAL WORLD APPAREL*

- **Chain:** BNB Chain
- **Token address:** `0x57aeDac0cCaafDEc0ec62FC4fBFd8252735affff`  ·  [explorer](https://bscscan.com/address/0x57aeDac0cCaafDEc0ec62FC4fBFd8252735affff)
- **Liquidity:** $306,956 real quote-side  (headline $307,361)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 10 days (≈ deployed 2026-08-05)
- **Custom logic:** **fund ops, bridge ops, lifecycle ops, admin config gated**
  - key fns → fund: `claimFee` · bridge: `sendFee`, `sendToken`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote NVDAB · pair `0x5de5A5Da39a23a023B964C25d1A836F9eeA7CFD1` · [DexScreener](https://dexscreener.com/bsc/0x5de5A5Da39a23a023B964C25d1A836F9eeA7CFD1)
- **Holders:** 7880
- **Why (score 35.5):** fund_ops+12 bridge+8 lifecycle+5 surface_breadth+3.6 liquidity+1.9 recency+5

## #74 · DOS · BNB Chain · score 35.1
*DAPPOS*

- **Chain:** BNB Chain
- **Token address:** `0xB0f09ea9ae0515C3551080D4a745C8115aA30e37`  ·  [explorer](https://bscscan.com/address/0xB0f09ea9ae0515C3551080D4a745C8115aA30e37)
- **Liquidity:** $913,389 real quote-side
- **Age / qualified by:** 3 days (≈ deployed 2026-08-12)
- **Custom logic:** impl/contract `DapposTokenOFT` — **admin treasury pool signer, bridge ops, lifecycle ops**
  - key fns → bridge: `lzReceive`, `lzReceiveAndRevert`, `lzReceiveSimulate`, `send`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0xCbeAad783FFD2CeA125E9D9B2Ec21E639d20Fa59` · [DexScreener](https://dexscreener.com/bsc/0xCbeAad783FFD2CeA125E9D9B2Ec21E639d20Fa59)
- **Holders:** 3001
- **Why (score 35.1):** bridge+8 admin_setters+6 lifecycle+5 surface_breadth+6.6 liquidity+3.8 recency+5.7

## #75 · JF · BNB Chain · score 34.9

- **Chain:** BNB Chain
- **Token address:** `0xb723c2010fE240FFcd177BEdeD7e64E411c91313`  ·  [explorer](https://bscscan.com/address/0xb723c2010fE240FFcd177BEdeD7e64E411c91313)
- **Liquidity:** $108,186 real quote-side  (headline $108,187)
- **Age / qualified by:** 20 days (≈ deployed 2026-07-26)
- **Custom logic:** impl/contract `JF` — **fund ops, admin treasury pool signer, lifecycle ops, admin config gated**
  - key fns → fund: `claimContractToken`, `claimStuckETH`, `claimStuckToken`, `setBurnPersent`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0x5038ffA600d759689150DA17822b41018Fd70d12` · [DexScreener](https://dexscreener.com/bsc/0x5038ffA600d759689150DA17822b41018Fd70d12)
- **Holders:** 1070
- **Why (score 34.9):** fund_ops+12 admin_setters+6 lifecycle+5 surface_breadth+7.8 liquidity+0.1 recency+4

## #76 · SpaceXcoin · BNB Chain · score 34.8

- **Chain:** BNB Chain
- **Token address:** `0xf225e70162837A811C77Dc2bB413A5C06E97FfFf`  ·  [explorer](https://bscscan.com/address/0xf225e70162837A811C77Dc2bB413A5C06E97FfFf)
- **Liquidity:** $132,827 real quote-side  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 3 days (≈ deployed 2026-08-12)
- **Custom logic:** **fund ops, bridge ops, lifecycle ops, admin config gated**
  - key fns → fund: `claimFee` · bridge: `sendFee`, `sendToken`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote SPCXB · pair `0x9955ea00dD43747c9B5a49838a300291AD96A837` · [DexScreener](https://dexscreener.com/bsc/0x9955ea00dD43747c9B5a49838a300291AD96A837)
- **Holders:** 2311
- **Why (score 34.8):** fund_ops+12 bridge+8 lifecycle+5 surface_breadth+3.6 liquidity+0.5 recency+5.7

## #77 · VANRY · Base · score 33.5

- **Chain:** Base
- **Token address:** `0x07848a7b542a9cd856122C6c4Ab9ec87c44F8b63`  ·  [explorer](https://basescan.org/address/0x07848a7b542a9cd856122C6c4Ab9ec87c44F8b63)
- **Liquidity:** $261,729 real quote-side  (headline $261,781)
- **Age / qualified by:** 4 days (≈ deployed 2026-08-12)
- **Custom logic:** impl/contract `VANRY` — **fund ops, lifecycle ops, admin config gated**
  - key fns → fund: `burn`, `burnFrom`, `mint`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** aerodrome · quote WETH · pair `0xE5ff8a4Dc6F0DC2fE166392139FD1836E8591a8C` · [DexScreener](https://dexscreener.com/base/0xE5ff8a4Dc6F0DC2fE166392139FD1836E8591a8C)
- **Safety flags:** mintable|pausable
- **Holders:** 497
- **Why (score 33.5):** fund_ops+12 lifecycle+5 surface_breadth+4.2 liquidity+1.7 recency+5.6 mintable+3 pausable+2

## #78 · NEX · BNB Chain · score 32.9

- **Chain:** BNB Chain
- **Token address:** `0x3Da5E2EF39cB7530306cf14BaF3c86c201a69B48`  ·  [explorer](https://bscscan.com/address/0x3Da5E2EF39cB7530306cf14BaF3c86c201a69B48)
- **Liquidity:** $6,313,038 real quote-side  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 7 days (≈ deployed 2026-08-09)
- **Custom logic:** impl/contract `NEX` — **fund ops, admin treasury pool signer, admin config gated**
  - key fns → fund: `claimStuckTokens`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote AIC · pair `0x7cB4a44748b30C4a7D3576F4e771729F8B62B1F2` · [DexScreener](https://dexscreener.com/bsc/0x7cB4a44748b30C4a7D3576F4e771729F8B62B1F2)
- **Holders:** 118
- **Why (score 32.9):** fund_ops+12 admin_setters+6 surface_breadth+3.6 liquidity+6 recency+5.3

## #79 · HALO · Base · score 32.2

- **Chain:** Base
- **Token address:** `0xbbd27C575fB0e113219D610cc787B02Eeff71d42`  ·  [explorer](https://basescan.org/address/0xbbd27C575fB0e113219D610cc787B02Eeff71d42)
- **Liquidity:** $929,465 real quote-side  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 11 days (≈ deployed 2026-08-05)
- **Custom logic:** impl/contract `HaloToken` — **fund ops, admin treasury pool signer**
  - key fns → fund: `acceptMinterAdmin`, `applyMinter`, `burn`, `burnFrom`, `cancelMinter`, `mint`, `proposeMinter`, `setMinter`, `transferMinterAdmin`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** aerodrome · quote VIRTUAL · pair `0x85900924bD09898C73EF8B931691D069a943e54A` · [DexScreener](https://dexscreener.com/base/0x85900924bD09898C73EF8B931691D069a943e54A)
- **Holders:** 578
- **Why (score 32.2):** fund_ops+12 admin_setters+6 surface_breadth+5.4 liquidity+3.9 recency+4.9

## #80 · YH · BNB Chain · score 31.8

- **Chain:** BNB Chain
- **Token address:** `0xCF9F47937AF27a19b656DbCc462e1f99Ec999999`  ·  [explorer](https://bscscan.com/address/0xCF9F47937AF27a19b656DbCc462e1f99Ec999999)
- **Liquidity:** $973,484 real quote-side  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 28 days (≈ deployed 2026-07-19)
- **Custom logic:** impl/contract `YH` — **fund ops, admin treasury pool signer, admin config gated**
  - key fns → fund: `claimLP`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote HGDAO · pair `0x6bB3e44D04D7444ae2ccD98568DaFB8b915aCB03` · [DexScreener](https://dexscreener.com/bsc/0x6bB3e44D04D7444ae2ccD98568DaFB8b915aCB03)
- **Holders:** 14014
- **Why (score 31.8):** fund_ops+12 admin_setters+6 surface_breadth+6.6 liquidity+4 recency+3.2

## #81 · 宇树机器人 · BNB Chain · score 31.7

- **Chain:** BNB Chain
- **Token address:** `0xaA63730f078FF3C3B31e3521BD8E63A8a7a7297e`  ·  [explorer](https://bscscan.com/address/0xaA63730f078FF3C3B31e3521BD8E63A8a7a7297e)
- **Liquidity:** $201,361 real quote-side  (headline $201,381)
- **Age / qualified by:** 1 days (≈ deployed 2026-08-14)
- **Custom logic:** impl/contract `SimpleProxy11` — **proxy upgrade**
  - key fns → upgrade: `setImplementation`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0xdd82c0ee3553c8a659aaebc60a2fcc82ed1c1489` (UNVERIFIED impl ⚠)
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote WBNB · pair `0x207fB72397ddE915D0d48427F77ff26bBcFf2BAE` · [DexScreener](https://dexscreener.com/bsc/0x207fB72397ddE915D0d48427F77ff26bBcFf2BAE)
- **Safety flags:** SAFETY_CHECK_UNAVAILABLE
- **Why (score 31.7):** swappable_logic+14 surface_breadth+0.6 unverified_impl+10 liquidity+1.2 recency+5.9

## #82 · MIZU · BNB Chain · score 31.5
*MIZU KAPPA*

- **Chain:** BNB Chain
- **Token address:** `0xb1D1F602034F7c4b242169b818200d07C117FfFF`  ·  [explorer](https://bscscan.com/address/0xb1D1F602034F7c4b242169b818200d07C117FfFF)
- **Liquidity:** $147,503 real quote-side  (headline $147,518)
- **Age / qualified by:** 38 days (≈ deployed 2026-07-09)
- **Custom logic:** **fund ops, bridge ops, lifecycle ops, admin config gated**
  - key fns → fund: `claimFee` · bridge: `sendFee`, `sendToken`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote WBNB · pair `0xebCEb9c56F7011A424E895bc3F48b1F7229ee4E3` · [DexScreener](https://dexscreener.com/bsc/0xebCEb9c56F7011A424E895bc3F48b1F7229ee4E3)
- **Holders:** 1433
- **Why (score 31.5):** fund_ops+12 bridge+8 lifecycle+5 surface_breadth+3.6 liquidity+0.7 recency+2.2

## #83 · ZX · BNB Chain · score 31.4
*Zirix*

- **Chain:** BNB Chain
- **Token address:** `0x45578E017c5014F06d5DA1707EEA7AFAec295437`  ·  [explorer](https://bscscan.com/address/0x45578E017c5014F06d5DA1707EEA7AFAec295437)
- **Liquidity:** $175,874 real quote-side  (headline $175,875)
- **Age / qualified by:** 10 days (≈ deployed 2026-08-05)
- **Custom logic:** impl/contract `ZirixTokenContract` — **fund ops, admin treasury pool signer, lifecycle ops, admin config gated**
  - key fns → fund: `burn`, `burnFrom`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0xF153fe4e7D71e7c1c8aE29344BD28991Fd160e8d` · [DexScreener](https://dexscreener.com/bsc/0xF153fe4e7D71e7c1c8aE29344BD28991Fd160e8d)
- **Holders:** 140
- **Why (score 31.4):** fund_ops+12 admin_setters+6 lifecycle+5 surface_breadth+2.4 liquidity+1 recency+5

## #84 · CDAO · BNB Chain · score 31.0  ⚠️ **ALREADY EXPLOITED**
*CDAO Token*

- **Chain:** BNB Chain
- **Token address:** `0xa9d33E9203E7d4B9EA8f37Eca73CFe810C5d7cD0`  ·  [explorer](https://bscscan.com/address/0xa9d33E9203E7d4B9EA8f37Eca73CFe810C5d7cD0)
- **Liquidity:** $10,803,648 real quote-side  (headline $10,832,478)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 56 days (≈ deployed 2026-06-20)
- **Custom logic:** impl/contract `CDaoToken` — **admin treasury pool signer, lifecycle ops, admin config gated**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote Pro · pair `0x86aC451a0c0bcAc5b74116Ae90832e89E9c630df` · [DexScreener](https://dexscreener.com/bsc/0x86aC451a0c0bcAc5b74116Ae90832e89E9c630df)
- **Holders:** 136209
- **Exploit status:** EXPLOITED (paired contract)
- **Why (score 31.0):** controls_reserve+10 admin_setters+6 lifecycle+5 surface_breadth+3.6 liquidity+6 recency+0.4

## #85 · SpaceXcoin · BNB Chain · score 30.9

- **Chain:** BNB Chain
- **Token address:** `0x0B175544Cf87Bf3f17Df828b1156A44018b328fA`  ·  [explorer](https://bscscan.com/address/0x0B175544Cf87Bf3f17Df828b1156A44018b328fA)
- **Liquidity:** $127,188 real quote-side
- **Age / qualified by:** 1 days (≈ deployed 2026-08-14)
- **Custom logic:** impl/contract `ProxyV2` — **proxy upgrade**
  - key fns → upgrade: `setImplementation`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0xba4c3893ef98a2c7a38146201c1ea82463f067a3` (UNVERIFIED impl ⚠)
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote WBNB · pair `0xcA059e284e74C351600fD339dd474F80995D60EA` · [DexScreener](https://dexscreener.com/bsc/0xcA059e284e74C351600fD339dd474F80995D60EA)
- **Holders:** 930390
- **Why (score 30.9):** swappable_logic+14 surface_breadth+0.6 unverified_impl+10 liquidity+0.4 recency+5.9

## #86 · ETHFI · Ethereum · score 30.7
*ether.fi governance token*

- **Chain:** Ethereum
- **Token address:** `0xFe0c30065B384F05761f15d0CC899D4F9F9Cc0eB`  ·  [explorer](https://etherscan.io/address/0xFe0c30065B384F05761f15d0CC899D4F9F9Cc0eB)
- **Liquidity:** $708,132 real quote-side  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 5 days (≈ deployed 2026-08-11)
- **Custom logic:** impl/contract `EtherFiGovernanceToken` — **fund ops, sig gated**
  - key fns → fund: `burn`, `burnFrom` · sig: `delegateBySig`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Deployer:** `0x2460bcb0a36b4072273498c38a1894235e20f1cd`
- **Market:** uniswap · quote ETH · pair `0x2e9eef85c2822c6ec9ee3d3e7da32873797c478de9815ca3021c4b21665b619d` · [DexScreener](https://dexscreener.com/ethereum/0x2e9eef85c2822c6ec9ee3d3e7da32873797c478de9815ca3021c4b21665b619d)
- **Holders:** 108296
- **Why (score 30.7):** fund_ops+12 sig_gated+8 surface_breadth+1.8 liquidity+3.4 recency+5.5

## #87 · USDe · Ethereum · score 30.6

- **Chain:** Ethereum
- **Token address:** `0x4c9EDD5852cd905f086C759E8383e09bff1E68B3`  ·  [explorer](https://etherscan.io/address/0x4c9EDD5852cd905f086C759E8383e09bff1E68B3)
- **Liquidity:** $974,652 real quote-side
- **Age / qualified by:** 28 days (≈ deployed 2026-07-18)
- **Custom logic:** impl/contract `USDe` — **fund ops, admin treasury pool signer**
  - key fns → fund: `burn`, `burnFrom`, `mint`, `setMinter`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Deployer:** `0x8de54b1cefedeab1766b947c7d9a9963436e8fae`
- **Market:** uniswap · quote USDC · pair `0x56fc29b86900aa0afa6e20b020429bffba1105cfb45070492c67529b46eb48c1` · [DexScreener](https://dexscreener.com/ethereum/0x56fc29b86900aa0afa6e20b020429bffba1105cfb45070492c67529b46eb48c1)
- **Safety flags:** mintable
- **Holders:** 48777
- **Why (score 30.6):** fund_ops+12 admin_setters+6 surface_breadth+2.4 liquidity+4 recency+3.2 mintable+3

## #88 · syrupUSDG · Ethereum · score 30.2

- **Chain:** Ethereum
- **Token address:** `0x87b65C4aAFFA76881f9E96F3e7ED945ddFC3Cd7A`  ·  [explorer](https://etherscan.io/address/0x87b65C4aAFFA76881f9E96F3e7ED945ddFC3Cd7A)
- **Liquidity:** $994,000 real quote-side  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 26 days (≈ deployed 2026-07-21)
- **Custom logic:** impl/contract `MaplePool` — **fund ops**
  - key fns → fund: `deposit`, `depositWithPermit`, `mint`, `mintWithPermit`, `redeem`, `requestRedeem`, `requestWithdraw`, `withdraw`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Deployer:** `0x54e28bb2d530ee10386dbca6e7e84efac809292c`
- **Market:** uniswap · quote USDG · pair `0x7a52ba9092e364c766820ed007fd0fc13be21290d329eaade1948c984c821f2d` · [DexScreener](https://dexscreener.com/ethereum/0x7a52ba9092e364c766820ed007fd0fc13be21290d329eaade1948c984c821f2d)
- **Safety flags:** mintable|external_call
- **Holders:** 49
- **Why (score 30.2):** fund_ops+12 surface_breadth+4.8 liquidity+4 recency+3.4 mintable+3 external_call+3

## #89 · TAOT · Base · score 29.9

- **Chain:** Base
- **Token address:** `0x7f2f00e54Dcaa8b248BDfD75Da2ae859d4d8FF3E`  ·  [explorer](https://basescan.org/address/0x7f2f00e54Dcaa8b248BDfD75Da2ae859d4d8FF3E)
- **Liquidity:** $211,774 real quote-side  (headline $211,776)
- **Age / qualified by:** 40 days (≈ deployed 2026-07-06)
- **Custom logic:** impl/contract `TAOT` — **fund ops, bridge ops, admin config gated**
  - key fns → fund: `bridgeBurnFrom`, `bridgeMint` · bridge: `bridgeBurnFrom`, `bridgeMint`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** aerodrome · quote USDC · pair `0xc4FbB564D11A36b71d0152A1A8CDdec709e20908` · [DexScreener](https://dexscreener.com/base/0xc4FbB564D11A36b71d0152A1A8CDdec709e20908)
- **Safety flags:** mintable
- **Holders:** 705
- **Why (score 29.9):** fund_ops+12 bridge+8 surface_breadth+3.6 liquidity+1.3 recency+2 mintable+3

## #90 · Romantic · BNB Chain · score 29.1

- **Chain:** BNB Chain
- **Token address:** `0xb45a6Ce5437eBE421b341E5bb92508432Ce99999`  ·  [explorer](https://bscscan.com/address/0xb45a6Ce5437eBE421b341E5bb92508432Ce99999)
- **Liquidity:** $327,887 real quote-side
- **Age / qualified by:** 20 days (≈ deployed 2026-07-26)
- **Custom logic:** impl/contract `GGGTOKEN` — **admin treasury pool signer, lifecycle ops, admin config gated**
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote WBNB · pair `0xb7A39286Bff6cdc84fF4ca43B832B3011a3e0963` · [DexScreener](https://dexscreener.com/bsc/0xb7A39286Bff6cdc84fF4ca43B832B3011a3e0963)
- **Safety flags:** blacklist_fn
- **Holders:** 26746
- **Why (score 29.1):** admin_setters+6 lifecycle+5 surface_breadth+12 liquidity+2.1 recency+4

## #91 · BRC · BNB Chain · score 28.9
*BearWin*

- **Chain:** BNB Chain
- **Token address:** `0xc69EEAD86a8249A768708DBA88001FEb90068888`  ·  [explorer](https://bscscan.com/address/0xc69EEAD86a8249A768708DBA88001FEb90068888)
- **Liquidity:** $148,801 real quote-side  (headline $148,816)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 18 days (≈ deployed 2026-07-29)
- **Custom logic:** impl/contract `ABRCTOKEN` — **admin treasury pool signer, admin token mover, lifecycle ops, admin config gated**
  - key fns → fund-mover: `rescueToken`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote BW · pair `0x040C925D68A32Ffa6199DADA68b4b9751f07DDB0` · [DexScreener](https://dexscreener.com/bsc/0x040C925D68A32Ffa6199DADA68b4b9751f07DDB0)
- **Holders:** 15594
- **Why (score 28.9):** admin_mover+10 admin_setters+6 lifecycle+5 surface_breadth+3 liquidity+0.7 recency+4.2

## #92 · WROON · BNB Chain · score 28.9

- **Chain:** BNB Chain
- **Token address:** `0x44Ff8893e4f245c772486134589AbA54f9Cb95BB`  ·  [explorer](https://bscscan.com/address/0x44Ff8893e4f245c772486134589AbA54f9Cb95BB)
- **Liquidity:** $120,502 real quote-side  (headline $120,502)
- **Age / qualified by:** 10 days (≈ deployed 2026-08-05)
- **Custom logic:** impl/contract `WROON` — **fund ops, admin treasury pool signer, admin config gated**
  - key fns → fund: `burn`, `burnFrom`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDC · pair `0x575D5eAEAD1e1700b97BE9778E76d9145F30efaA` · [DexScreener](https://dexscreener.com/bsc/0x575D5eAEAD1e1700b97BE9778E76d9145F30efaA)
- **Safety flags:** pausable|owner_holds_50pct
- **Holders:** 5167
- **Why (score 28.9):** fund_ops+12 admin_setters+6 surface_breadth+3.6 liquidity+0.3 recency+5 pausable+2

## #93 · GREEN · Ethereum · score 28.9

- **Chain:** Ethereum
- **Token address:** `0xb2089A7069861C8D90c8dA3aaCAB8e9188C0C531`  ·  [explorer](https://etherscan.io/address/0xb2089A7069861C8D90c8dA3aaCAB8e9188C0C531)
- **Liquidity:** $143,464 real quote-side  (headline $2,065,469)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 45 days (≈ deployed 2026-07-01)
- **Custom logic:** impl/contract `Green` — **fund ops, admin token mover**
  - key fns → fund: `burn`, `distributeMinting` · fund-mover: `transferAnyERC20Token`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Deployer:** `0x3c51167a3c99901ee21d949adad23106b068e7f9`
- **Market:** uniswap · quote GULD · pair `0x93f900e15be5ee054dd9a874e4ecdafd2a4f27e86424ab3a4f50af84eb51dad8` · [DexScreener](https://dexscreener.com/ethereum/0x93f900e15be5ee054dd9a874e4ecdafd2a4f27e86424ab3a4f50af84eb51dad8)
- **Safety flags:** mintable
- **Holders:** 11696
- **Why (score 28.9):** fund_ops+12 admin_mover+10 surface_breadth+1.8 liquidity+0.6 recency+1.5 mintable+3

## #94 · H · Ethereum · score 28.8
*Humanity*

- **Chain:** Ethereum
- **Token address:** `0xE76c5b78f93909d34404E9eb4C1f19e7582a5dE1`  ·  [explorer](https://etherscan.io/address/0xE76c5b78f93909d34404E9eb4C1f19e7582a5dE1)
- **Liquidity:** $1,164,581 real quote-side
- **Age / qualified by:** 3 days (≈ deployed 2026-08-12)
- **Custom logic:** impl/contract `HToken` — **fund ops, lifecycle ops**
  - key fns → fund: `burn`, `mint`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0x85d0b85f290ba575c50a6be38f24f9e99f94e7d3` (verified)
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Deployer:** `0x04a15e0850e534751a16c2b67e137e31bcef8e0f`
- **Market:** uniswap · quote USDT · pair `0xbe26d0e86426f365a1fe963e58c77432911ac6a61a3141b341b774f00b4ce3d8` · [DexScreener](https://dexscreener.com/ethereum/0xbe26d0e86426f365a1fe963e58c77432911ac6a61a3141b341b774f00b4ce3d8)
- **Holders:** 183045
- **Why (score 28.8):** fund_ops+12 lifecycle+5 surface_breadth+1.8 liquidity+4.3 recency+5.7

## #95 · MC · BNB Chain · score 28.6
*MC Token*

- **Chain:** BNB Chain
- **Token address:** `0x0a4D87F0b646F29aEAED09A2573AD1FF74bBba62`  ·  [explorer](https://bscscan.com/address/0x0a4D87F0b646F29aEAED09A2573AD1FF74bBba62)
- **Liquidity:** $1,639,496 real quote-side  (headline $1,639,497)
- **Age / qualified by:** 51 days (≈ deployed 2026-06-25)
- **Custom logic:** impl/contract `MCToken` — **admin treasury pool signer, lifecycle ops, admin config gated**
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0x1d26B5168f33d9bdF8d43887612C1b68bC27B121` · [DexScreener](https://dexscreener.com/bsc/0x1d26B5168f33d9bdF8d43887612C1b68bC27B121)
- **Safety flags:** pausable|hidden_owner
- **Holders:** 7446
- **Why (score 28.6):** admin_setters+6 lifecycle+5 surface_breadth+4.8 liquidity+4.9 recency+0.9 pausable+2 hidden_owner+5

## #96 · 喵喵币 · BNB Chain · score 27.0

- **Chain:** BNB Chain
- **Token address:** `0xd9D3dAd2EfeD7eE99F1363FAC549f5E476F19A5a`  ·  [explorer](https://bscscan.com/address/0xd9D3dAd2EfeD7eE99F1363FAC549f5E476F19A5a)
- **Liquidity:** $1,759,282 real quote-side  (headline $1,759,283)
- **Age / qualified by:** 16 days (≈ deployed 2026-07-31)
- **Custom logic:** impl/contract `MMToken` — **admin treasury pool signer, lifecycle ops, admin config gated**
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0x6f6A6eAbBf07af11EA58Ba523cF74618F45FD190` · [DexScreener](https://dexscreener.com/bsc/0x6f6A6eAbBf07af11EA58Ba523cF74618F45FD190)
- **Holders:** 79750
- **Why (score 27.0):** admin_setters+6 lifecycle+5 surface_breadth+6.6 liquidity+5 recency+4.4

## #97 · SFIG · BNB Chain · score 26.6

- **Chain:** BNB Chain
- **Token address:** `0x25F0ff2338174872e9C294d5D2fe736454321378`  ·  [explorer](https://bscscan.com/address/0x25F0ff2338174872e9C294d5D2fe736454321378)
- **Liquidity:** $3,651,794 real quote-side  (headline $3,669,710)
- **Age / qualified by:** 18 days (≈ deployed 2026-07-28)
- **Custom logic:** impl/contract `SFIG` — **admin treasury pool signer, lifecycle ops, admin config gated**
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0xEa862b187E7870cB88653D780AAE7f51523916e3` · [DexScreener](https://dexscreener.com/bsc/0xEa862b187E7870cB88653D780AAE7f51523916e3)
- **Holders:** 2375
- **Why (score 26.6):** admin_setters+6 lifecycle+5 surface_breadth+5.4 liquidity+6 recency+4.2

## #98 · CDXR · Ethereum · score 26.6
*Codex*

- **Chain:** Ethereum
- **Token address:** `0x40AAf75454036Bed56F3266cCf18f6b7befd6Aca`  ·  [explorer](https://etherscan.io/address/0x40AAf75454036Bed56F3266cCf18f6b7befd6Aca)
- **Liquidity:** $1,961,855 real quote-side  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 30 days (≈ deployed 2026-07-16)
- **Custom logic:** **fund ops**
  - key fns → fund: `mint`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** **FAM05** — shares a codebase with 1 other(s) via *identical_bytecode, identical_source*. A flaw here is a flaw in all 2 members.
  - siblings: GULD `0x14D6C649292c5c9790c5196D1a9EA039307947a1` (eth)
- **Deployer:** `0xf39c9feb0bd7d8643ffea8df9d89b8d3f7403441`
- **Market:** uniswap · quote GROW · pair `0x9f78fbfd4ae6a0251556764875d1c2a08681b7daf8c1461cbb72063412533f16` · [DexScreener](https://dexscreener.com/ethereum/0x9f78fbfd4ae6a0251556764875d1c2a08681b7daf8c1461cbb72063412533f16)
- **Safety flags:** mintable
- **Holders:** 1248
- **Why (score 26.6):** fund_ops+12 surface_breadth+0.6 family_x2+2.8 liquidity+5.2 recency+3 mintable+3

## #99 · SST · BNB Chain · score 26.4
*Smart Solve Token*

- **Chain:** BNB Chain
- **Token address:** `0x8dB27FB78c89975202f550697cE8Acb2E74B2469`  ·  [explorer](https://bscscan.com/address/0x8dB27FB78c89975202f550697cE8Acb2E74B2469)
- **Liquidity:** $2,231,620 real quote-side  (headline $2,231,621)
- **Age / qualified by:** 48 days (≈ deployed 2026-06-28)
- **Custom logic:** impl/contract `SmartSolveToken` — **fund ops, admin treasury pool signer**
  - key fns → fund: `burn`, `burnFrom`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0x850Dd77984103Ccd6a732126Ce3A1319993E9355` · [DexScreener](https://dexscreener.com/bsc/0x850Dd77984103Ccd6a732126Ce3A1319993E9355)
- **Holders:** 6906
- **Why (score 26.4):** fund_ops+12 admin_setters+6 surface_breadth+1.8 liquidity+5.4 recency+1.2

## #100 · FCO · BNB Chain · score 26.3
*FCO Token*

- **Chain:** BNB Chain
- **Token address:** `0xcD1829e826249f41a5Cb434Bf2d25C3D5eA78eC0`  ·  [explorer](https://bscscan.com/address/0xcD1829e826249f41a5Cb434Bf2d25C3D5eA78eC0)
- **Liquidity:** $820,269 real quote-side  (headline $820,439)
- **Age / qualified by:** 24 days (≈ deployed 2026-07-22)
- **Custom logic:** impl/contract `TokenFCO` — **admin treasury pool signer, admin token mover, admin config gated**
  - key fns → fund-mover: `rescueToken`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0x2925340Dd64472A71D32aa9Bec6176f541595d97` · [DexScreener](https://dexscreener.com/bsc/0x2925340Dd64472A71D32aa9Bec6176f541595d97)
- **Holders:** 10486
- **Why (score 26.3):** admin_mover+10 admin_setters+6 surface_breadth+3 liquidity+3.7 recency+3.6

## #101 · PRD · Ethereum · score 26.2
*PRDCTR*

- **Chain:** Ethereum
- **Token address:** `0xc84782858B7Bef5d25182Dbac956A6Aa463AeFE5`  ·  [explorer](https://etherscan.io/address/0xc84782858B7Bef5d25182Dbac956A6Aa463AeFE5)
- **Liquidity:** $983,924 real quote-side  (headline $4,458,858)
- **Age / qualified by:** 46 days (≈ deployed 2026-06-30)
- **Custom logic:** impl/contract `ConfigurableTokenUpgradeable` — **lifecycle ops, proxy upgrade**
  - key fns → upgrade: `upgradeToAndCall`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0x3e936df533ba0d625453c24194dc2efe76aae437` (verified)
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Deployer:** `0x528e271f811007f53afe6771aaa75fd9f771a5c2`
- **Market:** uniswap · quote USDT · pair `0x45aECbBCc9B5414bcfD84f1aE5F3d9f5488ba403` · [DexScreener](https://dexscreener.com/ethereum/0x45aECbBCc9B5414bcfD84f1aE5F3d9f5488ba403)
- **Holders:** 478
- **Why (score 26.2):** swappable_logic+14 lifecycle+5 surface_breadth+1.8 liquidity+4 recency+1.4

## #102 · usocks · Ethereum · score 25.3

- **Chain:** Ethereum
- **Token address:** `0x2E43E18a19Ae896c6f8657Ca6285b9672f67F7D2`  ·  [explorer](https://etherscan.io/address/0x2E43E18a19Ae896c6f8657Ca6285b9672f67F7D2)
- **Liquidity:** $109,161 real quote-side  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 3 days (≈ deployed 2026-08-13)
- **Custom logic:** impl/contract `USocks` — **fund ops**
  - key fns → fund: `burn`, `claim`, `claimBatch`, `depositFees`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Deployer:** `0x9b8ca6e01842e65406218e10ca02cf46a2c231b9`
- **Market:** uniswap · quote ETH · pair `0x18adf6fa633dfadb0aaa108b5773f9a878b293ee180c6b7da8db9a3f88c3bfcf` · [DexScreener](https://dexscreener.com/ethereum/0x18adf6fa633dfadb0aaa108b5773f9a878b293ee180c6b7da8db9a3f88c3bfcf)
- **Safety flags:** pausable|external_call
- **Holders:** 466
- **Why (score 25.3):** fund_ops+12 surface_breadth+2.4 liquidity+0.2 recency+5.7 pausable+2 external_call+3

## #103 · ELMT · Ethereum · score 24.6
*Element*

- **Chain:** Ethereum
- **Token address:** `0x600D601D8b9EB5DE5Ac90fEfC68d0d08801bFd3f`  ·  [explorer](https://etherscan.io/address/0x600D601D8b9EB5DE5Ac90fEfC68d0d08801bFd3f)
- **Liquidity:** $674,003 real quote-side  (headline $2,960,659)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 45 days (≈ deployed 2026-07-01)
- **Custom logic:** **fund ops**
  - key fns → fund: `mint`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** **FAM04** — shares a codebase with 2 other(s) via *identical_bytecode, identical_source*. A flaw here is a flaw in all 3 members.
  - siblings: GIVE `0x95669A6589A81A6704bab1020722d0C405841885` (eth); SWITCH `0xb10cc888cB2CcE7036F4c7ECAd8a57Da16161338` (eth)
- **Deployer:** `0xf07b976cd03da5c844f47f1b2570e87bb6c22c21`
- **Market:** uniswap · quote GULD · pair `0xc8e2ead0f86c658becc7fe0f6acc4e528b87b22bebc7dffa6848810282614078` · [DexScreener](https://dexscreener.com/ethereum/0xc8e2ead0f86c658becc7fe0f6acc4e528b87b22bebc7dffa6848810282614078)
- **Safety flags:** mintable
- **Holders:** 11382
- **Why (score 24.6):** fund_ops+12 surface_breadth+0.6 family_x3+4.2 liquidity+3.3 recency+1.5 mintable+3

## #104 · SWITCH · Ethereum · score 24.5

- **Chain:** Ethereum
- **Token address:** `0xb10cc888cB2CcE7036F4c7ECAd8a57Da16161338`  ·  [explorer](https://etherscan.io/address/0xb10cc888cB2CcE7036F4c7ECAd8a57Da16161338)
- **Liquidity:** $640,646 real quote-side  (headline $1,837,907)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 45 days (≈ deployed 2026-07-01)
- **Custom logic:** **fund ops**
  - key fns → fund: `mint`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** **FAM04** — shares a codebase with 2 other(s) via *identical_bytecode, identical_source*. A flaw here is a flaw in all 3 members.
  - siblings: ELMT `0x600D601D8b9EB5DE5Ac90fEfC68d0d08801bFd3f` (eth); GIVE `0x95669A6589A81A6704bab1020722d0C405841885` (eth)
- **Deployer:** `0x17c3ed160112dcafa76a118dbd3ce6e8afa1852e`
- **Market:** uniswap · quote GULD · pair `0x264984e00973c1dd3e2e145687715f211568eb7685af5527bcee61a1e6812675` · [DexScreener](https://dexscreener.com/ethereum/0x264984e00973c1dd3e2e145687715f211568eb7685af5527bcee61a1e6812675)
- **Safety flags:** mintable
- **Holders:** 18029
- **Why (score 24.5):** fund_ops+12 surface_breadth+0.6 family_x3+4.2 liquidity+3.2 recency+1.5 mintable+3

## #105 · BTCΞ · BNB Chain · score 24.4

- **Chain:** BNB Chain
- **Token address:** `0xb1939843fB9220719d13076dCeEfb0aeaeF06666`  ·  [explorer](https://bscscan.com/address/0xb1939843fB9220719d13076dCeEfb0aeaeF06666)
- **Liquidity:** $1,524,341 real quote-side  (headline $1,524,353)
- **Age / qualified by:** 35 days (≈ deployed 2026-07-11)
- **Custom logic:** impl/contract `BTToken` — **admin treasury pool signer, admin config gated**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote BTCB · pair `0x3cC292bB0011951F3151eB998816c31680a2Ce87` · [DexScreener](https://dexscreener.com/bsc/0x3cC292bB0011951F3151eB998816c31680a2Ce87)
- **Holders:** 7160
- **Why (score 24.4):** controls_reserve+10 admin_setters+6 surface_breadth+1.2 liquidity+4.7 recency+2.5

## #106 · WG · BNB Chain · score 24.4
*Whitegold*

- **Chain:** BNB Chain
- **Token address:** `0xbC2751Efe1bF9dd72230a62C40E3FFE87D415013`  ·  [explorer](https://bscscan.com/address/0xbC2751Efe1bF9dd72230a62C40E3FFE87D415013)
- **Liquidity:** $100,828 real quote-side  (headline $100,880)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 44 days (≈ deployed 2026-07-02)
- **Custom logic:** impl/contract `WhiteGold` — **admin treasury pool signer, lifecycle ops, admin config gated**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote GOLD · pair `0xA0B30645d730f7cdE1F25a857E4D52D024D21ac7` · [DexScreener](https://dexscreener.com/bsc/0xA0B30645d730f7cdE1F25a857E4D52D024D21ac7)
- **Holders:** 226
- **Why (score 24.4):** controls_reserve+10 admin_setters+6 lifecycle+5 surface_breadth+1.8 recency+1.6

## #107 · GIVE · Ethereum · score 24.3

- **Chain:** Ethereum
- **Token address:** `0x95669A6589A81A6704bab1020722d0C405841885`  ·  [explorer](https://etherscan.io/address/0x95669A6589A81A6704bab1020722d0C405841885)
- **Liquidity:** $540,517 real quote-side  (headline $2,187,825)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 44 days (≈ deployed 2026-07-02)
- **Custom logic:** **fund ops**
  - key fns → fund: `mint`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** **FAM04** — shares a codebase with 2 other(s) via *identical_bytecode, identical_source*. A flaw here is a flaw in all 3 members.
  - siblings: ELMT `0x600D601D8b9EB5DE5Ac90fEfC68d0d08801bFd3f` (eth); SWITCH `0xb10cc888cB2CcE7036F4c7ECAd8a57Da16161338` (eth)
- **Deployer:** `0xfb312004c11535d9237c8f1878a9da1473eb4d45`
- **Market:** uniswap · quote GULD · pair `0x95475b9b1492cf109969ff25c2862ef38d1a9998c6288f8b9b7d1c99c6443c2e` · [DexScreener](https://dexscreener.com/ethereum/0x95475b9b1492cf109969ff25c2862ef38d1a9998c6288f8b9b7d1c99c6443c2e)
- **Safety flags:** mintable
- **Holders:** 295
- **Why (score 24.3):** fund_ops+12 surface_breadth+0.6 family_x3+4.2 liquidity+2.9 recency+1.6 mintable+3

## #108 · CZ · BNB Chain · score 23.0
*赤子*

- **Chain:** BNB Chain
- **Token address:** `0xF5Ed4e9fb91F19D2E7f9D485F8D812c679eedd50`  ·  [explorer](https://bscscan.com/address/0xF5Ed4e9fb91F19D2E7f9D485F8D812c679eedd50)
- **Liquidity:** $190,766 real quote-side  (headline $190,767)
- **Age / qualified by:** 13 days (≈ deployed 2026-08-02)
- **Custom logic:** impl/contract `ChiziToken` — **admin treasury pool signer**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0x46b7d5F6a5a465052648ad6ED8a51A0D713e3280` · [DexScreener](https://dexscreener.com/bsc/0x46b7d5F6a5a465052648ad6ED8a51A0D713e3280)
- **Holders:** 1470
- **Why (score 23.0):** controls_reserve+10 admin_setters+6 surface_breadth+1.2 liquidity+1.1 recency+4.7

## #109 · v€ · BNB Chain · score 22.9
*Vow Euro*

- **Chain:** BNB Chain
- **Token address:** `0x3745e245612f130B57589688060454A8ae43276C`  ·  [explorer](https://bscscan.com/address/0x3745e245612f130B57589688060454A8ae43276C)
- **Liquidity:** $177,397 real quote-side  (headline $177,408)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 27 days (≈ deployed 2026-07-20)
- **Custom logic:** impl/contract `VowEuroToken` — **fund ops, admin config gated**
  - key fns → fund: `burn`, `burnFrom`, `mint`, `setSkipTransferBurn`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote v$ · pair `0x8fC5E4cC4768449bc7fEb0Bf094BCdc3e4B16975` · [DexScreener](https://dexscreener.com/bsc/0x8fC5E4cC4768449bc7fEb0Bf094BCdc3e4B16975)
- **Safety flags:** mintable
- **Holders:** 99
- **Why (score 22.9):** fund_ops+12 surface_breadth+3.6 liquidity+1 recency+3.3 mintable+3

## #110 · O · BNB Chain · score 22.5
*o1.exchange*

- **Chain:** BNB Chain
- **Token address:** `0x500A02a20B0B0A3F3efCCFc0559543F5743bd1C4`  ·  [explorer](https://bscscan.com/address/0x500A02a20B0B0A3F3efCCFc0559543F5743bd1C4)
- **Liquidity:** $551,382 real quote-side  (headline $2,208,057)
- **Age / qualified by:** 60 days (≈ deployed 2026-06-17)
- **Custom logic:** impl/contract `MyOFT` — **admin treasury pool signer, bridge ops**
  - key fns → bridge: `lzReceive`, `lzReceiveAndRevert`, `lzReceiveSimulate`, `send`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0x1A9B68ca1dCaCB106c4b853e2d9c915f0cFe2e56` · [DexScreener](https://dexscreener.com/bsc/0x1A9B68ca1dCaCB106c4b853e2d9c915f0cFe2e56)
- **Holders:** 34654
- **Why (score 22.5):** bridge+8 admin_setters+6 surface_breadth+5.4 liquidity+3 recency+0.1

## #111 · BFC · BNB Chain · score 22.3
*八方来*

- **Chain:** BNB Chain
- **Token address:** `0x8881d7B8e8702494866Fc3d05B9aA3c52c79A62E`  ·  [explorer](https://bscscan.com/address/0x8881d7B8e8702494866Fc3d05B9aA3c52c79A62E)
- **Liquidity:** $133,526 real quote-side  (headline $133,526)
- **Age / qualified by:** 28 days (≈ deployed 2026-07-18)
- **Custom logic:** impl/contract `BFLToken` — **lifecycle ops**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDC · pair `0x0167aaD664FcF265dC26A8B9647200cb6CA650c2` · [DexScreener](https://dexscreener.com/bsc/0x0167aaD664FcF265dC26A8B9647200cb6CA650c2)
- **Safety flags:** mintable|blacklist_fn
- **Holders:** 1351
- **Why (score 22.3):** controls_reserve+10 lifecycle+5 surface_breadth+0.6 liquidity+0.5 recency+3.2 mintable+3

## #112 · GULD · Ethereum · score 21.7

- **Chain:** Ethereum
- **Token address:** `0x14D6C649292c5c9790c5196D1a9EA039307947a1`  ·  [explorer](https://etherscan.io/address/0x14D6C649292c5c9790c5196D1a9EA039307947a1)
- **Liquidity:** $1,544,984 real quote-side  (headline $1,983,225)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 45 days (≈ deployed 2026-07-01)
- **Custom logic:** **fund ops**
  - key fns → fund: `mint`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** **FAM05** — shares a codebase with 1 other(s) via *identical_bytecode, identical_source*. A flaw here is a flaw in all 2 members.
  - siblings: CDXR `0x40AAf75454036Bed56F3266cCf18f6b7befd6Aca` (eth)
- **Deployer:** `0xf7460d81fa18a6a5b213e8450e68c9ca2648993b`
- **Market:** uniswap · quote GROW · pair `0xf63fb2907e8f1067caad3dbf158bcd71b9937a054e601a7a4f8cda55e2417ce8` · [DexScreener](https://dexscreener.com/ethereum/0xf63fb2907e8f1067caad3dbf158bcd71b9937a054e601a7a4f8cda55e2417ce8)
- **Holders:** 2732
- **Why (score 21.7):** fund_ops+12 surface_breadth+0.6 family_x2+2.8 liquidity+4.8 recency+1.5

## #113 · 币安宇宙 · BNB Chain · score 21.6

- **Chain:** BNB Chain
- **Token address:** `0x0118508d60B355b83B96eAcc08C41b71E8314c6b`  ·  [explorer](https://bscscan.com/address/0x0118508d60B355b83B96eAcc08C41b71E8314c6b)
- **Liquidity:** $187,724 real quote-side  (headline $188,220)
- **Age / qualified by:** 1 days (≈ deployed 2026-08-14)
- **Custom logic:** impl/contract `SimpleP015` — **proxy upgrade**
  - key fns → upgrade: `setImplementation`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** custom_setImplementation → impl `0x6605ecdf70eb83951dd5b6fcb7adbbb3d240076b` ()
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote WBNB · pair `0x439BBbcb0536460850d95158439968B8FBCdbF20` · [DexScreener](https://dexscreener.com/bsc/0x439BBbcb0536460850d95158439968B8FBCdbF20)
- **Holders:** 234475
- **Why (score 21.6):** swappable_logic+14 surface_breadth+0.6 liquidity+1.1 recency+5.9

## #114 · EP · BNB Chain · score 21.1

- **Chain:** BNB Chain
- **Token address:** `0xC689A4aF8A68c61386766755BB8C8d0A54388888`  ·  [explorer](https://bscscan.com/address/0xC689A4aF8A68c61386766755BB8C8d0A54388888)
- **Liquidity:** $144,414 real quote-side
- **Age / qualified by:** 45 days (≈ deployed 2026-07-01)
- **Custom logic:** impl/contract `ExpansionProtocol` — **admin treasury pool signer, admin config gated**
- **Controls reserve/treasury/pool/vault:** yes
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote WBNB · pair `0xd3691EBbbFCa22b983cC236abc38dFac56DdC65a` · [DexScreener](https://dexscreener.com/bsc/0xd3691EBbbFCa22b983cC236abc38dFac56DdC65a)
- **Holders:** 1895
- **Why (score 21.1):** controls_reserve+10 admin_setters+6 surface_breadth+3 liquidity+0.6 recency+1.5

## #115 · NES · Ethereum · score 20.6
*Nesa*

- **Chain:** Ethereum
- **Token address:** `0x230f1E241C621d5af670Dad83ebCdd18971E2995`  ·  [explorer](https://etherscan.io/address/0x230f1E241C621d5af670Dad83ebCdd18971E2995)
- **Liquidity:** $1,614,689 real quote-side
- **Age / qualified by:** 48 days (≈ deployed 2026-06-29)
- **Custom logic:** impl/contract `HypERC20` — **admin treasury pool signer, lifecycle ops, admin config gated**
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0x98b3f0db84ca50a776f7cc340f429198c917f6f1` (verified)
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Deployer:** `0x1cfd6a81e98de59e3eeb3ae35c3cb13fcb586e1e`
- **Market:** uniswap · quote USDC · pair `0x19d044e9f31155f162928a04f261ea2af6f811130bbc850398cfaed377d7fdb9` · [DexScreener](https://dexscreener.com/ethereum/0x19d044e9f31155f162928a04f261ea2af6f811130bbc850398cfaed377d7fdb9)
- **Holders:** 28447
- **Why (score 20.6):** admin_setters+6 lifecycle+5 surface_breadth+3.6 liquidity+4.8 recency+1.2

## #116 · US · BNB Chain · score 20.5
*Talus Token*

- **Chain:** BNB Chain
- **Token address:** `0x51f1AFC16E154d1601e61EcA21d8Af4897f1e840`  ·  [explorer](https://bscscan.com/address/0x51f1AFC16E154d1601e61EcA21d8Af4897f1e840)
- **Liquidity:** $152,962 real quote-side  (headline $161,509)
- **Age / qualified by:** 56 days (≈ deployed 2026-06-21)
- **Custom logic:** impl/contract `BridgeToken` — **fund ops, lifecycle ops, admin config gated**
  - key fns → fund: `burn`, `mint`
- **Controls reserve/treasury/pool/vault:** no
- **Proxy / swappable logic:** eip1967 → impl `0x7f8c5e730121657e17e452c5a1ba3fa1ef96f22a` (verified)
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0xC84c8a7A25cEb962403775FA5a8C38Fbce0D4162` · [DexScreener](https://dexscreener.com/bsc/0xC84c8a7A25cEb962403775FA5a8C38Fbce0D4162)
- **Holders:** 234
- **Why (score 20.5):** fund_ops+12 lifecycle+5 surface_breadth+2.4 liquidity+0.7 recency+0.4

## #117 · RALLY · Ethereum · score 20.5

- **Chain:** Ethereum
- **Token address:** `0x19640000000ba88d36206BeB10D0e86011C8d08c`  ·  [explorer](https://etherscan.io/address/0x19640000000ba88d36206BeB10D0e86011C8d08c)
- **Liquidity:** $705,614 real quote-side  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 45 days (≈ deployed 2026-07-01)
- **Custom logic:** **fund ops**
  - key fns → fund: `mint`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Deployer:** `0xa6b171f4448fd6ea0763a578b30f771dc114495b`
- **Market:** uniswap · quote GULD · pair `0x12a9c409e2f0868b3f5bf76cffcc0c5128a31c491188bd6dd35b3c232bb62a14` · [DexScreener](https://dexscreener.com/ethereum/0x12a9c409e2f0868b3f5bf76cffcc0c5128a31c491188bd6dd35b3c232bb62a14)
- **Safety flags:** mintable
- **Holders:** 7059
- **Why (score 20.5):** fund_ops+12 surface_breadth+0.6 liquidity+3.4 recency+1.5 mintable+3

## #118 · BBD · BNB Chain · score 20.2
*BigBull Decentralized*

- **Chain:** BNB Chain
- **Token address:** `0x1b50119Bad9eFA60686ec1a418409BD391148f4C`  ·  [explorer](https://bscscan.com/address/0x1b50119Bad9eFA60686ec1a418409BD391148f4C)
- **Liquidity:** $524,204 real quote-side  (headline $524,933)
- **Age / qualified by:** 13 days (≈ deployed 2026-08-02)
- **Custom logic:** impl/contract `BigBull` — **fund ops**
  - key fns → fund: `mint`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0x24Eca0867dC02BAcA23bC5FEa9f0B746C6776EEc` · [DexScreener](https://dexscreener.com/bsc/0x24Eca0867dC02BAcA23bC5FEa9f0B746C6776EEc)
- **Holders:** 693
- **Why (score 20.2):** fund_ops+12 surface_breadth+0.6 liquidity+2.9 recency+4.7

## #119 · SPX · BNB Chain · score 20.0
*ShopinX Token*

- **Chain:** BNB Chain
- **Token address:** `0xCa56094722450016F280C4Fd6a333E5c36903827`  ·  [explorer](https://bscscan.com/address/0xCa56094722450016F280C4Fd6a333E5c36903827)
- **Liquidity:** $239,046 real quote-side  (headline $263,717)
- **Age / qualified by:** 19 days (≈ deployed 2026-07-28)
- **Custom logic:** impl/contract `ShopinXToken` — **fund ops, admin config gated**
  - key fns → fund: `burn`, `burnFrom`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0xe2561a789E8d94f3f9B620AaEcc627e1E205FE8B` · [DexScreener](https://dexscreener.com/bsc/0xe2561a789E8d94f3f9B620AaEcc627e1E205FE8B)
- **Safety flags:** blacklist_fn
- **Holders:** 2215
- **Why (score 20.0):** fund_ops+12 surface_breadth+2.4 liquidity+1.5 recency+4.1

## #120 · 关山月 · BNB Chain · score 18.9

- **Chain:** BNB Chain
- **Token address:** `0xdeA5a7a216c867Df782779f4ab0E3b2aB868f2E3`  ·  [explorer](https://bscscan.com/address/0xdeA5a7a216c867Df782779f4ab0E3b2aB868f2E3)
- **Liquidity:** $169,784 real quote-side  (headline $169,785)
- **Age / qualified by:** 8 days (≈ deployed 2026-08-08)
- **Custom logic:** impl/contract `GSY` — **admin treasury pool signer, lifecycle ops**
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote USDT · pair `0xCF7e25D3B5890947f2c7fDed0D101aB0b9175AfE` · [DexScreener](https://dexscreener.com/bsc/0xCF7e25D3B5890947f2c7fDed0D101aB0b9175AfE)
- **Holders:** 12612
- **Why (score 18.9):** admin_setters+6 lifecycle+5 surface_breadth+1.8 liquidity+0.9 recency+5.2

## #121 · rETH · Ethereum · score 18.9
*Rocket Pool ETH*

- **Chain:** Ethereum
- **Token address:** `0xae78736Cd615f374D3085123A210448E74Fc6393`  ·  [explorer](https://etherscan.io/address/0xae78736Cd615f374D3085123A210448E74Fc6393)
- **Liquidity:** $106,892 real quote-side  (headline $147,515)  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 46 days (≈ deployed 2026-06-30)
- **Custom logic:** impl/contract `RocketTokenRETH` — **fund ops**
  - key fns → fund: `burn`, `depositExcess`, `depositExcessCollateral`, `mint`
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Deployer:** `0x0ccf14983364a7735d369879603930afe10df21e`
- **Market:** uniswap · quote ETH · pair `0xee74bb87de06533905dc4a7266db239eccca3a3cbffe752bfe850785f8af78a2` · [DexScreener](https://dexscreener.com/ethereum/0xee74bb87de06533905dc4a7266db239eccca3a3cbffe752bfe850785f8af78a2)
- **Safety flags:** mintable
- **Holders:** 21665
- **Why (score 18.9):** fund_ops+12 surface_breadth+2.4 liquidity+0.1 recency+1.4 mintable+3

## #122 · CZ · BNB Chain · score 12.2
*The Final Form Bull*

- **Chain:** BNB Chain
- **Token address:** `0x7A848a5A8169aa6a2f603D056A749f924F504444`  ·  [explorer](https://bscscan.com/address/0x7A848a5A8169aa6a2f603D056A749f924F504444)
- **Liquidity:** $341,175 real quote-side  (headline $341,201)
- **Age / qualified by:** 41 days (≈ deployed 2026-07-05)
- **Custom logic:** **lifecycle ops, admin config gated**
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote WBNB · pair `0xd55Fa2c5E63eCAC3A158ca3fED4c8C2185ED45b2` · [DexScreener](https://dexscreener.com/bsc/0xd55Fa2c5E63eCAC3A158ca3fED4c8C2185ED45b2)
- **Safety flags:** pausable
- **Holders:** 66611
- **Why (score 12.2):** lifecycle+5 surface_breadth+1.2 liquidity+2.1 recency+1.9 pausable+2

## #123 · GPU · BNB Chain · score 11.0  ⚠️ **ALREADY EXPLOITED**

- **Chain:** BNB Chain
- **Token address:** `0x9DbeF6496134C151b9F9855cc5a1Ee77f0324444`  ·  [explorer](https://bscscan.com/address/0x9DbeF6496134C151b9F9855cc5a1Ee77f0324444)
- **Liquidity:** $103,201 real quote-side  — ⚠ *thin_quote_circular_risk*
- **Age / qualified by:** 13 days (≈ deployed 2026-08-02)
- **Custom logic:** **lifecycle ops, admin config gated**
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote NVDAB · pair `0x29271eD4B6B8FF41c326C81ca040fd110A4A047e` · [DexScreener](https://dexscreener.com/bsc/0x29271eD4B6B8FF41c326C81ca040fd110A4A047e)
- **Holders:** 10826
- **Exploit status:** ticker collision - UNRESOLVED
- **Why (score 11.0):** lifecycle+5 surface_breadth+1.2 liquidity+0.1 recency+4.7

## #124 · GOGOGO · BNB Chain · score 10.9

- **Chain:** BNB Chain
- **Token address:** `0x27645951262895AC9f4F18Cde02154aA4fbb86C0`  ·  [explorer](https://bscscan.com/address/0x27645951262895AC9f4F18Cde02154aA4fbb86C0)
- **Liquidity:** $296,616 real quote-side  (headline $296,618)
- **Age / qualified by:** 42 days (≈ deployed 2026-07-04)
- **Custom logic:** impl/contract `GoogolV2` — **admin treasury pool signer, admin config gated**
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** uniswap · quote USDT · pair `0x3b75172a3d636b763980B2E950268dc6F59c0b72` · [DexScreener](https://dexscreener.com/bsc/0x3b75172a3d636b763980B2E950268dc6F59c0b72)
- **Holders:** 2
- **Why (score 10.9):** admin_setters+6 surface_breadth+1.2 liquidity+1.9 recency+1.8

## #125 · TCC · BNB Chain · score 10.8
*TCryptochicks*

- **Chain:** BNB Chain
- **Token address:** `0xa4390B901a63641c92327E5793b45FCB46954444`  ·  [explorer](https://bscscan.com/address/0xa4390B901a63641c92327E5793b45FCB46954444)
- **Liquidity:** $137,850 real quote-side
- **Age / qualified by:** 40 days (≈ deployed 2026-07-07)
- **Custom logic:** **lifecycle ops, admin config gated**
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote WBNB · pair `0xC04e7fac7ea87ea9a0D31B6BCD7CA9B44CE4F803` · [DexScreener](https://dexscreener.com/bsc/0xC04e7fac7ea87ea9a0D31B6BCD7CA9B44CE4F803)
- **Safety flags:** pausable
- **Holders:** 61280
- **Why (score 10.8):** lifecycle+5 surface_breadth+1.2 liquidity+0.6 recency+2 pausable+2

## #126 · 9 · BNB Chain · score 10.5
*714*

- **Chain:** BNB Chain
- **Token address:** `0x990C71fDFA761bCF500AC8753f775FF7Fb1b4444`  ·  [explorer](https://bscscan.com/address/0x990C71fDFA761bCF500AC8753f775FF7Fb1b4444)
- **Liquidity:** $115,294 real quote-side  (headline $115,306)
- **Age / qualified by:** 39 days (≈ deployed 2026-07-07)
- **Custom logic:** **lifecycle ops, admin config gated**
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote WBNB · pair `0xFfc1c1Db5aef5C1b36d835a5c5159422d3213066` · [DexScreener](https://dexscreener.com/bsc/0xFfc1c1Db5aef5C1b36d835a5c5159422d3213066)
- **Safety flags:** pausable
- **Holders:** 7013
- **Why (score 10.5):** lifecycle+5 surface_breadth+1.2 liquidity+0.2 recency+2.1 pausable+2

## #127 · bibi · BNB Chain · score 8.5
*Binance bibi*

- **Chain:** BNB Chain
- **Token address:** `0x0b6d8934fC8838B1027b510364A2087317bD4444`  ·  [explorer](https://bscscan.com/address/0x0b6d8934fC8838B1027b510364A2087317bD4444)
- **Liquidity:** $103,154 real quote-side
- **Age / qualified by:** 38 days (≈ deployed 2026-07-08)
- **Custom logic:** **lifecycle ops, admin config gated**
- **Controls reserve/treasury/pool/vault:** no
- **Shared codebase:** No exact-clone family or known template lineage detected.
- **Market:** pancakeswap · quote WBNB · pair `0x2f19F30b8Be1A00E6a5903953F17244FBFcB0309` · [DexScreener](https://dexscreener.com/bsc/0x2f19F30b8Be1A00E6a5903953F17244FBFcB0309)
- **Holders:** 55058
- **Why (score 8.5):** lifecycle+5 surface_breadth+1.2 liquidity+0.1 recency+2.2

---

## Appendix — excluded (NOT candidates)
Inflated / circular liquidity (headline USD is not real money):

- **TAO** (eth) `0x819Cef100B177529035D035434CbAc49Fa9660cE` — headline $2,148,113,384, real quote-side $0 [MintBurnTeamToken]
- **HBAR** (eth) `0xEA7b2FC6Df1294732B8cf1F95c27b05e6e990E9b` — headline $1,449,620,085, real quote-side $0 [MintBurnTeamToken]
- **TRUU** (eth) `0xeE41ED87afAb2682F5688714499EbF4fa5c6fF19` — headline $3,096,541, real quote-side $0 [Truth]
- **CHL** (eth) `0x0F3ae93C6813cc85C9797b683ff1Db93Ade20F7D` — headline $3,096,330, real quote-side $0 [ChonceIIoon]
- **WIN** (eth) `0xb10CB07CA2CDac77FbB5707f6690301f9d036F45` — headline $2,161,020, real quote-side $18,058 [Token]
- **vAPI** (base) `0xe9f78bCAaA75673f270FdC3FfE4deF7E7Fc6c502` — headline $281,928, real quote-side $1 [TokenERC20]
- **BABAB** (bsc) `0x4eF9d3062c7F6ebA4AAE4990c5036598C6eff4ec` — headline $139,424, real quote-side $35,636 [BeaconProxy]
- **xtoken** (base) `0xe0c48Bfa530e3993FFD1a9202E4022327643E15F` — headline $113,724, real quote-side $3,577 [XTokenProxy]