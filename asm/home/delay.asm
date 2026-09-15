; Pocket Monsters Kin (Japan) — Bank 00 frame-delay helpers.
; Recovered from this repository's ROM-derived commit
; 2eef70f8a4c15959b2dce9e7773a508572a45a7e.

DelayFrame::
    ld a, 1
    ld [wVBlankOccurred], a

.halt
    halt
    nop
    ld a, [wVBlankOccurred]
    and a
    jr nz, .halt
    ret

DelayFrames::
    call DelayFrame
    dec c
    jr nz, DelayFrames
    ret
