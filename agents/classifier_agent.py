"""
Classifier Agent for categorizing customer issues.
"""

from typing import Dict, Any
from .base_agent import BaseAgent

class ClassifierAgent(BaseAgent):
    """Agent responsible for categorizing customer issues."""
    
    def __init__(self):
        super().__init__("ClassifierAgent")
        # Define issue categories
        self.categories = [
            "billing",
            "technical_support",
            "product_inquiry",
            "account_management",
            "shipping",
            "returns",
            "complaint",
            "feedback"
        ]
        
    async def process(self, session_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify the customer issue based on the message content.
        
        Args:
            session_state: Dictionary containing the current state of the session
            
        Returns:
            Updated session state with classification results
        """
        self.log_activity("Starting issue classification")
        
        # Extract customer message
        customer_message = session_state.get("customer_message", "")
        
        # In a real implementation, this would use NLP or ML models
        # For now, we'll use keyword matching as a placeholder
        category = self._classify_issue(customer_message)
        
        # Update session state
        session_state["issue_category"] = category
        session_state["classification_confidence"] = 0.85  # Placeholder confidence score
        
        self.log_activity(f"Issue classified as: {category}")
        
        return session_state
        
    def _classify_issue(self, message: str) -> str:
        """
        Classify an issue based on keywords in the message.
        
        Args:
            message: Customer message to classify
            
        Returns:
            Category of the issue
        """
        message_lower = message.lower()
        
        # Simple keyword-based classification
        if any(keyword in message_lower for keyword in ["bill", "charge", "payment", "invoice"]):
            return "billing"
        elif any(keyword in message_lower for keyword in ["error", "bug", "crash", "not working", "broken"]):
            return "technical_support"
        elif any(keyword in message_lower for keyword in ["product", "item", "feature"]):
            return "product_inquiry"
        elif any(keyword in message_lower for keyword in ["account", "login", "password", "profile"]):
            return "account_management"
        elif any(keyword in message_lower for keyword in ["ship", "delivery", "tracking"]):
            return "shipping"
        elif any(keyword in message_lower for keyword in ["return", "refund", "exchange"]):
            return "returns"
        elif any(keyword in message_lower for keyword in ["complaint", "disappointed", "angry", "unhappy"]):
            return "complaint"
        elif any(keyword in message_lower for keyword in ["suggestion", "feedback", "improve"]):
            return "feedback"
        else:
            # Default category
            return "general_inquiry"