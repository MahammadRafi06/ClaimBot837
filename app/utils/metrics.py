"""Metrics collection and monitoring utilities."""

import time
from functools import wraps
from typing import Any, Callable, Dict, Optional
from prometheus_client import Counter, Histogram, start_http_server

# Metrics definitions
PROCESSING_TIME = Histogram(
    'agent_processing_seconds',
    'Time spent processing in agent',
    ['agent_name', 'status']
)

PROCESSING_ERRORS = Counter(
    'agent_errors_total',
    'Number of processing errors',
    ['agent_name', 'error_type']
)

SUCCESSFUL_PROCESSES = Counter(
    'agent_successes_total',
    'Number of successful processes',
    ['agent_name']
)

def track_time_and_errors(f: Callable) -> Callable:
    """Decorator to track processing time and errors.
    
    Args:
        f: Function to wrap
        
    Returns:
        Wrapped function with timing and error tracking
    """
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        try:
            result = f(self, *args, **kwargs)
            PROCESSING_TIME.labels(
                agent_name=self.name,
                status='success'
            ).observe(time.time() - start_time)
            SUCCESSFUL_PROCESSES.labels(agent_name=self.name).inc()
            return result
        except Exception as e:
            PROCESSING_TIME.labels(
                agent_name=self.name,
                status='error'
            ).observe(time.time() - start_time)
            PROCESSING_ERRORS.labels(
                agent_name=self.name,
                error_type=type(e).__name__
            ).inc()
            raise
    return wrapper

class MetricsManager:
    """Manager for application metrics."""
    
    def __init__(self, port: int = 8000):
        """Initialize the metrics manager.
        
        Args:
            port: Port to expose metrics on
        """
        self.port = port
    
    def start(self) -> None:
        """Start the metrics server."""
        start_http_server(self.port)
    
    @staticmethod
    def track_state_size(state: Dict[str, Any]) -> None:
        """Track the size of the state dictionary.
        
        Args:
            state: State dictionary to measure
        """
        # Implementation for state size tracking
        pass
    
    @staticmethod
    def track_llm_usage(tokens: int, model: str) -> None:
        """Track LLM token usage.
        
        Args:
            tokens: Number of tokens used
            model: Name of the model used
        """
        # Implementation for LLM usage tracking
        pass 