# Project Standards

This document defines shared organizational standards for the disassembly project. It complements `DISASSEMBLY_STANDARDS.md` by covering naming, assets, manifests, provenance, generated material, and repository boundaries.

## Naming

- Prefer stable, descriptive names over temporary labels when an identity is verified.
- Preserve original identifiers, addresses, banks, section names, table indices, and other source-facing identifiers where useful for reproducibility.
- Mark uncertain names or interpretations explicitly instead of presenting guesses as facts.
- Keep version-, region-, language-, and revision-specific material clearly scoped when bytes or behavior differ.

## Source and generated material

Prefer editable source representations and reproducible conversion steps over opaque derived files. Track generated files only when they are useful project artifacts, evidence, or human-reviewable assets with documented origin. Keep disposable build output, caches, and scratch dumps outside version control. Retail or rebuilt ROM images are never repository artifacts.

## Assets

Retain provenance for graphics, sprites, text, maps, audio, scripts, tables, and other recovered content. Human-viewable PNGs should accompany sprite/graphics reconstruction when practical. Verify byte identity or cryptographic hashes before deduplicating, and preserve target-specific provenance for shared files.

## Manifests

Use stable identifiers and record verified target/release, region, language, revision, source location, repository path, size, hashes, generation method, verification level, shared usage, and notes as applicable. Unknown fields remain `null`, `TBD`, or `unknown`.

See `../manifests/README.md` and `../manifests/example.asset-manifest.json`.

## Provenance and verification

Meaningful claims should identify the target and reproducible evidence. Use **Unverified**, **Observed**, **Reconstructed**, and **Matched** as defined in `VERIFICATION.md`.

## Repository structure and reviewability

Preserve the repository's verified architecture instead of forcing a layout copied from another generation. Add directories only for real project material. Prefer small, coherent commits and asset batches with related documentation/manifests updated together when practical.
