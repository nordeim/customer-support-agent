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
