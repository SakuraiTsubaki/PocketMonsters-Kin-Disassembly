# Project Status

This file summarizes target coverage, reconstruction stage, and matching status. Detailed historical progress may also live in game-specific research files and the root README.

## Shared milestones

- [ ] Target inventory is authoritative
- [ ] Source/build toolchain is documented
- [ ] Major code/data regions are mapped
- [ ] Structured source replaces understood opaque/raw regions
- [ ] Graphics/text/audio/maps/scripts are reconstructed where applicable
- [ ] Build outputs are verified by bank/section/range or equivalent
- [ ] Supported targets reach defined exact-match criteria

Use the terminology from `VERIFICATION.md`: **Unverified**, **Observed**, **Reconstructed**, and **Matched**.

## Sprite work

Generation II native Pokémon battle graphics are preserved under `gfx/pokemon/` with extraction manifests under `manifests/sprites/`.

Generation III adaptation is a separate derived layer documented by `docs/SPRITE_TARGET_GEN3.md` and stored under `gfx/targets/gen3/pokemon/` when target files are produced.

Current Generation III target progress:

- [x] target format and separation from native source defined
- [x] target manifest format defined
- [x] validator added for 64×64 indexed PNG, palette limits, 4bpp size, GBA LZ77 round-trip, and SHA-256
- [x] Bulbasaur source audit and FireRed/LeafGreen presentation reference recorded
- [x] Ivysaur source audit and FireRed/LeafGreen presentation reference recorded
- [x] Venusaur source audit and FireRed/LeafGreen presentation reference recorded
- [ ] Bulbasaur pixel adaptation completed
- [ ] Bulbasaur 4bpp/palette/compression package validated
- [ ] first three-species target batch validated

Do not expand the target conversion across the full Pokédex until the first target species has passed the complete visual and binary validation gates.
