# Pokémon sprite reconstruction

Sprite assets are extracted directly from the read-only Gold ROM baselines. Uploads are intentionally split into small batches.

For each sprite, the original LZ-compressed 2bpp stream is kept next to a human-viewable PNG preview. A single shared asset is stored only when the compressed bytes and decompressed 2bpp bytes are identical across all compared baselines. Per-ROM bank/address/file-offset provenance remains in the batch manifest so deduplication never loses source information.

PNG previews use a neutral four-level grayscale palette; they are inspection images, not claims about the in-game CGB palette.

Batch 0001 covers #001 Bulbasaur through #003 Venusaur and was checked against all eight Gold baselines: Japanese Rev 0, Japanese Rev A, Korean, English, German, French, Italian, and Spanish.
