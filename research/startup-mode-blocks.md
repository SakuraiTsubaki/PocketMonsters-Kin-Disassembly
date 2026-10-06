# Japanese CGB mode startup branches

The startup CGB check branches at `0x05C9`/ `0x05CC`. The non-CGB path
clears A and joins at `0x05CE`; the CGB path records mode, clears hardware
state, and waits for LY `0x91`. Both paths are preserved as separately
reassemblable RGBDS blocks bound to the Japanese candidate hash. The candidate
is not promoted to verified.
