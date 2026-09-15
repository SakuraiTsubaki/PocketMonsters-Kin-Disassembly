# Generation III Sprite Target Manifests

This directory records derived Generation III battle-sprite assets created from the preserved Generation II native/source layer.

See `docs/SPRITE_TARGET_GEN3.md` for the normative target specification.

## Required identity fields

Each per-species manifest should identify:

- National Pokédex/species ID
- species slug/name
- source generation and game
- native source manifest batch
- native source asset paths and SHA-256 values
- target status and verification level

## Front/back presentation fields

Record separately for front and back:

- `canvas`: always `[64, 64]` for completed target battle sprites
- `bbox`: occupied pixel bounds in `[x, y, width, height]` form
- `presentation_size`: Generation III-style logical display size
- `y_offset`
- `reference`: Generation III comparison source, if used
- `adaptation_method`
- `manual_pixel_edits`

`presentation_size` is not the physical PNG size.

## Output hashes

Record SHA-256 for all generated files, including PNG, uncompressed 4bpp, compressed 4bpp, palette source, binary palette, and compressed binary palette when present.

## Status vocabulary

Recommended target states:

- `planned`
- `source-audited`
- `pixel-adapted`
- `encoded`
- `validated`

Do not mark a target `validated` until visual, format, palette, compression round-trip, and hash checks all pass.
