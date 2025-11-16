"""
Base Agent class for the AI Customer Issue Analyzer system.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

class BaseAgent(ABC):
    """Abstract base class for all agents in the system."""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
    @abstractmethod
    async def process(self, session_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the customer issue based on the current session state.
        
        Args:
            session_state: Dictionary containing the current state of the session
            
        Returns:
            Updated session state with agent-specific results
        """
        pass
        
    def log_activity(self, message: str, level: str = "info"):
        """Log agent activity for observability."""
        log_message = f"[{self.name}] {message}"
        if level.lower() == "error":
            self.logger.error(log_message)
        elif level.lower() == "warning":
            self.logger.warning(log_message)
        elif level.lower() == "debug":
            self.logger.debug(log_message)
        else:
            self.logger.info(log_message)