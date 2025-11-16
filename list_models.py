#!/usr/bin/env python3
"""
Script to list available Gemini models.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def list_gemini_models():
    """List available Gemini models."""
    print("Listing available Gemini models...")
    
    # Get API key from environment
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key or api_key == "your_gemini_api_key_here" or api_key == "your_actual_gemini_api_key_here":
        print("ERROR: API key not found or still set to placeholder value")
        print("Please update your .env file with a valid Gemini API key")
        return
        
    try:
        # Configure the API
        genai.configure(api_key=api_key)
        
        # List models
        print("\\nAvailable models for generateContent:")
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"  - {model.name}")
                
        print("\\nAll available models:")
        for model in genai.list_models():
            print(f"  - {model.name}: {model.supported_generation_methods}")
        
    except Exception as e:
        print(f"ERROR: Failed to list models: {e}")

if __name__ == "__main__":
    list_gemini_models()