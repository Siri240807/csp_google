#!/usr/bin/env python3
"""
Comprehensive test suite for the AI Customer Issue Analyzer system.
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator import SupportOrchestrator
from agents.classifier_agent import ClassifierAgent
from agents.analyzer_agent import AnalyzerAgent
from agents.resolver_agent import ResolverAgent
from agents.logger_agent import LoggerAgent
from utils.session_manager import SessionManager
from memory.faq_memory import FAQMemory
from database.connector import DatabaseConnector

# Load environment variables
load_dotenv()

def test_agent_instantiation():
    """Test that all agents can be instantiated."""
    print("Testing agent instantiation...")
    
    try:
        classifier = ClassifierAgent()
        analyzer = AnalyzerAgent()
        resolver = ResolverAgent()
        logger = LoggerAgent()
        print("✅ All agents instantiated successfully")
        return True
    except Exception as e:
        print(f"❌ Error instantiating agents: {e}")
        return False

def test_session_manager():
    """Test session manager functionality."""
    print("Testing session manager...")
    
    try:
        session = SessionManager("test-session-123")
        session.update_state({"customer_message": "Test message"})
        
        state = session.get_state()
        assert state["session_id"] == "test-session-123"
        assert state["customer_message"] == "Test message"
        print("✅ Session manager working correctly")
        return True
    except Exception as e:
        print(f"❌ Error with session manager: {e}")
        return False

def test_faq_memory():
    """Test FAQ memory functionality."""
    print("Testing FAQ memory...")
    
    try:
        faq_memory = FAQMemory("test_faq_memory.json")
        faq_memory.add_faq("Test question", "Test answer", "test")
        
        results = faq_memory.search_faqs(["test"])
        assert len(results) > 0
        print("✅ FAQ memory working correctly")
        return True
    except Exception as e:
        print(f"❌ Error with FAQ memory: {e}")
        return False

def test_database_connector():
    """Test database connector functionality."""
    print("Testing database connector...")
    
    try:
        db = DatabaseConnector(db_type="csv", file_path="test_interactions.csv")
        
        # Test logging
        test_data = {
            "session_id": "test-session-456",
            "customer_message": "Test database message",
            "issue_category": "test",
            "order_ids": ["TEST-123"],
            "product_names": ["Test Product"],
            "problem_types": ["test_issue"],
            "solution": "Test solution",
            "classification_confidence": 0.95
        }
        
        success = db.log_interaction(test_data)
        assert success
        print("✅ Database connector working correctly")
        return True
    except Exception as e:
        print(f"❌ Error with database connector: {e}")
        return False

async def test_full_system():
    """Test the full system with a sample message."""
    print("Testing full system...")
    
    try:
        orchestrator = SupportOrchestrator()
        
        test_message = "I ordered product XYZ last week but haven't received it yet. My order ID is ORD-12345."
        result = await orchestrator.process_customer_message(test_message)
        
        assert "session_id" in result
        assert "solution" in result
        assert "category" in result
        assert "confidence" in result
        
        print(f"✅ Full system test passed")
        print(f"   Category: {result['category']}")
        print(f"   Confidence: {result['confidence']}")
        print(f"   Session ID: {result['session_id']}")
        return True
    except Exception as e:
        print(f"❌ Error with full system test: {e}")
        return False

def cleanup_test_files():
    """Clean up test files."""
    test_files = ["test_faq_memory.json", "test_interactions.csv"]
    for file in test_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"Cleaned up {file}")
            except Exception as e:
                print(f"Error cleaning up {file}: {e}")

def main():
    """Run all tests."""
    print("Running comprehensive system tests...\n")
    
    tests = [
        test_agent_instantiation,
        test_session_manager,
        test_faq_memory,
        test_database_connector,
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    # Run async test
    async_result = asyncio.run(test_full_system())
    results.append(async_result)
    print()
    
    # Clean up
    cleanup_test_files()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)