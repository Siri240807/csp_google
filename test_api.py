#!/usr/bin/env python3
"""
Test script to verify Gemini API key and connection.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test the Gemini API connection."""
    print("Testing Gemini API connection...")
    
    # Get API key from environment
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key or api_key == "your_gemini_api_key_here" or api_key == "your_actual_gemini_api_key_here":
        print("ERROR: API key not found or still set to placeholder value")
        print("Please update your .env file with a valid Gemini API key")
        return False
        
    try:
        # Configure the API
        genai.configure(api_key=api_key)
        print("SUCCESS: Gemini API configured successfully")
        
        # Initialize the model with a known working model
        model = genai.GenerativeModel('models/gemini-pro-latest')
        print("SUCCESS: Initialized model models/gemini-pro-latest")
        
        # Test with a simple prompt
        print("Testing model response...")
        response = model.generate_content("Hello, this is a test. Please respond with 'Test successful'")
        print(f"Model response: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to connect to Gemini API: {e}")
        return False

if __name__ == "__main__":
    success = test_gemini_api()
    if success:
        print("\n✅ Gemini API is properly configured!")
        print("You can now run the main application.")
    else:
        print("\n❌ Gemini API configuration failed!")
        print("Please check your API key and try again.")