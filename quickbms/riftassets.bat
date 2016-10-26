E:
cd\RIFT\PTS\Assets
:again
if "%~1" == "" goto done
quickbms.exe riftassets.bms %1
shift
goto again
:done
pause