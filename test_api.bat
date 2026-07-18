@echo off
setlocal enabledelayedexpansion

REM Change this if your server runs on a different port.
set BASE_URL=http://127.0.0.1:8000

REM Optional first argument overrides the keyword used in POST tests.
if "%~1"=="" (
    set KEYWORD=programming
) else (
    set KEYWORD=%~1
)

echo.
echo ========================================
echo FastAPI Joke Generator - API Test Script
echo Base URL: %BASE_URL%
echo Keyword:  %KEYWORD%
echo ========================================
echo.

call :print_section "Health Check"
curl.exe -s %BASE_URL%/health
echo.
echo.

call :print_section "Random Joke - GET /jokes/random/sync"
curl.exe -s %BASE_URL%/jokes/random/sync
echo.
echo.

call :print_section "Random Joke - GET /jokes/random/async"
curl.exe -s "%BASE_URL%/jokes/random/async?count=2"
echo.
echo.

call :print_section "Keyword Search - POST /jokes/keyword/sync"
curl.exe -s -X POST %BASE_URL%/jokes/keyword/sync ^
  -H "Content-Type: application/json" ^
  -d "{\"keyword\":\"%KEYWORD%\",\"count\":1}"
echo.
echo.

call :print_section "Keyword Search - POST /jokes/keyword/async"
curl.exe -s -X POST %BASE_URL%/jokes/keyword/async ^
  -H "Content-Type: application/json" ^
  -d "{\"keyword\":\"%KEYWORD%\",\"count\":1}"
echo.
echo.

echo Done.
exit /b 0

:print_section
echo ----------------------------------------
echo %~1
echo ----------------------------------------
exit /b 0
