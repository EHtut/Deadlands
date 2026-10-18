# Deadlands

A straight modpack — no custom scripting. Zombie apocalypse in a dead city, with
parasites, guns, Create, and a light layer of Ars Nouveau magic.

Minecraft **1.21.1**, NeoForge **21.1.262**, packwiz. Dedicated server + friends.

## The brief (Ethan, 2026-10-17)

- Keep the performance and visual mods from Arkhdottir; everything else is new.
- Zombie apocalypse with ruined cities — **the whole world is a city** (The Lost Cities, `onlycities`).
- Many types of zombies, **and parasites**.
- **Guns are a big focus.** Create and Ars magic are the other two pillars.
- Fantasy kept light: *"mostly the magic from ars but nothing overly fantastical."*

## Where things are

| | |
|---|---|
| `tools/modlist.json` | **the source of truth** — every mod, grouped, with why it is in |
| `pack/` | the packwiz pack, **generated** — never hand-edit |
| `C:\MCServer\zombie-instance` | the dedicated server. rcon on 25576, localhost; `tools/rcon.py --instance C:/MCServer/zombie-instance "list"` |

## Building

```bash
python tools/resolve.py resolve tools/modlist.json   # pin every entry against Modrinth
python tools/resolve.py deps                         # libraries Modrinth says are missing
python tools/fetch_jars.py                           # download + sha512-verify every jar
python tools/check_deps.py tools/.cache/jars --side=server   # what the LOADER will say
python tools/check_deps.py tools/.cache/jars --side=client
python tools/gen_pack.py                             # write pack/
python tools/fetch_jars.py --server C:/MCServer/zombie-instance/mods
```

⚠️ **Modrinth's dependency data is incomplete — the jars are the authority.** On the
first build `deps` reported a closed graph and `check_deps` then found four boot-blockers:
SmartBrainLib and Voidless Framework undeclared, and GeckoLib and TaCZ pinned too old.

## Decisions that would otherwise be re-litigated

**One of each overlapping system.** Hordes *and* infection: **The Hordes**. Block-breaking
zombies: **Enhanced AI** only — so no Enhanced Hordes, Zombie Break & Build or Zombie
Proof Doors. **Gamingbarn's Zombies is out**: it replaces every vanilla monster, and the
zombie rosters already cover that ground.

**Two gun engines, by request:** TaCZ and Vic's Point Blank. Two separate ammo economies.
⚠️ **TaCZ on 1.21.1 is an UNOFFICIAL port.** It needs `tacz-pack-upgrader`, and
`tacza` (TaCZ: Accel) to stop it eating CPU — Accel names the port's exact version
(`>=1.1.8-hotfix-r7`), so it is built for it. Superb Warfare and BlockFront are **out**:
each would be a third gun engine.

**Scape and Run: Parasites has no 1.21.1 NeoForge build.** Fungal Infection: Spore plus
Spore: SRP is the route to that feel.

**Lost Cities on 1.21 is NOT `level-type=lostcities`** — that is the 1.12 method. It is
`[profiles] selectedProfile` in `config/lostcities-server.toml` (a copy lives in
`server-config/`), set **before** the world first generates. Verified 2026-10-17: 48 of 55
fully generated spawn chunks contain city blocks.
⚠️ **Measure per FULLY GENERATED chunk.** Counting block palettes across region files
reported "natural terrain" twice — the ring of half-generated chunks around spawn is bare
terrain and swamps the count. That false negative led to an unneeded
`dimensionsWithProfiles` edit, since reverted. Do not re-add it.

**One third-person camera.** Third Person Shooting needs Shoulder Surfing Reloaded, so
Better Third Person was dropped rather than run alongside it.

**Waystones not carried.** Free teleport undercuts crossing a dead city.

## Not done yet

- **NeoForge 21.1.262, not 247:** Elite X Quality Guns requires `>=21.1.259`.
- **ZoNiEx removed:** every version is a Forge 1.20.1 jar mislabelled as 1.21.1 NeoForge.
- **`check_deps.py` now catches both of those** — it passed them before, and the loader did not.
- **Publishing** — no GitHub remote yet, so no client import link.
- **No mod has been seen in game.** Everything above is resolution and jar metadata.
