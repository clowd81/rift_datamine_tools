for %%a in (*.wav) do ( ww2ogg --pcb packed_codebooks.bin "%%a" )
for %%a in (*.ogg) do revorb "%%a"