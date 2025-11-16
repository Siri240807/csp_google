"""
Analyzer Agent for extracting key details from customer issues.
"""

import re
from typing import Dict, Any, List
from .base_agent import BaseAgent

class AnalyzerAgent(BaseAgent):
    """Agent responsible for extracting key details from customer issues."""
    
    def __init__(self):
        super().__init__("AnalyzerAgent")
        
    async def process(self, session_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract key details from the customer issue.
        
        Args:
            session_state: Dictionary containing the current state of the session
            
        Returns:
            Updated session state with extracted details
        """
        self.log_activity("Starting issue analysis")
        
        # Extract customer message
        customer_message = session_state.get("customer_message", "")
        
        # Extract key details
        order_ids = self._extract_order_ids(customer_message)
        product_names = self._extract_product_names(customer_message)
        problem_types = self._extract_problem_types(customer_message)
        
        # Update session state
        session_state["order_ids"] = order_ids
        session_state["product_names"] = product_names
        session_state["problem_types"] = problem_types
        
        self.log_activity(f"Extracted {len(order_ids)} order IDs, {len(product_names)} products, {len(problem_types)} problem types")
        
        return session_state
        
    def _extract_order_ids(self, message: str) -> List[str]:
        """
        Extract order IDs from the message.
        
        Args:
            message: Customer message to analyze
            
        Returns:
            List of order IDs found in the message
        """
        # Pattern for order IDs (various formats)
        patterns = [
            r'\b(?:ORDER|ORD|Order)[\-_\s]?(?:ID)?[\-_\s]?([A-Z0-9]{6,12})\b',
            r'\b([A-Z]{2}\d{8,10})\b',  # Format like AB12345678
            r'\b(\d{8,12})\b'  # Pure numeric order IDs
        ]
        
        order_ids = []
        for pattern in patterns:
            matches = re.findall(pattern, message, re.IGNORECASE)
            order_ids.extend(matches)
            
        return list(set(order_ids))  # Remove duplicates
        
    def _extract_product_names(self, message: str) -> List[str]:
        """
        Extract product names from the message.
        
        Args:
            message: Customer message to analyze
            
        Returns:
            List of product names found in the message
        """
        # This is a simplified implementation
        # In a real system, this would use NLP techniques or product databases
        product_indicators = ["product", "item", "model"]
        products = []
        
        # Simple approach: look for quoted text near product indicators
        for indicator in product_indicators:
            pattern = rf'{indicator}["\']?\s*:?\s*["\']?([^"\'.!?]+)["\']?'
            matches = re.findall(pattern, message, re.IGNORECASE)
            products.extend(matches)
            
        return list(set(products))  # Remove duplicates
        
    def _extract_problem_types(self, message: str) -> List[str]:
        """
        Extract problem types from the message.
        
        Args:
            message: Customer message to analyze
            
        Returns:
            List of problem types found in the message
        """
        # Common problem type keywords
        problem_keywords = {
            "delay": ["delay", "late", "slow"],
            "damage": ["damage", "broken", "cracked", "defective"],
            "missing": ["missing", "lost", "not received"],
            "wrong_item": ["wrong", "incorrect", "mistake"],
            "quality": ["quality", "poor", "bad"],
            "functionality": ["work", "working", "function", "operate"],
            "billing": ["charge", "billed", "price", "cost"],
            "access": ["access", "login", "enter", "open"]
        }
        
        problem_types = []
        message_lower = message.lower()
        
        for problem_type, keywords in problem_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                problem_types.append(problem_type)
                
        return list(set(problem_types))  # Remove duplicates