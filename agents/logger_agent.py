"""
Logger Agent for recording customer interactions.
"""

import csv
import os
from datetime import datetime
from typing import Dict, Any
from .base_agent import BaseAgent

class LoggerAgent(BaseAgent):
    """Agent responsible for logging customer interactions."""
    
    def __init__(self, log_file_path: str = "customer_interactions.csv"):
        super().__init__("LoggerAgent")
        self.log_file_path = log_file_path
        self._initialize_log_file()
        
    async def process(self, session_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Log the customer interaction to a database/CSV file.
        
        Args:
            session_state: Dictionary containing the current state of the session
            
        Returns:
            Updated session state
        """
        self.log_activity("Starting interaction logging")
        
        try:
            # Log to CSV file
            self._log_to_csv(session_state)
            self.log_activity("Interaction logged successfully")
        except Exception as e:
            self.log_activity(f"Error logging interaction: {str(e)}", "error")
            
        return session_state
        
    def _initialize_log_file(self):
        """Initialize the log file with headers if it doesn't exist."""
        if not os.path.exists(self.log_file_path):
            headers = [
                "timestamp", "customer_message", "issue_category", 
                "order_ids", "product_names", "problem_types", 
                "solution", "classification_confidence"
            ]
            
            with open(self.log_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                
    def _log_to_csv(self, session_state: Dict[str, Any]):
        """
        Log the session state to a CSV file.
        
        Args:
            session_state: Session state to log
        """
        # Prepare data for logging
        timestamp = datetime.now().isoformat()
        customer_message = session_state.get("customer_message", "")
        issue_category = session_state.get("issue_category", "")
        order_ids = ";".join(session_state.get("order_ids", []))
        product_names = ";".join(session_state.get("product_names", []))
        problem_types = ";".join(session_state.get("problem_types", []))
        solution = session_state.get("solution", "")
        confidence = session_state.get("classification_confidence", "")
        
        # Write to CSV
        with open(self.log_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                timestamp, customer_message, issue_category,
                order_ids, product_names, problem_types,
                solution, confidence
            ])
            
    # TODO: Add methods for logging to Google Sheets or Notion
    # These would require additional libraries and authentication