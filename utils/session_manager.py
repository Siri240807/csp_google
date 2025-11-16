"""
Session Manager for maintaining state across agent interactions.
"""

import json
from typing import Dict, Any
from datetime import datetime

class SessionManager:
    """Manages session state for customer interactions."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.state = {
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "customer_message": "",
            "issue_category": "",
            "order_ids": [],
            "product_names": [],
            "problem_types": [],
            "solution": "",
            "classification_confidence": 0.0
        }
        
    def update_state(self, updates: Dict[str, Any]):
        """
        Update the session state with new information.
        
        Args:
            updates: Dictionary of key-value pairs to update in the state
        """
        self.state.update(updates)
        self.state["updated_at"] = datetime.now().isoformat()
        
    def get_state(self) -> Dict[str, Any]:
        """
        Get the current session state.
        
        Returns:
            Current session state dictionary
        """
        return self.state.copy()
        
    def save_to_file(self, filepath: str):
        """
        Save the session state to a JSON file.
        
        Args:
            filepath: Path to save the session state
        """
        with open(filepath, 'w') as f:
            json.dump(self.state, f, indent=2)
            
    @classmethod
    def load_from_file(cls, filepath: str) -> 'SessionManager':
        """
        Load a session state from a JSON file.
        
        Args:
            filepath: Path to load the session state from
            
        Returns:
            SessionManager instance with loaded state
        """
        with open(filepath, 'r') as f:
            state = json.load(f)
            
        session = cls(state["session_id"])
        session.state = state
        return session
        
    def compact_context(self, max_length: int = 1000) -> Dict[str, Any]:
        """
        Compact the context to reduce memory usage while preserving important information.
        
        Args:
            max_length: Maximum length for text fields
            
        Returns:
            Compacted state dictionary
        """
        compacted_state = self.state.copy()
        
        # Truncate long text fields
        for key, value in compacted_state.items():
            if isinstance(value, str) and len(value) > max_length:
                compacted_state[key] = value[:max_length] + "...[truncated]"
                
        return compacted_state