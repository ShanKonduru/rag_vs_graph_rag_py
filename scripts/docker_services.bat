@echo off
REM =====================================================
REM  RAG System - Docker Services Management (Windows)
REM =====================================================
REM  Start, stop, and manage Docker services
REM  Usage: docker_services.bat [start|stop|status|logs]
REM =====================================================

if "%1"=="help" (
    echo Available commands:
    echo   docker_services.bat start    - Start all services ^(Neo4j + Ollama^)
    echo   docker_services.bat stop     - Stop all services
    echo   docker_services.bat status   - Check service status
    echo   docker_services.bat logs     - View service logs
    echo   docker_services.bat restart  - Restart all services
    echo   docker_services.bat neo4j    - Start Neo4j only
    echo   docker_services.bat ollama   - Start Ollama only
    goto :eof
)

REM Check if Docker is available
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker not found. Please install Docker Desktop first.
    echo Download from: https://docker.com/products/docker-desktop
    pause
    exit /b 1
)

cd /d "%~dp0"
if not exist docker\docker-compose.yml (
    echo ERROR: docker-compose.yml not found in docker directory
    exit /b 1
)

cd docker

if "%1"=="start" (
    echo Starting all Docker services...
    docker-compose up -d
    echo.
    echo Services starting up. Check status with:
    echo   docker_services.bat status
    goto :eof
)

if "%1"=="stop" (
    echo Stopping all Docker services...
    docker-compose down
    echo Services stopped.
    goto :eof
)

if "%1"=="status" (
    echo Checking service status...
    docker-compose ps
    echo.
    echo Service URLs:
    echo   Neo4j Browser: http://localhost:7474
    echo   Ollama API:     http://localhost:11434
    goto :eof
)

if "%1"=="logs" (
    echo Showing service logs...
    docker-compose logs -f
    goto :eof
)

if "%1"=="restart" (
    echo Restarting all services...
    docker-compose restart
    echo Services restarted.
    goto :eof
)

if "%1"=="neo4j" (
    echo Starting Neo4j service only...
    docker-compose up -d neo4j
    echo Neo4j started. Access at: http://localhost:7474
    goto :eof
)

if "%1"=="ollama" (
    echo Starting Ollama service only...
    docker-compose up -d ollama
    echo Ollama started. API at: http://localhost:11434
    goto :eof
)

echo Usage: docker_services.bat [command]
echo.
echo Available commands:
echo   start     - Start all services
echo   stop      - Stop all services
echo   status    - Check service status
echo   logs      - View service logs
echo   restart   - Restart services
echo.
echo Run 'docker_services.bat help' for more options