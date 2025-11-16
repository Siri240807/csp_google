"""
Resolver Agent for generating solutions using Gemini API.
"""

import os
import asyncio
from typing import Dict, Any
import google.generativeai as genai
from .base_agent import BaseAgent

class ResolverAgent(BaseAgent):
    """Agent responsible for generating solutions using Gemini API."""
    
    def __init__(self):
        super().__init__("ResolverAgent")
        self.model = None
        self.faq_memory = {}  # In a real implementation, this would connect to a database
        
        # Initialize Gemini API if API key is available
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('models/gemini-pro-latest')
            
    async def process(self, session_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a solution for the customer issue using Gemini.
        
        Args:
            session_state: Dictionary containing the current state of the session
            
        Returns:
            Updated session state with generated solution
        """
        self.log_activity("Starting solution generation")
        
        if not self.model:
            self.log_activity("Gemini API not configured, using fallback response", "warning")
            session_state["solution"] = "Thank you for contacting us. Our team will review your issue and respond shortly."
            return session_state
            
        # Build prompt based on session state
        prompt = self._build_prompt(session_state)
        
        try:
            # Generate response using Gemini
            response = await self._generate_response(prompt)
            session_state["solution"] = response
            self.log_activity("Solution generated successfully")
        except Exception as e:
            self.log_activity(f"Error generating solution: {str(e)}", "error")
            session_state["solution"] = "We apologize for the inconvenience. Our support team will contact you shortly."
            
        return session_state
        
    def _build_prompt(self, session_state: Dict[str, Any]) -> str:
        """
        Build a prompt for the Gemini model based on session state.
        
        Args:
            session_state: Current session state
            
        Returns:
            Formatted prompt for the model
        """
        # Extract relevant information
        customer_message = session_state.get("customer_message", "")
        category = session_state.get("issue_category", "general")
        order_ids = session_state.get("order_ids", [])
        product_names = session_state.get("product_names", [])
        problem_types = session_state.get("problem_types", [])
        
        # Build prompt
        prompt = f"""You are a customer support specialist for our company. Please provide a helpful and professional response to the customer's issue.

Customer Message: {customer_message}

Issue Details:
- Category: {category}
- Order IDs: {', '.join(order_ids) if order_ids else 'None'}
- Products: {', '.join(product_names) if product_names else 'None'}
- Problem Types: {', '.join(problem_types) if problem_types else 'None'}

Please provide a solution that:
1. Acknowledges the customer's concern
2. Provides specific steps to resolve the issue
3. Includes relevant policies or procedures
4. Offers additional assistance if needed

Response:"""
        
        return prompt
        
    async def _generate_response(self, prompt: str) -> str:
        """
        Generate a response using the Gemini model.
        
        Args:
            prompt: Prompt to send to the model
            
        Returns:
            Generated response
        """
        if not self.model:
            raise Exception("Gemini model not initialized")
            
        # In a real implementation, we would also retrieve relevant FAQs here
        # For now, we'll just generate a response
        response = await asyncio.get_event_loop().run_in_executor(
            None, lambda: self.model.generate_content(prompt)
        )
        
        return response.text
        
    def add_faq(self, question: str, answer: str):
        """
        Add an FAQ to the memory.
        
        Args:
            question: FAQ question
            answer: FAQ answer
        """
        self.faq_memory[question.lower()] = answer
        
    def get_relevant_faqs(self, keywords: list) -> dict:
        """
        Get relevant FAQs based on keywords.
        
        Args:
            keywords: List of keywords to search for
            
        Returns:
            Dictionary of relevant FAQs
        """
        relevant_faqs = {}
        keyword_set = set(k.lower() for k in keywords)
        
        for question, answer in self.faq_memory.items():
            # Simple keyword matching
            if any(keyword in question for keyword in keyword_set):
                relevant_faqs[question] = answer
                
        return relevant_faqs