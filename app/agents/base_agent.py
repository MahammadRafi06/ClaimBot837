"""Base agent class for the claims processing system."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from ..utils.logging import LoggedAgent
from config import Config

class BaseAgent(ABC, LoggedAgent):
    """Base class for all agents in the system."""
    
    def __init__(self, name: str, config: Config):
        """Initialize the agent.
        
        Args:
            name: Name of the agent
            config: Application configuration
        """
        super().__init__(name, config)
        self.name = name
        self.config = config
        self.max_retries = config.MAX_RETRIES
    
    @abstractmethod
    def _process_impl(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Implementation of the processing logic.
        
        This method should be implemented by concrete agent classes.
        
        Args:
            state: Current state dictionary
            
        Returns:
            Updated state dictionary
        """
        pass
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the current state with error handling and logging.
        
        Args:
            state: Current state dictionary
            
        Returns:
            Updated state dictionary
        """
        self.log_state(state, f"Starting {self.name} processing")
        
        retries = 0
        last_error = None
        
        while retries < self.max_retries:
            try:
                result = self._process_impl(state)
                self.log_state(result, f"Completed {self.name} processing")
                return result
            except Exception as e:
                retries += 1
                last_error = e
                self.log_error(e, {"state": state, "retry": retries})
                if retries >= self.max_retries:
                    break
        
        raise RuntimeError(f"Failed to process after {retries} retries") from last_error
    
    def validate_state(self, state: Dict[str, Any], required_keys: list[str]) -> None:
        """Validate that the state contains required keys.
        
        Args:
            state: State dictionary to validate
            required_keys: List of required keys
            
        Raises:
            ValueError: If any required keys are missing
        """
        missing_keys = [key for key in required_keys if key not in state]
        if missing_keys:
            error = f"Missing required keys in state: {missing_keys}"
            self.log_error(ValueError(error), {"state": state})
            raise ValueError(error)
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})" 