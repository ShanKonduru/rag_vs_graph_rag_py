@echo off
REM RAG vs Graph RAG vs Knowledge Graph System Setup Script for Windows

echo Setting up RAG vs Graph RAG vs Knowledge Graph System...

REM Start services
echo Starting Neo4j and Ollama services...
cd docker
docker-compose up -d

echo Waiting for services to start...
timeout /t 30 /nobreak >nul

REM Check Neo4j
echo Checking Neo4j connection...
:check_neo4j
docker exec rag_neo4j cypher-shell -u neo4j -p password "RETURN 1" >nul 2>&1
if errorlevel 1 (
    echo Waiting for Neo4j...
    timeout /t 5 /nobreak >nul
    goto check_neo4j
)
echo Neo4j is ready!

REM Check Ollama
echo Checking Ollama connection...
:check_ollama
curl -f http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo Waiting for Ollama...
    timeout /t 5 /nobreak >nul
    goto check_ollama
)
echo Ollama is ready!

REM Pull Ollama models
echo Pulling Ollama models...
docker exec rag_ollama ollama pull llama2
docker exec rag_ollama ollama pull mistral

echo Setup complete!
echo.
echo Services:
echo - Neo4j Browser: http://localhost:7474 (username: neo4j, password: password)
echo - Ollama API: http://localhost:11434
echo.
echo Available models:
docker exec rag_ollama ollama list