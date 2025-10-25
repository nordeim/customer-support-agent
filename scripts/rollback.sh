#!/bin/bash
# scripts/rollback.sh

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

# Load environment variables
load_environment() {
    log_info "Loading environment variables..."
    
    if [ ! -f "$ENV_FILE" ]; then
        log_error "Environment file not found: $ENV_FILE"
        exit 1
    fi
    
    # Load environment variables from .env.prod
    set -a
    source "$ENV_FILE"
    set +a
    
    log_info "Environment variables loaded"
}

# Get previous version
get_previous_version() {
    log_info "Getting previous version..."
    
    # Get the previous version tag
    local previous_version=$(git describe --tags --abbrev=0 HEAD~1 2>/dev/null || echo "")
    
    if [ -z "$previous_version" ]; then
        log_error "No previous version found"
        exit 1
    fi
    
    echo "$previous_version"
}

# Backup current data
backup_data() {
    log_info "Backing up current data..."
    
    local backup_dir="${PROJECT_ROOT}/backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    # Backup database
    docker-compose -f "$COMPOSE_FILE" exec -T postgres pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" > "$backup_dir/database.sql"
    
    # Backup Redis data
    docker cp $(docker-compose -f "$COMPOSE_FILE" ps -q redis):/data "$backup_dir/redis"
    
    # Backup uploads
    docker cp $(docker-compose -f "$COMPOSE_FILE" ps -q backend):/app/uploads "$backup_dir/"
    
    log_info "Data backed up to: $backup_dir"
    echo "$backup_dir"
}

# Rollback to previous version
rollback_to_version() {
    local target_version="$1"
    
    log_info "Rolling back to version: $target_version"
    
    # Stop current services
    docker-compose -f "$COMPOSE_FILE" down
    
    # Pull previous images
    docker pull customer-support-backend:$target_version
    docker pull customer-support-frontend:$target_version
    
    # Update environment file with previous version
    sed -i.bak "s/VERSION=.*/VERSION=$target_version/" "$ENV_FILE"
    
    # Load updated environment
    load_environment
    
    # Start services with previous version
    docker-compose -f "$COMPOSE_FILE" up -d
    
    log_info "Rollback to version $target_version completed"
}

# Restore data if needed
restore_data() {
    local backup_dir="$1"
    
    if [ -z "$backup_dir" ] || [ ! -d "$backup_dir" ]; then
        log_warn "No backup directory provided or directory does not exist"
        return 0
    fi
    
    log_info "Restoring data from backup: $backup_dir"
    
    # Restore database
    if [ -f "$backup_dir/database.sql" ]; then
        docker-compose -f "$COMPOSE_FILE" exec -T postgres psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" < "$backup_dir/database.sql"
        log_info "Database restored"
    fi
    
    # Restore Redis data
    if [ -d "$backup_dir/redis" ]; then
        docker cp "$backup_dir/redis" $(docker-compose -f "$COMPOSE_FILE" ps -q redis):/
        log_info "Redis data restored"
    fi
    
    # Restore uploads
    if [ -d "$backup_dir/uploads" ]; then
        docker cp "$backup_dir/uploads" $(docker-compose -f "$COMPOSE_FILE" ps -q backend):/app/
        log_info "Uploads restored"
    fi
    
    log_info "Data restoration completed"
}

# Verify rollback
verify_rollback() {
    log_info "Verifying rollback..."
    
    # Wait for services to be healthy
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f http://localhost:8000/health > /dev/null 2>&1 && \
           curl -f http://localhost:80/health > /dev/null 2>&1; then
            log_info "Rollback verification successful"
            return 0
        fi
        
        log_info "Waiting for services... (attempt $attempt/$max_attempts)"
        sleep 10
        ((attempt++))
    done
    
    log_error "Rollback verification failed"
    return 1
}

# Main rollback function
main() {
    local target_version="${1:-}"
    local backup_dir=""
    
    # If no version specified, get previous version
    if [ -z "$target_version" ]; then
        target_version=$(get_previous_version)
    fi
    
    log_info "Starting rollback to version: $target_version"
    
    load_environment
    
    # Backup current data
    backup_dir=$(backup_data)
    
    # Perform rollback
    rollback_to_version "$target_version"
    
    # Wait for services
    sleep 30
    
    # Verify rollback
    if verify_rollback; then
        log_info "Rollback completed successfully!"
        
        # Ask if user wants to restore data
        read -p "Do you want to restore data from backup? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            restore_data "$backup_dir"
        fi
    else
        log_error "Rollback verification failed!"
        log_info "You can restore data from backup manually: $backup_dir"
        exit 1
    fi
}

# Handle script arguments
case "${1:-}" in
    "")
        main
        ;;
    "to")
        main "$2"
        ;;
    "restore")
        load_environment
        restore_data "$2"
        ;;
    *)
        echo "Usage: $0 [to <version>] [restore <backup_dir>]"
        echo "Examples:"
        echo "  $0                    # Rollback to previous version"
        echo "  $0 to 1.0.0          # Rollback to specific version"
        echo "  $0 restore /path/to/backup  # Restore data from backup"
        exit 1
        ;;
esac
