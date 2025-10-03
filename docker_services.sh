#!/bin/bash
# =====================================================
#  RAG System - Docker Services Management (Unix/Linux)
# =====================================================
#  Start, stop, and manage Docker services
#  Usage: ./docker_services.sh [start|stop|status|logs]
# =====================================================

show_help() {
    echo "Available commands:"
    echo "  ./docker_services.sh start    - Start all services (Neo4j + Ollama)"
    echo "  ./docker_services.sh stop     - Stop all services"
    echo "  ./docker_services.sh status   - Check service status"
    echo "  ./docker_services.sh logs     - View service logs"
    echo "  ./docker_services.sh restart  - Restart all services"
    echo "  ./docker_services.sh neo4j    - Start Neo4j only"
    echo "  ./docker_services.sh ollama   - Start Ollama only"
}

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker not found. Please install Docker first."
    exit 1
fi

# Change to script directory
cd "$(dirname "$0")"

if [ ! -f "docker/docker-compose.yml" ]; then
    echo "ERROR: docker-compose.yml not found in docker directory"
    exit 1
fi

cd docker

case "$1" in
    "help")
        show_help
        ;;
    "start")
        echo "Starting all Docker services..."
        docker-compose up -d
        echo ""
        echo "Services starting up. Check status with:"
        echo "  ./docker_services.sh status"
        ;;
    "stop")
        echo "Stopping all Docker services..."
        docker-compose down
        echo "Services stopped."
        ;;
    "status")
        echo "Checking service status..."
        docker-compose ps
        echo ""
        echo "Service URLs:"
        echo "  Neo4j Browser: http://localhost:7474"
        echo "  Ollama API:     http://localhost:11434"
        ;;
    "logs")
        echo "Showing service logs..."
        docker-compose logs -f
        ;;
    "restart")
        echo "Restarting all services..."
        docker-compose restart
        echo "Services restarted."
        ;;
    "neo4j")
        echo "Starting Neo4j service only..."
        docker-compose up -d neo4j
        echo "Neo4j started. Access at: http://localhost:7474"
        ;;
    "ollama")
        echo "Starting Ollama service only..."
        docker-compose up -d ollama
        echo "Ollama started. API at: http://localhost:11434"
        ;;
    *)
        echo "Usage: ./docker_services.sh [command]"
        echo ""
        echo "Available commands:"
        echo "  start     - Start all services"
        echo "  stop      - Stop all services"
        echo "  status    - Check service status"
        echo "  logs      - View service logs"
        echo "  restart   - Restart services"
        echo ""
        echo "Run './docker_services.sh help' for more options"
        ;;
esac