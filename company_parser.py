"""
Company Name Parser Module
Parses company names into Name and Legal fields
"""

import re
from typing import Tuple
import pandas as pd


class CompanyParser:
    """Parses company names into name and legal suffix components"""
    
    def __init__(self):
        self.legal_suffixes = set()
        self.load_legal_suffixes()
    
    def load_legal_suffixes(self):
        """Load legal suffixes from file"""
        try:
            with open('legal.txt', 'r', encoding='utf-8') as f:
                self.legal_suffixes = {line.strip().lower() for line in f if line.strip()}
        except FileNotFoundError:
            # Default legal suffixes
            self.legal_suffixes = {
                'ltd', 'limited', 'inc', 'incorporated', 'corp', 'corporation',
                'llc', 'gmbh', 'ag', 'pvt', 'private', 'co', 'kg', 'plc',
                'sa', 'nv', 'bv', 'oy', 'ab', 'as', 'spa', 'srl', 'sl', 'slu'
            }
    
    def parse(self, company_name: str) -> Tuple[str, str]:
        """
        Parse company name into (Name, Legal)
        Returns (name in lowercase, legal suffix in lowercase)
        """
        if not company_name or pd.isna(company_name):
            return "", ""
        
        company_name = str(company_name).strip()
        if not company_name:
            return "", ""
        
        # Split into words
        words = company_name.split()
        
        # Find legal suffix at the end
        legal_parts = []
        name_parts = []
        
        # Check from the end backwards
        found_legal = False
        for i in range(len(words) - 1, -1, -1):
            word = words[i].lower().rstrip('.,;:')
            if not found_legal and word in self.legal_suffixes:
                legal_parts.insert(0, word)
                found_legal = True
            elif found_legal:
                # Continue collecting legal parts (e.g., "GmbH & Co. KG")
                if word in self.legal_suffixes or word in ['&', 'and']:
                    legal_parts.insert(0, word)
                else:
                    name_parts.insert(0, words[i])
                    break
            else:
                name_parts.insert(0, words[i])
        
        # Join the parts
        name = ' '.join(name_parts).strip().lower()
        legal = ' '.join(legal_parts).strip().lower()
        
        # If no legal suffix found, the entire name is the name
        if not legal:
            name = company_name.lower()
        
        return name, legal

