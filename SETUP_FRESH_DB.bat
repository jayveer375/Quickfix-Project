@echo off
echo ===================================
echo  QuickFix - Fresh Database Setup
echo ===================================
echo.

cd /d "%~dp0"

echo Deleting old corrupted database...
if exist "instance\database.db" (
    copy "instance\database.db" "instance\database_old_backup.db" >nul
    del "instance\database.db"
    echo Old DB backed up and removed.
) else (
    echo No existing database found.
)

echo.
echo Creating fresh database with new admin credentials...
python fresh_db.py

echo.
echo Done! Press any key to exit.
pause
