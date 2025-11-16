"""
Orchestrator for coordinating the multi-agent customer support system.
"""

import asyncio
import uuid
from typing import Dict, Any
from agents.classifier_agent import ClassifierAgent
from agents.analyzer_agent import AnalyzerAgent
from agents.resolver_agent import ResolverAgent
from agents.logger_agent import LoggerAgent
from utils.session_manager import SessionManager
from database.connector import DatabaseConnector

class SupportOrchestrator:
    """Orchestrates the multi-agent customer support system."""
    
    def __init__(self):
        # Initialize agents
        self.classifier_agent = ClassifierAgent()
        self.analyzer_agent = AnalyzerAgent()
        self.resolver_agent = ResolverAgent()
        self.logger_agent = LoggerAgent()
        
        # Initialize database connector
        self.db_connector = DatabaseConnector(db_type="csv")
        
        # Track active sessions
        self.active_sessions = {}
        
    async def process_customer_message(self, customer_message: str) -> Dict[str, Any]:
        """
        Process a customer message through the multi-agent system.
        
        Args:
            customer_message: The customer's message
            
        Returns:
            Dictionary containing the final response and session data
        """
        # Create a new session
        session_id = str(uuid.uuid4())
        session_manager = SessionManager(session_id)
        session_manager.update_state({"customer_message": customer_message})
        
        # Store session
        self.active_sessions[session_id] = session_manager
        
        try:
            # Process through agents sequentially
            # 1. Classification
            session_state = await self.classifier_agent.process(session_manager.get_state())
            session_manager.update_state(session_state)
            
            # 2. Analysis
            session_state = await self.analyzer_agent.process(session_manager.get_state())
            session_manager.update_state(session_state)
            
            # 3. Resolution
            session_state = await self.resolver_agent.process(session_manager.get_state())
            session_manager.update_state(session_state)
            
            # 4. Logging
            session_state = await self.logger_agent.process(session_manager.get_state())
            session_manager.update_state(session_state)
            
            # Log to database
            self._log_to_database(session_manager.get_state())
            
            # Clean up session
            self.active_sessions.pop(session_id, None)
            
            # Return final result
            return {
                "session_id": session_id,
                "solution": session_state.get("solution", ""),
                "category": session_state.get("issue_category", ""),
                "confidence": session_state.get("classification_confidence", 0.0),
                "order_ids": session_state.get("order_ids", []),
                "products": session_state.get("product_names", [])
            }
            
        except Exception as e:
            # Handle errors gracefully
            error_message = f"We apologize, but we encountered an error processing your request: {str(e)}"
            session_manager.update_state({"solution": error_message})
            
            # Log error
            self._log_to_database(session_manager.get_state())
            
            # Clean up session
            self.active_sessions.pop(session_id, None)
            
            return {
                "session_id": session_id,
                "solution": error_message,
                "error": str(e)
            }
            
    def _log_to_database(self, session_state: Dict[str, Any]):
        """
        Log session data to the database.
        
        Args:
            session_state: Session state to log
        """
        try:
            self.db_connector.log_interaction(session_state)
        except Exception as e:
            print(f"Warning: Failed to log to database: {e}")
            
    async def process_concurrent_messages(self, messages: list) -> list:
        """
        Process multiple customer messages concurrently.
        
        Args:
            messages: List of customer messages
            
        Returns:
            List of results for each message
        """
        # Create tasks for concurrent processing
        tasks = [self.process_customer_message(msg) for msg in messages]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions in results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "session_id": f"error_{i}",
                    "solution": f"Failed to process message: {str(result)}",
                    "error": str(result)
                })
            else:
                processed_results.append(result)
                
        return processed_results

# Example usage function
async def demo():
    """Demonstrate the orchestrator with sample messages."""
    orchestrator = SupportOrchestrator()
    
    # Sample customer messages
    messages = [
        "I ordered product XYZ last week but haven't received it yet. My order ID is ORD-12345.",
        "There's a bug in your mobile app. It crashes every time I try to login.",
        "I'd like to return the item I purchased because it's not what I expected."
    ]
    
    print("Processing customer messages...")
    results = await orchestrator.process_concurrent_messages(messages)
    
    for i, result in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(f"Session ID: {result.get('session_id')}")
        print(f"Category: {result.get('category', 'N/A')}")
        print(f"Confidence: {result.get('confidence', 'N/A')}")
        print(f"Solution: {result.get('solution')}")
        if "error" in result:
            print(f"Error: {result['error']}")

if __name__ == "__main__":
    # Run the demo
    asyncio.run(demo())