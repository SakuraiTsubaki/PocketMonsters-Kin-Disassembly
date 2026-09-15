# Generation III Sprite Target Standard

This document defines the **target** battle-sprite format for adapting Generation I and Generation II source sprites into Generation III-compatible assets.

The native Generation II graphics in `gfx/pokemon/` remain source/reference material. They are not the final target format.

## 1. Source versus target

Two layers must remain distinct:

- **Native/source layer** — reconstructed Generation II graphics, native dimensions, 2bpp data, original compression streams, source PNGs, pointers, hashes, region/revision coverage, and provenance.
- **Generation III target layer** — derived battle graphics intended to be directly usable by a Generation III-style engine and build pipeline.

Do not replace or overwrite native source assets when creating target assets.

## 2. Target directory

Generation III-derived assets belong under:

```text
gfx/targets/gen3/pokemon/<species>/
```

The existing path:

```text
gfx/pokemon/<species>/
```

remains the Generation II native/source layer.

## 3. Final battle-sprite canvas

Both front and back target PNGs use a **64×64 pixel canvas**.

This does **not** mean that every Pokémon must fill the full 64×64 area. Generation III presentation uses species-specific occupied sizes and vertical offsets inside the common canvas. The target manifest therefore records presentation metadata separately from the physical PNG canvas.

Required files:

```text
front.png
back.png
```

Required PNG properties:

- width: `64`
- height: `64`
- indexed/paletted image
- transparent palette entry at index `0`
- no more than `16` palette entries
- no semi-transparent sprite pixels

## 4. Presentation normalization

Generation I/II source graphics are references, not immutable final layouts.

The target sprite must preserve the source Pokémon's:

- silhouette
- pose identity
- face and eye placement
- characteristic markings
- representative colors
- overall visual identity

but may adjust:

- occupied pixel area
- internal placement on the 64×64 canvas
- outline cleanup
- local pixel clusters
- shading steps
- palette ramps

when required to produce a natural Generation III battle presentation.

Do not complete adaptation by only:

- nearest-neighbor enlargement
- automatic image scaling
- automatic 16-color quantization
- background removal
- padding the original native image into a 64×64 canvas

Minimal manual pixel correction is allowed when it serves Generation III adaptation rather than redesign.

## 5. Generation III presentation metadata

Generation III battle graphics use a fixed graphics resource together with species-specific presentation coordinates. For example, `pret/pokefirered` stores species-specific `.size` and `.y_offset` values in `gMonFrontPicCoords` and `gMonBackPicCoords` while the Pokémon graphics are included as compressed 4bpp resources.

Each target manifest must therefore record, independently for front and back:

- final canvas size (`64×64`)
- occupied/bounding-box size
- occupied/bounding-box coordinates
- target presentation size
- target `y_offset`
- Generation III reference game/data used for presentation comparison
- adaptation method
- whether manual pixel edits were performed

The presentation size is **not** the PNG file size. For example, FireRed/LeafGreen data contains species-specific logical sizes such as Bulbasaur front `40×40` with `y_offset = 16` and Bulbasaur back `48×32` with `y_offset = 16`, while the target graphics resource belongs to the common Generation III sprite pipeline.

## 6. Palette format

The final target uses the Generation III 4bpp palette model.

Requirements:

- palette index `0` is transparent
- maximum `16` entries
- normal and shiny palettes are tracked separately
- unused entries are deterministic rather than arbitrary
- palette decisions prioritize species identity and readable Generation III-style shading over mechanically preserving the original four-color Game Boy palette

Recommended source files:

```text
normal.pal
shiny.pal
```

Generated binary palette assets:

```text
normal.gbapal
shiny.gbapal
```

If the destination build expects compressed palettes, also generate:

```text
normal.gbapal.lz
shiny.gbapal.lz
```

## 7. 4bpp graphics output

A complete 64×64 4bpp tiled sprite contains 64 8×8 tiles. At 32 bytes per 4bpp tile, the uncompressed graphic payload is **2048 bytes** per front or back sprite.

Required generated assets:

```text
front.4bpp
back.4bpp
front.4bpp.lz
back.4bpp.lz
```

The `.4bpp.lz` convention matches the Generation III decompilation workflow used by projects such as `pret/pokefirered`, where Pokémon front and back graphics are included from paths such as `graphics/pokemon/<species>/front.4bpp.lz` and `back.4bpp.lz`.

## 8. Shiny handling

Normal and shiny appearances should normally share the same front/back pixel graphics and differ through palette data, matching the standard Generation III Pokémon graphics model.

If an exceptional source requires different pixel graphics, record that exception explicitly instead of silently duplicating data.

## 9. Per-species package

A completed target species should contain, where applicable:

```text
gfx/targets/gen3/pokemon/<species>/
├── front.png
├── back.png
├── front.4bpp
├── back.4bpp
├── front.4bpp.lz
├── back.4bpp.lz
├── normal.pal
├── shiny.pal
├── normal.gbapal
├── shiny.gbapal
├── normal.gbapal.lz
├── shiny.gbapal.lz
└── SHA256SUMS
```

The corresponding manifest belongs under `manifests/sprites/gen3/`.

## 10. Hashing and provenance

Every generated file must have a SHA-256 value recorded in either the per-species manifest or `SHA256SUMS`.

The manifest must retain links back to the native/source assets, including their hashes and original manifest batch where available. A derived asset without traceable source provenance is not considered complete.

## 11. Validation gates

A target sprite is complete only when all applicable checks pass:

1. native source is identified and preserved;
2. front and back PNGs are exactly 64×64;
3. PNGs use indexed color and index 0 transparency;
4. each PNG uses at most 16 palette entries;
5. presentation metadata is recorded;
6. uncompressed 4bpp output is exactly 2048 bytes per sprite;
7. compressed graphics can be decompressed back to the exact 4bpp payload;
8. palette binaries match their source palette definition;
9. SHA-256 values match all generated files;
10. normal/shiny palette handling is documented;
11. visual review confirms that the sprite is a Generation III adaptation rather than a mechanically padded or scaled Generation II image;
12. no ROM image is committed.

## 12. Batch policy

Generation III adaptations must be committed in small, reviewable batches. Do not mass-convert the full Pokédex before the first species in a batch has passed visual, binary, palette, compression, manifest, and hash validation.

The intended workflow is:

```text
native Gen II source
→ source analysis
→ Gen III presentation target
→ pixel adaptation
→ indexed 64×64 PNG
→ normal/shiny palette
→ 4bpp
→ Generation III compression
→ manifest + SHA-256
→ validation
```
