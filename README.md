# Zombiepack *(working name)*

A straight modpack — no custom scripting. Zombie apocalypse in a dead city, with
parasites, guns, Create, and a light layer of Ars Nouveau magic.

Minecraft **1.21.1**, NeoForge **21.1.247**, packwiz. Dedicated server + friends.

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
| `C:\MCServer\zombie-instance` | the dedicated server |

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
`[profiles] selectedProfile` in `config/lostcities-server.toml`, and it must be set
**before** the world first generates.

**One third-person camera.** Third Person Shooting needs Shoulder Surfing Reloaded, so
Better Third Person was dropped rather than run alongside it.

**Waystones not carried.** Free teleport undercuts crossing a dead city.

## Not done yet

- 🖊️ **The pack name.** "Zombiepack" lives in `tools/gen_pack.py` `PACK_NAME` and nowhere else.
- **First boot** — needs the EULA accepted in `zombie-instance/eula.txt`.
- **Publishing** — no GitHub remote yet, so no client import link.
- **No mod has been seen in game.** Everything above is resolution and jar metadata.
