@echo off

set /p VERSION="Enter version tag (e.g. beta, v1.1, latest): "

SET IMAGE_NAME=tmr2000/cs2-panel:%VERSION%

echo --- STARTING BUILD & PULLING FROM GIT ---

:: Using %DATE%_%TIME% as a cache buster forces Docker to fetch fresh code every build
docker build --build-arg CACHEBUST=%DATE%_%TIME% -t %IMAGE_NAME% .

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Build failed! Ensure Docker Desktop is open and your Git repository URL is correct.
    pause
    exit /b %ERRORLEVEL%
)

echo --- PUSHING TO DOCKER HUB ---
docker login
docker push %IMAGE_NAME%

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Push failed!
    pause
    exit /b %ERRORLEVEL%
)

echo --- DEPLOYMENT FINISHED SUCCESSFULLY ---
pause