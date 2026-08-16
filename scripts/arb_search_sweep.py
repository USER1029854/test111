"""Phase 1b: independent discovery net using DEXScreener's own search endpoint.

Runs against a different host than the GeckoTerminal sweep, so it costs nothing
against that budget. Search results omit pairCreatedAt/liquidity provenance
guarantees, so this stage only harvests Arbitrum pair ADDRESSES; phase 2
re-reads each one authoritatively.

Word list is tuned to Arbitrum's actual ecosystem shape (GMX/perps-adjacent,
Camelot/points-farming launchpad culture, restaking, RWA, bridged assets)
rather than reusing the BSC meme-heavy list verbatim.
"""
import requests, json, time, string, itertools

H = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
OUT = "/home/user/test111/data/arb_ds_search_pools.json"
LOG = "/home/user/test111/data/arb_search_log.txt"

WORDS = """ai defi swap dao protocol finance chain node arb arbitrum perp perps perpetual
stake restake liquid vault lend borrow yield farm points airdrop claim redeem
bridge oracle index rwa nft game gamefi metaverse depin social pay card bank credit
fund trade quant alpha beta gamma sigma delta omega labs network capital treasury
reserve market maker pool router hub core prime edge nexus apex vertex matrix
quantum neural synth forge anvil citadel fortress bastion summit peak zenith horizon
orbit cosmos nova stellar solar lunar terra aqua flux pulse wave surge boost drift
shift pivot axis vector scalar tensor graph mesh grid link chain token coin cash
gmx camelot gains vela vertex hmx umami dopex jones rodeo pendle radiant dolomite
plutus magic sperp lyra premia buffer aark mux level cap gains kwenta grail spa
gns pear tap fee escrow governance ve lock boost multiplier layerzero stargate
across hop synapse celer wormhole axelar orbiter connext rollup optimistic based
launchpad presale ido fair mint genesis odyssey season quest campaign incentive
zk zksync scroll linea base blast mode fraxtal degen novel fresh new gem hidden
"""
terms = []
terms += ["".join(c) for c in itertools.product(string.ascii_lowercase, repeat=2)]
terms += list(dict.fromkeys(WORDS.split()))
terms += [c + d for c in string.ascii_lowercase for d in "0123456789"][:120]

pools, calls, errs = {}, 0, []
def log(m):
    print(m, flush=True)
    open(LOG, "a").write(m + "\n")

log(f"=== DS search sweep (arbitrum): {len(terms)} terms ===")
t0 = time.time()
for i, q in enumerate(terms):
    for attempt in range(3):
        try:
            calls += 1
            r = requests.get("https://api.dexscreener.com/latest/dex/search",
                             params={"q": q}, timeout=30, headers=H)
            if r.status_code == 429:
                time.sleep(5 * (attempt + 1)); continue
            if r.status_code != 200:
                break
            for p in (r.json().get("pairs") or []):
                if p.get("chainId") != "arbitrum":
                    continue
                a = (p.get("pairAddress") or "").lower()
                if a and a not in pools:
                    pools[a] = {
                        "pool_address": p["pairAddress"],
                        "gt_name": f'{p["baseToken"].get("symbol")}/{p["quoteToken"].get("symbol")}',
                        "gt_created": None,          # search omits it; phase 2 resolves
                        "gt_reserve_usd": (p.get("liquidity") or {}).get("usd"),
                        "gt_fdv": p.get("fdv"),
                        "base_token": p["baseToken"]["address"],
                        "quote_token": p["quoteToken"]["address"],
                        "dex": p.get("dexId"),
                        "srcs": ["ds_search"],
                    }
            break
        except Exception as e:
            errs.append(f"{q}:{type(e).__name__}"); time.sleep(1.5)
    time.sleep(0.25)
    if i % 150 == 0:
        log(f"  term {i}/{len(terms)} -> {len(pools)} arbitrum pairs ({calls} calls)")

log(f"=== DS search done: {len(pools)} arbitrum pairs, {calls} calls, {len(errs)} errs, {time.time()-t0:.0f}s ===")
json.dump({"pools": list(pools.values()), "errors": errs[:100], "calls": calls}, open(OUT, "w"), indent=1)
log("wrote " + OUT)
