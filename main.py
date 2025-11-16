#!/usr/bin/env python3
"""
AI Customer Issue Analyzer + Auto-Resolution Agent
Enterprise-grade multi-agent system for automated customer support.
"""

import os
import sys
import asyncio
from dotenv import load_dotenv
from orchestrator import SupportOrchestrator

# Load environment variables
load_dotenv()

def main():
    """Main entry point for the AI Customer Issue Analyzer system."""
    print("AI Customer Issue Analyzer + Auto-Resolution Agent")
    print("=" * 50)
    
    # Check if required environment variables are set
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        print("Warning: GEMINI_API_KEY not found in environment variables")
        print("Please set your Gemini API key in the .env file")
    
    # Run the demo
    asyncio.run(run_demo())
    
async def run_demo():
    """Run a demo of the multi-agent system."""
    orchestrator = SupportOrchestrator()
    
    # Sample customer message
    customer_message = "I ordered product XYZ last week but haven't received it yet. My order ID is ORD-12345."
    
    print(f"\nProcessing customer message: {customer_message}")
    result = await orchestrator.process_customer_message(customer_message)
    
    print(f"\nSession ID: {result.get('session_id')}")
    print(f"Category: {result.get('category')}")
    print(f"Confidence: {result.get('confidence')}")
    print(f"Solution: {result.get('solution')}")
    
    if "error" in result:
        print(f"Error: {result['error']}")

if __name__ == "__main__":
    main()