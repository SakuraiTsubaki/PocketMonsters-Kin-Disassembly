# Bank 00 — map_objects

`map_objects` is a 0x310-byte ROM0 module in every tracked Gold release. The logic is shared across Japanese, Korean, English, German, French, Italian, and Spanish builds; release binaries differ because referenced RAM/code/data addresses are relocated.

## Verified ROM ranges

| release | start | end exclusive | size | SHA-1 |
|---|---:|---:|---:|---|
| JP Rev 0 | `0x1649` | `0x1959` | 784 | `c57eeb51d98337b5b94de67f9d734bfe8fc1569e` |
| JP Rev A | `0x1649` | `0x1959` | 784 | `c57eeb51d98337b5b94de67f9d734bfe8fc1569e` |
| KR | `0x16EF` | `0x19FF` | 784 | `c57f490728c72a8cb55a0c8fc15a16461f5b0b17` |
| EN | `0x169C` | `0x19AC` | 784 | `445d2f45cf83e2271217946947d2010adcb72cfc` |
| DE | `0x16C0` | `0x19D0` | 784 | `86f1d7580d67bd53bf66d29631824739b8d22468` |
| FR | `0x16A5` | `0x19B5` | 784 | `d9d0c8da6c43febd8acd29e446cd8d35b93c6766` |
| IT | `0x16BA` | `0x19CA` | 784 | `073de31b763a6c9977866bf19d3d5b3542e0fcb0` |
| ES | `0x16B9` | `0x19C9` | 784 | `d212ccb706d160e5ef7317af4b6669661f4b2039` |

Japanese Rev 0 and Rev A are byte-identical for this complete module.

## Semantic coverage

`src/home/map_objects.asm` reconstructs the full module, including:

- sprite palette and virtual-tile lookup
- sprite-facing capability lookup
- collision/tile permission helpers
- grass/water/tree/counter/pit/ice/whirlpool/waterfall checks
- map-object lookup and visibility/time gating
- object creation/deletion/follower cleanup
- scripted movement pointer setup
- object-struct allocation
- sprite movement/facing data lookup and copy
- movement-script byte fetch
- sprite-update state controls
- sprite update dispatch
- object-struct lookup and direction helpers

The independently maintained public EN, JP-family, and KR disassemblies expose the same semantic routine set; those sources are used only to cross-check symbol names and control-flow interpretation. The uploaded retail ROMs are the byte-level authority.

## Verification

`tests/test_bank00_map_objects.py` locks:

- exact range and SHA-1 for all 8 releases
- invariant 0x310-byte size
- Japanese Rev 0 / Rev A identity
- invariant entry and tail instruction structures

Full `byte_perfect_all_releases` remains open until the repository has a complete RGBDS layout/constants/macros environment and can assemble the module in-place for every target ROM.
