@echo off
cd /d "%~dp0"
echo Running data import...
python import_old_data.py > import_log.txt 2>&1
echo.
echo Done! Check import_log.txt for results.
type import_log.txt
pause
