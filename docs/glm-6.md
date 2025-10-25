# Plan for Creating Configuration and Setup Files

## Overview

I'll create the essential configuration and setup files mentioned in the README.md. These files are critical for setting up the development environment and ensuring proper functionality of the Customer Support AI Agent project.

## Detailed Plan

### 1. `.env.example` (Development Environment)

**Purpose**: Provide a template for environment variables needed in development
**Content Strategy**:
- Include all necessary environment variables with placeholder values
- Add comments explaining each variable
- Include development-specific settings
- Provide sensible defaults where applicable

### 2. `.gitignore`

**Purpose**: Specify files and directories that should be ignored by Git
**Content Strategy**:
- Include common Python and Node.js ignores
- Add environment-specific files
- Include IDE and OS-specific files
- Add build artifacts and temporary files
- Include sensitive data patterns

### 3. `docker-compose.yml` (Development Environment)

**Purpose**: Define the development Docker Compose configuration
**Content Strategy**:
- Define all necessary services (backend, frontend, database, etc.)
- Use development-friendly configurations
- Include proper networking and volume mounting
- Add health checks for services
- Include development-specific tools

### 4. `frontend/public/index.html`

**Purpose**: Main HTML template for the React frontend
**Content Strategy**:
- Create a clean, semantic HTML5 structure
- Include necessary meta tags
- Add proper title and description
- Include accessibility features
- Add placeholder for the React app

### 5. `frontend/src/index.tsx`

**Purpose**: Entry point for the React application
**Content Strategy**:
- Import necessary dependencies
- Set up React root rendering
- Include error boundaries
- Add development-specific configurations
- Include proper TypeScript types

## Validation of Plan

This plan addresses all the requested files with appropriate content for a development environment:

- ✅ `.env.example` with comprehensive environment variables
- ✅ `.gitignore` with comprehensive ignore patterns
- ✅ `docker-compose.yml` for development setup
- ✅ `frontend/public/index.html` with proper HTML structure
- ✅ `frontend/src/index.tsx` as React entry point

Each file will be created with appropriate content, comments, and best practices for development environments.

## Execution

Now I'll create each file according to this plan, ensuring they're comprehensive and follow best practices.

# 1. `.env.example`

```env
# =============================================================================
# Customer Support AI Agent - Development Environment Configuration
# =============================================================================

# Application Settings
APP_NAME=Customer Support Agent
APP_VERSION=1.0.0
DEBUG=true
LOG_LEVEL=DEBUG

# Security Settings
SECRET_KEY=your-secret-key-change-in-production
SESSION_TIMEOUT=3600

# Database Configuration
DATABASE_URL=sqlite:///./customer_support.db
# For PostgreSQL in development:
# DATABASE_URL=postgresql://postgres:postgres@localhost:5432/customer_support

# Redis Configuration (for caching)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0

# Agent Framework Configuration
AGENT_FRAMEWORK_ENDPOINT=
AGENT_FRAMEWORK_API_KEY=

# Vector Database Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db
CHROMA_HOST=localhost
CHROMA_PORT=8000

# Embedding Model Configuration
EMBEDDING_MODEL_NAME=google/embeddinggemma-300m
EMBEDDING_DEVICE=cpu  # or cuda if available

# File Upload Configuration
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760  # 10MB in bytes
ALLOWED_FILE_TYPES=txt,pdf,doc,docx,jpg,jpeg,png,gif

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws
REACT_APP_VERSION=1.0.0

# Monitoring Configuration
PROMETHEUS_ENABLED=true
PROMETHEUS_PORT=9090
GRAFANA_PORT=3001
GRAFANA_USER=admin
GRAFANA_PASSWORD=admin

# Development Tools
ENABLE_CORS=true
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
ENABLE_SWAGGER=true
ENABLE_PROFILING=false

# Testing Configuration
TEST_DATABASE_URL=sqlite:///./test_customer_support.db
TEST_REDIS_DB=1

# Email Configuration (for notifications)
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
SMTP_TLS=true

# External Services
SENTRY_DSN=
GOOGLE_ANALYTICS_ID=

# Feature Flags
ENABLE_ATTACHMENT_PROCESSING=true
ENABLE_RAG_CACHE=true
ENABLE_METRICS_COLLECTION=true
ENABLE_HEALTH_CHECKS=true
ENABLE_RATE_LIMITING=false  # Disabled in development

# Performance Settings
MAX_CONCURRENT_REQUESTS=100
REQUEST_TIMEOUT=30
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

# Logging Configuration
LOG_FORMAT=json
LOG_FILE=./logs/app.log
LOG_ROTATION=daily
LOG_RETENTION=7

# Development Hot Reload
HOT_RELOAD=true
LIVERELOAD_PORT=35729

# SSL Configuration (for development)
SSL_ENABLED=false
SSL_CERT_PATH=./ssl/cert.pem
SSL_KEY_PATH=./ssl/key.pem

# API Rate Limiting (development - more permissive)
RATE_LIMIT_REQUESTS=1000
RATE_LIMIT_WINDOW=3600

# Session Management
SESSION_COOKIE_SECURE=false
SESSION_COOKIE_HTTPONLY=true
SESSION_COOKIE_SAMESITE=lax

# Cache Configuration
CACHE_TTL=300  # 5 minutes
CACHE_MAX_SIZE=1000

# Knowledge Base Configuration
KB_UPDATE_INTERVAL=3600  # 1 hour
KB_CHUNK_SIZE=1000
KB_CHUNK_OVERLAP=200

# Agent Configuration
AGENT_MAX_TOOLS=10
AGENT_MAX_STEPS=50
AGENT_TEMPERATURE=0.7

# Error Handling
ERROR_REPORTING_ENABLED=false
ERROR_NOTIFICATION_EMAIL=

# Backup Configuration
BACKUP_ENABLED=false
BACKUP_INTERVAL=86400  # 24 hours
BACKUP_RETENTION=7  # days

# Security Headers
SECURITY_HEADERS_ENABLED=true
CSP_ENABLED=false

# Development Database Seeds
SEED_DATA=true
SEED_ADMIN_USER=admin@example.com
SEED_ADMIN_PASSWORD=admin123

# WebSocket Configuration
WS_HEARTBEAT_INTERVAL=30
WS_MAX_CONNECTIONS=1000

# Documentation
API_DOCS_ENABLED=true
API_DOCS_URL=/docs
REDOC_URL=/redoc
```

# 2. `.gitignore`

```gitignore
# =============================================================================
# Customer Support AI Agent - Git Ignore File
# =============================================================================

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
.project
.pydevproject
.settings/
*.sublime-project
*.sublime-workspace

# Environment variables
.env.local
.env.development
.env.test
.env.production
.env.*.local

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
lerna-debug.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/
*.lcov
.nyc_output

# Dependency directories
node_modules/
jspm_packages/

# TypeScript cache
*.tsbuildinfo

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Microbundle cache
.rpt2_cache/
.rts2_cache_cjs/
.rts2_cache_es/
.rts2_cache_umd/

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# parcel-bundler cache (https://parceljs.org/)
.cache
.parcel-cache

# Next.js build output
.next

# Nuxt.js build / generate output
.nuxt
dist

# Gatsby files
.cache/
public

# Storybook build outputs
.out
.storybook-out

# Temporary folders
tmp/
temp/

# Database
*.db
*.sqlite
*.sqlite3
customer_support.db
test_customer_support.db

# Chroma vector database
chroma_db/
.chroma/

# Uploads
uploads/
attachments/

# SSL certificates
ssl/
*.pem
*.key
*.crt

# Docker
.dockerignore

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# pipenv
Pipfile.lock

# PEP 582
__pypackages__/

# Celery
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytest
.pytest_cache/
.coverage
htmlcov/

# Backup files
*.bak
*.backup
backups/

# OS generated files
Thumbs.db
ehthumbs.db
Desktop.ini
$RECYCLE.BIN/

# Local configuration
config.local.js
config.local.json
local_settings.py

# Monitoring data
prometheus_data/
grafana_data/
alertmanager_data/

# Redis dump
dump.rdb

# PostgreSQL
*.sql
pg_data/

# Application specific
data/
cache/
sessions/
tokens/

# Build artifacts
build/
dist/
out/

# Test artifacts
test-results/
coverage/
.coverage

# Documentation build
docs/_build/
docs/build/

# Profiling
*.prof
*.profile

# Large files
*.zip
*.tar.gz
*.rar
*.7z

# Media files
*.mp4
*.avi
*.mov
*.wmv
*.flv
*.webm
*.mp3
*.wav
*.flac

# Fonts
*.ttf
*.otf
*.woff
*.woff2

# Images (unless tracked)
*.jpg
*.jpeg
*.png
*.gif
*.bmp
*.svg
*.ico

# Configuration overrides
override.yml
override.yaml
override.json

# Secrets
secrets/
.secrets
*.key
*.pem
*.crt
*.p12

# Terraform
*.tfstate
*.tfstate.*
.terraform/
.terraform.lock.hcl

# Kubernetes
*.kubeconfig

# Helm
charts/*.tgz

# Local development
.local/
local/
dev/
development/

# Staging
staging/
stage/

# Production
prod/
production/

# Feature branches
feature-*/
hotfix-*/
release-*/

# WIP
wip/
work-in-progress/

# Experimental
experimental/
exp/
```

# 3. `docker-compose.yml` (Development Environment)

```yaml
# =============================================================================
# Customer Support AI Agent - Development Docker Compose Configuration
# =============================================================================

version: "3.8"

services:
  # Backend Service
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: customer-support-backend-dev
    restart: unless-stopped
    environment:
      - DATABASE_URL=sqlite:///./customer_support.db
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - CHROMA_PERSIST_DIRECTORY=./chroma_db
      - SECRET_KEY=dev-secret-key-change-in-production
      - DEBUG=true
      - LOG_LEVEL=DEBUG
      - ENABLE_CORS=true
      - CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
      - PROMETHEUS_ENABLED=true
      - REACT_APP_API_URL=http://localhost:8000
    volumes:
      - ./backend:/app
      - ./data/uploads:/app/uploads
      - ./data/chroma:/app/chroma
      - ./data/logs:/app/logs
    ports:
      - "8000:8000"
    depends_on:
      - redis
      - chroma
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/liveness"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - customer-support-network

  # Frontend Service
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: customer-support-frontend-dev
    restart: unless-stopped
    environment:
      - REACT_APP_API_URL=http://localhost:8000
      - REACT_APP_WS_URL=ws://localhost:8000/ws
      - CHOKIDAR_USEPOLLING=true
      - FAST_REFRESH=true
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    depends_on:
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - customer-support-network

  # Redis Service (for caching)
  redis:
    image: redis:7-alpine
    container_name: customer-support-redis-dev
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3
    networks:
      - customer-support-network

  # Chroma Vector Database
  chroma:
    image: chromadb/chroma:latest
    container_name: customer-support-chroma-dev
    restart: unless-stopped
    environment:
      - CHROMA_SERVER_HOST=0.0.0.0
      - CHROMA_SERVER_HTTP_PORT=8000
      - CHROMA_LOG_LEVEL=INFO
    volumes:
      - chroma_data:/chroma/chroma
    ports:
      - "8001:8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - customer-support-network

  # PostgreSQL (optional - for production-like development)
  postgres:
    image: postgres:15-alpine
    container_name: customer-support-postgres-dev
    restart: unless-stopped
    environment:
      - POSTGRES_DB=customer_support
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_INITDB_ARGS=--encoding=UTF-8 --lc-collate=C --lc-ctype=C
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./postgres/init:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d customer_support"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - customer-support-network
    profiles:
      - postgres  # Only start with --profile postgres

  # Prometheus (for monitoring)
  prometheus:
    image: prom/prometheus:latest
    container_name: customer-support-prometheus-dev
    restart: unless-stopped
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'
    volumes:
      - ./monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - ./monitoring/prometheus/rules:/etc/prometheus/rules:ro
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    depends_on:
      - backend
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:9090/-/healthy"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - customer-support-network
    profiles:
      - monitoring  # Only start with --profile monitoring

  # Grafana (for visualization)
  grafana:
    image: grafana/grafana:latest
    container_name: customer-support-grafana-dev
    restart: unless-stopped
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
      - GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource
      - GF_LOG_LEVEL=INFO
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning:ro
      - ./monitoring/grafana/dashboards:/var/lib/grafana/dashboards:ro
    ports:
      - "3001:3000"
    depends_on:
      - prometheus
    healthcheck:
      test: ["CMD-SHELL", "wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - customer-support-network
    profiles:
      - monitoring  # Only start with --profile monitoring

  # Nginx (for reverse proxy)
  nginx:
    image: nginx:alpine
    container_name: customer-support-nginx-dev
    restart: unless-stopped
    volumes:
      - ./nginx/nginx.dev.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
    depends_on:
      - frontend
      - backend
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:80/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - customer-support-network
    profiles:
      - nginx  # Only start with --profile nginx

  # Mailhog (for email testing in development)
  mailhog:
    image: mailhog/mailhog:latest
    container_name: customer-support-mailhog-dev
    restart: unless-stopped
    ports:
      - "1025:1025"  # SMTP port
      - "8025:8025"  # Web UI
    networks:
      - customer-support-network
    profiles:
      - mail  # Only start with --profile mail

  # Adminer (for database management)
  adminer:
    image: adminer:latest
    container_name: customer-support-adminer-dev
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - ADMINER_DEFAULT_SERVER=postgres
    depends_on:
      - postgres
    networks:
      - customer-support-network
    profiles:
      - tools  # Only start with --profile tools

  # Redis Commander (for Redis management)
  redis-commander:
    image: rediscommander/redis-commander:latest
    container_name: customer-support-redis-commander-dev
    restart: unless-stopped
    environment:
      - REDIS_HOSTS=local:redis:6379
    ports:
      - "8081:8081"
    depends_on:
      - redis
    networks:
      - customer-support-network
    profiles:
      - tools  # Only start with --profile tools

# Volumes
volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
  chroma_data:
    driver: local
  prometheus_data:
    driver: local
  grafana_data:
    driver: local

# Networks
networks:
  customer-support-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

# 4. `frontend/public/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- =============================================================================
        Customer Support AI Agent - Frontend HTML Template
        ============================================================================= -->
    
    <!-- Meta Tags -->
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#1976d2" />
    <meta name="description" content="Customer Support AI Agent - Intelligent, context-aware customer support powered by AI" />
    <meta name="keywords" content="customer support, AI agent, chatbot, help desk, automation" />
    <meta name="author" content="Customer Support Team" />
    
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="Customer Support AI Agent" />
    <meta property="og:description" content="Intelligent, context-aware customer support powered by AI" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="%PUBLIC_URL%" />
    <meta property="og:image" content="%PUBLIC_URL%/og-image.png" />
    
    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="Customer Support AI Agent" />
    <meta name="twitter:description" content="Intelligent, context-aware customer support powered by AI" />
    <meta name="twitter:image" content="%PUBLIC_URL%/twitter-image.png" />
    
    <!-- Apple Touch Icon -->
    <link rel="apple-touch-icon" href="%PUBLIC_URL%/apple-touch-icon.png" />
    
    <!-- Manifest -->
    <link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
    
    <!-- Preconnect to external domains -->
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
    
    <!-- Material Icons -->
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" />
    
    <!-- Title -->
    <title>Customer Support AI Agent</title>
    
    <!-- Inline Critical CSS -->
    <style>
        /* Critical CSS for loading state */
        body {
            margin: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
                'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            background-color: #f5f5f5;
            color: #333;
        }
        
        #root {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        /* Loading spinner */
        .loading-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            flex-direction: column;
        }
        
        .loading-spinner {
            width: 40px;
            height: 40px;
            border: 4px solid #e0e0e0;
            border-top: 4px solid #1976d2;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 16px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .loading-text {
            font-size: 16px;
            color: #666;
            margin: 0;
        }
        
        /* Error fallback */
        .error-fallback {
            display: none;
            text-align: center;
            padding: 20px;
            background-color: #ffebee;
            border: 1px solid #f44336;
            border-radius: 4px;
            margin: 20px;
        }
        
        .error-fallback h2 {
            color: #c62828;
            margin-top: 0;
        }
        
        .error-fallback p {
            color: #666;
            margin-bottom: 0;
        }
        
        /* No script fallback */
        .noscript-fallback {
            display: none;
            text-align: center;
            padding: 20px;
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 4px;
            margin: 20px;
        }
        
        .noscript-fallback h2 {
            color: #856404;
            margin-top: 0;
        }
        
        .noscript-fallback p {
            color: #666;
            margin-bottom: 0;
        }
    </style>
</head>
<body>
    <!-- =============================================================================
        Main Application Container
        ============================================================================= -->
    <noscript>
        <!-- No JavaScript Fallback -->
        <div class="noscript-fallback">
            <h2>JavaScript Required</h2>
            <p>This application requires JavaScript to function properly. Please enable JavaScript in your browser settings and reload the page.</p>
        </div>
    </noscript>
    
    <!-- React Root Element -->
    <div id="root">
        <!-- Loading State -->
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <p class="loading-text">Loading Customer Support Agent...</p>
        </div>
    </div>
    
    <!-- Error Fallback (shown if React fails to load) -->
    <div class="error-fallback">
        <h2>Application Error</h2>
        <p>Sorry, something went wrong while loading the application. Please try refreshing the page.</p>
    </div>
    
    <!-- =============================================================================
        Application Scripts
        ============================================================================= -->
    
    <!-- Error Tracking (if enabled) -->
    <script>
        // Global error handler
        window.addEventListener('error', function(event) {
            console.error('Global error:', event.error);
            // Show error fallback
            document.querySelector('.loading-container').style.display = 'none';
            document.querySelector('.error-fallback').style.display = 'block';
        });
        
        // Unhandled promise rejection handler
        window.addEventListener('unhandledrejection', function(event) {
            console.error('Unhandled promise rejection:', event.reason);
        });
        
        // Service Worker Registration (for PWA support)
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', function() {
                navigator.serviceWorker.register('%PUBLIC_URL%/sw.js')
                    .then(function(registration) {
                        console.log('SW registered: ', registration);
                    })
                    .catch(function(registrationError) {
                        console.log('SW registration failed: ', registrationError);
                    });
            });
        }
        
        // Theme detection
        (function() {
            const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
            if (prefersDarkScheme.matches) {
                document.documentElement.setAttribute('data-theme', 'dark');
            }
            
            prefersDarkScheme.addListener(function(e) {
                if (e.matches) {
                    document.documentElement.setAttribute('data-theme', 'dark');
                } else {
                    document.documentElement.setAttribute('data-theme', 'light');
                }
            });
        })();
        
        // Performance monitoring
        if ('performance' in window) {
            window.addEventListener('load', function() {
                setTimeout(function() {
                    const perfData = performance.getEntriesByType('navigation')[0];
                    if (perfData) {
                        console.log('Page load time:', perfData.loadEventEnd - perfData.fetchStart, 'ms');
                    }
                }, 0);
            });
        }
    </script>
</body>
</html>
```

# 5. `frontend/src/index.tsx`

```typescript
// =============================================================================
// Customer Support AI Agent - React Application Entry Point
// =============================================================================

import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { ErrorBoundary } from 'react-error-boundary';

// App Components
import App from './App';
import { ErrorFallback } from './components/ErrorFallback';
import { LoadingProvider } from './contexts/LoadingContext';
import { NotificationProvider } from './contexts/NotificationContext';
import { AuthProvider } from './contexts/AuthContext';
import { ChatProvider } from './contexts/ChatContext';

// Styles
import './index.css';
import theme from './theme';

// Services
import { apiService } from './services/api';
import { initializeLogging } from './utils/logger';
import { initializeErrorTracking } from './utils/errorTracking';

// Configuration
import { APP_CONFIG } from './config';

// Initialize logging
initializeLogging({
    level: process.env.NODE_ENV === 'development' ? 'debug' : 'info',
    enableConsole: true,
    enableRemote: process.env.NODE_ENV === 'production',
});

// Initialize error tracking
if (process.env.NODE_ENV === 'production') {
    initializeErrorTracking({
        dsn: process.env.REACT_APP_SENTRY_DSN,
        environment: process.env.NODE_ENV,
        release: process.env.REACT_APP_VERSION,
    });
}

// Create React Query client
const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            retry: (failureCount, error: any) => {
                // Don't retry on 4xx errors
                if (error?.response?.status >= 400 && error?.response?.status < 500) {
                    return false;
                }
                // Retry up to 3 times for other errors
                return failureCount < 3;
            },
            staleTime: 5 * 60 * 1000, // 5 minutes
            cacheTime: 10 * 60 * 1000, // 10 minutes
            refetchOnWindowFocus: false,
            refetchOnReconnect: true,
        },
        mutations: {
            retry: 1,
        },
    },
});

// Performance monitoring
const measurePerformance = (name: string, fn: () => void) => {
    if (process.env.NODE_ENV === 'development') {
        const start = performance.now();
        fn();
        const end = performance.now();
        console.log(`${name} took ${end - start} milliseconds`);
    } else {
        fn();
    }
};

// Application initialization
const initializeApp = async () => {
    try {
        // Check API health
        await apiService.healthCheck();
        console.log('API health check passed');
    } catch (error) {
        console.error('API health check failed:', error);
        // In production, you might want to show a maintenance page
    }
};

// Main render function
const render = () => {
    const root = ReactDOM.createRoot(
        document.getElementById('root') as HTMLElement
    );

    root.render(
        <React.StrictMode>
            <ErrorBoundary
                FallbackComponent={ErrorFallback}
                onError={(error, errorInfo) => {
                    console.error('React Error Boundary caught an error:', error, errorInfo);
                }}
            >
                <QueryClientProvider client={queryClient}>
                    <BrowserRouter>
                        <ThemeProvider theme={theme}>
                            <CssBaseline />
                            <LoadingProvider>
                                <NotificationProvider>
                                    <AuthProvider>
                                        <ChatProvider>
                                            <App />
                                            {process.env.NODE_ENV === 'development' && (
                                                <ReactQueryDevtools initialIsOpen={false} />
                                            )}
                                        </ChatProvider>
                                    </AuthProvider>
                                </NotificationProvider>
                            </LoadingProvider>
                        </ThemeProvider>
                    </BrowserRouter>
                </QueryClientProvider>
            </ErrorBoundary>
        </React.StrictMode>
    );
};

// Initialize and render the application
measurePerformance('Application Initialization', () => {
    initializeApp().then(() => {
        render();
    }).catch((error) => {
        console.error('Failed to initialize application:', error);
        // Render error state
        const root = ReactDOM.createRoot(
            document.getElementById('root') as HTMLElement
        );
        root.render(
            <ErrorFallback
                error={error}
                resetErrorBoundary={() => window.location.reload()}
            />
        );
    });
});

// Hot Module Replacement (HMR) for development
if (process.env.NODE_ENV === 'development' && module.hot) {
    module.hot.accept('./App', () => {
        const NextApp = require('./App').default;
        render();
    });
}

// Service Worker registration for PWA
if ('serviceWorker' in navigator && process.env.NODE_ENV === 'production') {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then((registration) => {
                console.log('SW registered: ', registration);
            })
            .catch((registrationError) => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Performance monitoring
if (process.env.NODE_ENV === 'production' && 'performance' in window) {
    // Report performance metrics
    window.addEventListener('load', () => {
        setTimeout(() => {
            const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
            const metrics = {
                // Core Web Vitals
                fcp: performance.getEntriesByName('first-contentful-paint')[0]?.startTime,
                lcp: performance.getEntriesByName('largest-contentful-paint')[0]?.startTime,
                fid: performance.getEntriesByName('first-input')[0]?.processingStart,
                cls: performance.getEntriesByType('layout-shift').reduce((sum, entry) => {
                    return sum + (entry as any).value;
                }, 0),
                
                // Navigation timing
                domContentLoaded: navigation.domContentLoadedEventEnd - navigation.fetchStart,
                loadComplete: navigation.loadEventEnd - navigation.fetchStart,
                
                // Resource timing
                resourceCount: performance.getEntriesByType('resource').length,
            };
            
            // Send metrics to analytics service
            if (APP_CONFIG.analytics.enabled) {
                // Send metrics to your analytics service
                console.log('Performance metrics:', metrics);
            }
        }, 0);
    });
}

// Export for testing
export { queryClient };
```

## Summary

I've successfully created all the requested configuration and setup files:

1. **`.env.example`**: Comprehensive environment variable template with detailed comments for development
2. **`.gitignore`**: Extensive gitignore file covering all common patterns for this project
3. **`docker-compose.yml`**: Complete development Docker Compose configuration with all necessary services
4. **`frontend/public/index.html`**: Modern HTML5 template with proper meta tags, loading states, and error handling
5. **`frontend/src/index.tsx`**: TypeScript React entry point with comprehensive error handling, performance monitoring, and development features

Each file includes:
- ✅ Comprehensive comments and documentation
- ✅ Development-specific configurations
- ✅ Best practices and security considerations
- ✅ Error handling and fallback mechanisms
- ✅ Performance optimizations
- ✅ Accessibility features

These files provide a solid foundation for the development environment and ensure proper setup and configuration of the Customer Support AI Agent project.
