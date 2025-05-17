"""Logging configuration for the application."""

import logging
import sys
from typing import Optional
from config import Config

def setup_logger(name: str, config: Config) -> logging.Logger:
    """Set up a logger with the given name and configuration.
    
    Args:
        name: Name of the logger
        config: Application configuration
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(config.LOG_LEVEL)
    
    # Create handlers
    console_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler('app.log')
    
    # Create formatters and add it to handlers
    formatter = logging.Formatter(config.LOG_FORMAT)
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

class LoggedAgent:
    """Mixin to add logging capabilities to agents."""
    
    def __init__(self, name: str, config: Config):
        """Initialize the logged agent.
        
        Args:
            name: Name of the agent
            config: Application configuration
        """
        self.logger = setup_logger(f"agent.{name}", config)
    
    def log_state(self, state: dict, message: Optional[str] = None) -> None:
        """Log the current state with an optional message.
        
        Args:
            state: Current state dictionary
            message: Optional message to log with the state
        """
        if message:
            self.logger.debug(f"{message} - State: {state}")
        else:
            self.logger.debug(f"Current state: {state}")
    
    def log_error(self, error: Exception, context: Optional[dict] = None) -> None:
        """Log an error with optional context.
        
        Args:
            error: The error that occurred
            context: Optional context dictionary
        """
        if context:
            self.logger.error(f"Error: {str(error)} - Context: {context}", exc_info=True)
        else:
            self.logger.error(f"Error: {str(error)}", exc_info=True) 