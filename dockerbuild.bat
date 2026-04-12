@echo off

set /p VERSION="Enter version tag (e.g. beta, v1.1, latest): "

SET IMAGE_NAME=tmr2000/cs2-panel:%VERSION%

echo --- STARTING BUILD ---
docker build -t %IMAGE_NAME% .

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Build failed! Check your Dockerfile or code.
    pause
    exit /b %ERRORLEVEL%
)

echo --- PUSHING TO DOCKER HUB ---
docker login
docker push %IMAGE_NAME%

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Push failed! Are you logged in? (run 'docker login')
    pause
    exit /b %ERRORLEVEL%
)

echo --- DEPLOYMENT FINISHED SUCCESSFULLY ---
pause