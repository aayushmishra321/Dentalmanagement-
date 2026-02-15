@echo off
echo ==========================================
echo GitHub Repository Cleanup Script
echo ==========================================
echo.

REM Remove .env from git if committed
echo Removing .env from git tracking...
git rm --cached .env 2>nul || echo   .env not in git (good!)

REM Remove database from git if committed
echo Removing db.sqlite3 from git tracking...
git rm --cached db.sqlite3 2>nul || echo   db.sqlite3 not in git (good!)

REM Remove log files from git if committed
echo Removing log files from git tracking...
git rm --cached logs\*.log 2>nul || echo   No log files in git (good!)

REM Remove staticfiles from git if committed
echo Removing staticfiles\ from git tracking...
git rm -r --cached staticfiles\ 2>nul || echo   staticfiles\ not in git (good!)

REM Remove media files from git (keep .gitkeep)
echo Removing media files from git tracking...
git rm -r --cached media\ 2>nul || echo   media\ not in git
git add media\.gitkeep 2>nul || echo   media\.gitkeep added

REM Add logs/.gitkeep
git add logs\.gitkeep 2>nul || echo   logs\.gitkeep added

REM Clean local files
echo.
echo Cleaning local files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
echo   Python cache cleaned

REM Show status
echo.
echo ==========================================
echo Git Status:
echo ==========================================
git status

echo.
echo ==========================================
echo Cleanup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Review the git status above
echo 2. Run: git add .
echo 3. Run: git commit -m "Clean repository for deployment"
echo 4. Run: git push origin main
echo.
pause
