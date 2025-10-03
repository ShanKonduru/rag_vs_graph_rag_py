#!/bin/bash

# RAG vs Graph RAG vs Knowledge Graph System Setup Script

echo "Setting up RAG vs Graph RAG vs Knowledge Graph System..."

# Start services
echo "Starting Neo4j and Ollama services..."
cd docker
docker-compose up -d

echo "Waiting for services to start..."
sleep 30

# Check Neo4j
echo "Checking Neo4j connection..."
until docker exec rag_neo4j cypher-shell -u neo4j -p password "RETURN 1" > /dev/null 2>&1; do
    echo "Waiting for Neo4j..."
    sleep 5
done
echo "Neo4j is ready!"

# Check Ollama
echo "Checking Ollama connection..."
until curl -f http://localhost:11434/api/tags > /dev/null 2>&1; do
    echo "Waiting for Ollama..."
    sleep 5
done
echo "Ollama is ready!"

# Pull Ollama models
echo "Pulling Ollama models..."
docker exec rag_ollama ollama pull llama2
docker exec rag_ollama ollama pull mistral

echo "Setup complete!"
echo ""
echo "Services:"
echo "- Neo4j Browser: http://localhost:7474 (username: neo4j, password: password)"
echo "- Ollama API: http://localhost:11434"
echo ""
echo "Available models:"
docker exec rag_ollama ollama list