"""
FAQ Memory for storing and retrieving frequently asked questions.
"""

import json
import os
from typing import Dict, List, Optional, Union
from datetime import datetime

class FAQMemory:
    """Manages storage and retrieval of frequently asked questions."""
    
    def __init__(self, storage_path: str = "faq_memory.json"):
        self.storage_path = storage_path
        self.faqs = {}
        self.last_updated = None
        self._load_from_storage()
        
    def _load_from_storage(self):
        """Load FAQs from persistent storage."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    self.faqs = data.get("faqs", {})
                    self.last_updated = data.get("last_updated")
            except Exception as e:
                print(f"Warning: Could not load FAQ memory from {self.storage_path}: {e}")
                self.faqs = {}
                
    def _save_to_storage(self):
        """Save FAQs to persistent storage."""
        try:
            data = {
                "faqs": self.faqs,
                "last_updated": datetime.now().isoformat()
            }
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save FAQ memory to {self.storage_path}: {e}")
            
    def add_faq(self, question: str, answer: str, category: str = "general") -> bool:
        """
        Add a new FAQ to memory.
        
        Args:
            question: The FAQ question
            answer: The FAQ answer
            category: Category for the FAQ
            
        Returns:
            True if successfully added, False otherwise
        """
        try:
            faq_id = str(hash(question))  # Simple ID generation
            self.faqs[faq_id] = {
                "question": question,
                "answer": answer,
                "category": category,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            self._save_to_storage()
            return True
        except Exception as e:
            print(f"Error adding FAQ: {e}")
            return False
            
    def get_faq(self, faq_id: str) -> Optional[Dict]:
        """
        Retrieve an FAQ by ID.
        
        Args:
            faq_id: The ID of the FAQ to retrieve
            
        Returns:
            FAQ dictionary if found, None otherwise
        """
        return self.faqs.get(faq_id)
        
    def search_faqs(self, keywords: List[str], category: Optional[str] = None) -> List[Dict]:
        """
        Search for FAQs containing specific keywords.
        
        Args:
            keywords: List of keywords to search for
            category: Optional category to filter by
            
        Returns:
            List of matching FAQs
        """
        results = []
        keyword_set = set(k.lower() for k in keywords)
        
        for faq_id, faq in self.faqs.items():
            # Check category filter
            if category and faq.get("category") != category:
                continue
                
            # Check keyword matches in question or answer
            question = faq.get("question", "").lower()
            answer = faq.get("answer", "").lower()
            
            if any(keyword in question or keyword in answer for keyword in keyword_set):
                results.append({**faq, "id": faq_id})
                
        return results
        
    def get_all_faqs(self) -> Dict:
        """
        Get all FAQs.
        
        Returns:
            Dictionary of all FAQs
        """
        return self.faqs.copy()
        
    def remove_faq(self, faq_id: str) -> bool:
        """
        Remove an FAQ from memory.
        
        Args:
            faq_id: The ID of the FAQ to remove
            
        Returns:
            True if successfully removed, False otherwise
        """
        if faq_id in self.faqs:
            del self.faqs[faq_id]
            self._save_to_storage()
            return True
        return False
        
    def update_faq(self, faq_id: str, question: Optional[str] = None, answer: Optional[str] = None, category: Optional[str] = None) -> bool:
        """
        Update an existing FAQ.
        
        Args:
            faq_id: The ID of the FAQ to update
            question: New question (optional)
            answer: New answer (optional)
            category: New category (optional)
            
        Returns:
            True if successfully updated, False otherwise
        """
        if faq_id not in self.faqs:
            return False
            
        faq = self.faqs[faq_id]
        if question:
            faq["question"] = question
        if answer:
            faq["answer"] = answer
        if category:
            faq["category"] = category
            
        faq["updated_at"] = datetime.now().isoformat()
        self._save_to_storage()
        return True