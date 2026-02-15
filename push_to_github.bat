@echo off
echo ==========================================
echo Push to GitHub Script
echo ==========================================
echo.
echo Repository: https://github.com/aayushmishra321/Dentalmanagement-.git
echo.

REM Check if git is initialized
if not exist .git (
    echo Initializing Git repository...
    git init
    echo.
)

REM Check if remote exists
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo Adding remote repository...
    git remote add origin https://github.com/aayushmishra321/Dentalmanagement-.git
    echo.
) else (
    echo Remote repository already exists
    echo.
)

REM Show current status
echo Current Git Status:
echo ==========================================
git status
echo.

REM Add all files
echo Adding all files...
git add .
echo.

REM Commit
echo Enter commit message (or press Enter for default):
set /p COMMIT_MSG="Commit message: "
if "%COMMIT_MSG%"=="" set COMMIT_MSG=Initial commit: Dental Management System v1.0.0

echo.
echo Committing with message: %COMMIT_MSG%
git commit -m "%COMMIT_MSG%"
echo.

REM Set main branch
echo Setting main branch...
git branch -M main
echo.

REM Push to GitHub
echo Pushing to GitHub...
echo ==========================================
git push -u origin main
echo.

if errorlevel 1 (
    echo.
    echo ==========================================
    echo Push failed! Common solutions:
    echo ==========================================
    echo 1. Check your internet connection
    echo 2. Verify GitHub credentials
    echo 3. Use Personal Access Token instead of password
    echo 4. Try: git pull origin main --rebase
    echo 5. Then run this script again
    echo.
) else (
    echo.
    echo ==========================================
    echo SUCCESS! Project pushed to GitHub
    echo ==========================================
    echo.
    echo Visit your repository:
    echo https://github.com/aayushmishra321/Dentalmanagement-
    echo.
    echo Next steps:
    echo 1. Verify files on GitHub
    echo 2. Add repository description
    echo 3. Deploy to Render (see DEPLOYMENT.md)
    echo.
)

pause
