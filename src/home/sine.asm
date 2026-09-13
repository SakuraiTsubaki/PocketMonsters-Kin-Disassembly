Cosine:: ; unreferenced
; a = d * cos(a * pi/32)
	add %010000
	; fallthrough
Sine::
; a = d * sin(a * pi/32)
	ld e, a
	homecall _Sine
	ret
