#!/bin/bash
# scripts/deploy.sh

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_FILE="${PROJECT_ROOT}/.env.prod"
COMPOSE_FILE="${PROJECT_ROOT}/docker-compose.prod.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required files exist
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if [ ! -f "$ENV_FILE" ]; then
        log_error "Environment file not found: $ENV_FILE"
        exit 1
    fi
    
    if [ ! -f "$COMPOSE_FILE" ]; then
        log_error "Docker Compose file not found: $COMPOSE_FILE"
        exit 1
    fi
    
    # Check if Docker is running
    if ! docker info > /dev/null 2>&1; then
        log_error "Docker is not running"
        exit 1
    fi
    
    # Check if Docker Compose is available
    if ! command -v docker-compose > /dev/null 2>&1; then
        log_error "Docker Compose is not installed"
        exit 1
    fi
    
    log_info "Prerequisites check passed"
}

# Load environment variables
load_environment() {
    log_info "Loading environment variables..."
    
    # Load environment variables from .env.prod
    set -a
    source "$ENV_FILE"
    set +a
    
    # Export required variables
    export VERSION BUILD_DATE VCS_REF
    export POSTGRES_DB POSTGRES_USER POSTGRES_PASSWORD
    export REDIS_PASSWORD
    export SECRET_KEY AGENT_FRAMEWORK_ENDPOINT AGENT_FRAMEWORK_API_KEY
    export REACT_APP_API_URL
    export GRAFANA_USER GRAFANA_PASSWORD
    
    log_info "Environment variables loaded"
}

# Build Docker images
build_images() {
    log_info "Building Docker images..."
    
    cd "$PROJECT_ROOT"
    
    # Build backend image
    log_info "Building backend image..."
    docker build -f backend/Dockerfile.prod -t customer-support-backend:$VERSION ./backend
    
    # Build frontend image
    log_info "Building frontend image..."
    docker build -f frontend/Dockerfile.prod -t customer-support-frontend:$VERSION ./frontend
    
    log_info "Docker images built successfully"
}

# Run database migrations
run_migrations() {
    log_info "Running database migrations..."
    
    cd "$PROJECT_ROOT"
    
    # Start only the database service
    docker-compose -f "$COMPOSE_FILE" up -d postgres
    
    # Wait for database to be ready
    log_info "Waiting for database to be ready..."
    sleep 10
    
    # Run migrations
    docker-compose -f "$COMPOSE_FILE" run --rm backend python scripts/migrate.py upgrade
    
    log_info "Database migrations completed"
}

# Deploy services
deploy_services() {
    log_info "Deploying services..."
    
    cd "$PROJECT_ROOT"
    
    # Stop existing services
    docker-compose -f "$COMPOSE_FILE" down
    
    # Start services
    docker-compose -f "$COMPOSE_FILE" up -d
    
    log_info "Services deployed"
}

# Wait for services to be healthy
wait_for_services() {
    log_info "Waiting for services to be healthy..."
    
    local services=("postgres" "redis" "backend" "frontend" "prometheus" "grafana")
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        local all_healthy=true
        
        for service in "${services[@]}"; do
            if ! docker-compose -f "$COMPOSE_FILE" ps "$service" | grep -q "Up (healthy)"; then
                all_healthy=false
                break
            fi
        done
        
        if [ "$all_healthy" = true ]; then
            log_info "All services are healthy"
            return 0
        fi
        
        log_info "Waiting for services... (attempt $attempt/$max_attempts)"
        sleep 10
        ((attempt++))
    done
    
    log_error "Services did not become healthy within the expected time"
    return 1
}

# Run health checks
run_health_checks() {
    log_info "Running health checks..."
    
    # Check backend health
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        log_info "Backend health check passed"
    else
        log_error "Backend health check failed"
        return 1
    fi
    
    # Check frontend health
    if curl -f http://localhost:80/health > /dev/null 2>&1; then
        log_info "Frontend health check passed"
    else
        log_error "Frontend health check failed"
        return 1
    fi
    
    # Check Prometheus health
    if curl -f http://localhost:9090/-/healthy > /dev/null 2>&1; then
        log_info "Prometheus health check passed"
    else
        log_error "Prometheus health check failed"
        return 1
    fi
    
    # Check Grafana health
    if curl -f http://localhost:3000/api/health > /dev/null 2>&1; then
        log_info "Grafana health check passed"
    else
        log_error "Grafana health check failed"
        return 1
    fi
    
    log_info "All health checks passed"
}

# Cleanup old images
cleanup() {
    log_info "Cleaning up old Docker images..."
    
    # Remove unused images
    docker image prune -f
    
    # Remove old versions of our images (keep last 2 versions)
    docker images --format "table {{.Repository}}\t{{.Tag}}" | grep "customer-support" | \
    tail -n +3 | awk '{print $1":"$2}' | tail -n +3 | \
    xargs -r docker rmi
    
    log_info "Cleanup completed"
}

# Main deployment function
main() {
    log_info "Starting deployment..."
    
    check_prerequisites
    load_environment
    build_images
    run_migrations
    deploy_services
    wait_for_services
    run_health_checks
    cleanup
    
    log_info "Deployment completed successfully!"
    
    # Display service URLs
    echo ""
    log_info "Service URLs:"
    echo "  Frontend: http://localhost:80"
    echo "  Backend API: http://localhost:8000"
    echo "  Prometheus: http://localhost:9090"
    echo "  Grafana: http://localhost:3000"
    echo "  AlertManager: http://localhost:9093"
    echo ""
    log_info "Grafana credentials: $GRAFANA_USER / $GRAFANA_PASSWORD"
}

# Handle script arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "build")
        check_prerequisites
        load_environment
        build_images
        ;;
    "migrate")
        check_prerequisites
        load_environment
        run_migrations
        ;;
    "health")
        run_health_checks
        ;;
    "cleanup")
        cleanup
        ;;
    "logs")
        docker-compose -f "$COMPOSE_FILE" logs -f "${2:-}"
        ;;
    "stop")
        docker-compose -f "$COMPOSE_FILE" down
        ;;
    "restart")
        docker-compose -f "$COMPOSE_FILE" restart
        ;;
    *)
        echo "Usage: $0 {deploy|build|migrate|health|cleanup|logs|stop|restart}"
        exit 1
        ;;
esac
