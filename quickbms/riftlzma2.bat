E:
cd\RIFT\PTS\Assets
:again
if "%~1" == "" goto done
quickbms.exe riftlzma2.bms %1 "LZMA2"
shift
goto again
:done
pause