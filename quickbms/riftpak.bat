C:
cd\Downloads\Rift Files\
:again
if "%~1" == "" goto done
quickbms.exe -d riftpak.bms %1 "PAK"
shift
goto again
:done
pause
