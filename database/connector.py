"""
Database connector for various storage systems (CSV, Google Sheets, Notion).
"""

import csv
import os
from datetime import datetime
from typing import Dict, Any, List

class DatabaseConnector:
    """Connects to various database systems for logging customer interactions."""
    
    def __init__(self, db_type: str = "csv", **kwargs):
        """
        Initialize the database connector.
        
        Args:
            db_type: Type of database ("csv", "google_sheets", "notion")
            **kwargs: Additional configuration parameters
        """
        self.db_type = db_type
        self.config = kwargs
        self.initialized = False
        
        if db_type == "csv":
            self.file_path = self.config.get("file_path", "customer_interactions.csv")
            self._initialize_csv()
            self.initialized = True
        else:
            # For Google Sheets and Notion, initialization would require auth
            # This is a placeholder for future implementation
            print(f"Database type '{db_type}' requires additional setup")
            
    def _initialize_csv(self):
        """Initialize CSV file with headers if it doesn't exist."""
        if not os.path.exists(self.file_path):
            headers = [
                "timestamp", "session_id", "customer_message", "issue_category",
                "order_ids", "product_names", "problem_types", "solution",
                "classification_confidence"
            ]
            
            with open(self.file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                
    def log_interaction(self, session_data: Dict[str, Any]) -> bool:
        """
        Log a customer interaction to the database.
        
        Args:
            session_data: Dictionary containing session data to log
            
        Returns:
            True if successful, False otherwise
        """
        if not self.initialized:
            print("Database connector not properly initialized")
            return False
            
        try:
            if self.db_type == "csv":
                return self._log_to_csv(session_data)
            else:
                # Placeholder for other database types
                print(f"Logging to {self.db_type} not yet implemented")
                return False
        except Exception as e:
            print(f"Error logging interaction: {e}")
            return False
            
    def _log_to_csv(self, session_data: Dict[str, Any]) -> bool:
        """
        Log session data to CSV file.
        
        Args:
            session_data: Dictionary containing session data to log
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Prepare data for logging
            timestamp = session_data.get("timestamp", datetime.now().isoformat())
            session_id = session_data.get("session_id", "")
            customer_message = session_data.get("customer_message", "")
            issue_category = session_data.get("issue_category", "")
            order_ids = ";".join(session_data.get("order_ids", []))
            product_names = ";".join(session_data.get("product_names", []))
            problem_types = ";".join(session_data.get("problem_types", []))
            solution = session_data.get("solution", "")
            confidence = session_data.get("classification_confidence", "")
            
            # Write to CSV
            with open(self.file_path, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    timestamp, session_id, customer_message, issue_category,
                    order_ids, product_names, problem_types, solution,
                    confidence
                ])
                
            return True
        except Exception as e:
            print(f"Error writing to CSV: {e}")
            return False
            
    # TODO: Add methods for Google Sheets and Notion integration
    # These would require additional libraries and authentication