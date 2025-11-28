"""
Semantic Classification Module
Classifies columns into: Phone Number, Company Name, Country, Date, Other
"""

import pandas as pd
import numpy as np
import re
from typing import Dict, List, Tuple
import phonenumbers
from dateutil import parser as date_parser
from datetime import datetime


class SemanticClassifier:
    """Classifies column data into semantic types"""
    
    def __init__(self):
        self.countries = set()
        self.legal_suffixes = set()
        self.load_reference_data()
    
    def load_reference_data(self):
        """Load reference data for classification"""
        try:
            # Load countries
            with open('Countries.txt', 'r', encoding='utf-8') as f:
                self.countries = {line.strip().lower() for line in f if line.strip()}
        except FileNotFoundError:
            print("Warning: Countries.txt not found, using default country list")
            self.countries = {'india', 'usa', 'united states', 'uk', 'united kingdom', 
                            'china', 'japan', 'germany', 'france', 'canada', 'australia'}
        
        try:
            # Load legal suffixes
            with open('legal.txt', 'r', encoding='utf-8') as f:
                self.legal_suffixes = {line.strip().lower() for line in f if line.strip()}
        except FileNotFoundError:
            print("Warning: legal.txt not found, using default legal suffixes")
            self.legal_suffixes = {'ltd', 'limited', 'inc', 'incorporated', 'corp', 'corporation',
                                 'llc', 'gmbh', 'ag', 'pvt', 'private', 'co', 'kg', 'plc'}
    
    def is_phone_number(self, value: str) -> bool:
        """Check if a value is a phone number"""
        if pd.isna(value) or not isinstance(value, str):
            return False
        
        value = value.strip()
        if not value:
            return False
        
        # Remove common separators
        cleaned = re.sub(r'[\s\-\(\)\.]', '', value)
        
        # Check if it starts with + or has country code pattern
        if re.match(r'^\+?\d{7,15}$', cleaned):
            try:
                # Try parsing with phonenumbers library
                parsed = phonenumbers.parse(value, None)
                return phonenumbers.is_valid_number(parsed)
            except:
                # Fallback: check if it looks like a phone number
                return len(cleaned) >= 7 and len(cleaned) <= 15 and cleaned.isdigit()
        
        return False
    
    def is_date(self, value: str) -> bool:
        """Check if a value is a date"""
        if pd.isna(value) or not isinstance(value, str):
            return False
        
        value = str(value).strip()
        if not value:
            return False
        
        # Common date patterns
        date_patterns = [
            r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
            r'^\d{2}/\d{2}/\d{4}$',  # MM/DD/YYYY
            r'^\d{2}-\d{2}-\d{4}$',  # MM-DD-YYYY
            r'^\d{4}/\d{2}/\d{2}$',  # YYYY/MM/DD
            r'^\d{1,2}\s+\w+\s+\d{4}$',  # DD Month YYYY
        ]
        
        for pattern in date_patterns:
            if re.match(pattern, value):
                try:
                    date_parser.parse(value, fuzzy=False)
                    return True
                except:
                    pass
        
        # Try fuzzy parsing
        try:
            date_parser.parse(value, fuzzy=True)
            return True
        except:
            pass
        
        return False
    
    def is_country(self, value: str) -> bool:
        """Check if a value is a country name"""
        if pd.isna(value) or not isinstance(value, str):
            return False
        
        value = value.strip().lower()
        return value in self.countries
    
    def is_company_name(self, value: str) -> bool:
        """Check if a value is a company name"""
        if pd.isna(value) or not isinstance(value, str):
            return False
        
        value = str(value).strip()
        if not value or len(value) < 2:
            return False
        
        # Check for legal suffixes
        words = value.lower().split()
        for word in words:
            if word in self.legal_suffixes:
                return True
        
        # Check if it contains common company indicators
        company_indicators = ['bank', 'corp', 'inc', 'ltd', 'llc', 'gmbh', 'ag', 'co']
        value_lower = value.lower()
        for indicator in company_indicators:
            if indicator in value_lower:
                return True
        
        # Heuristic: if it's a proper noun (starts with capital) and not a date/phone
        if value[0].isupper() and not self.is_date(value) and not self.is_phone_number(value):
            # Check if it's not a country
            if not self.is_country(value):
                return True
        
        return False
    
    def classify_column(self, df: pd.DataFrame, column_name: str) -> Tuple[str, float]:
        """
        Classify a column and return (classification, confidence)
        """
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in dataframe")
        
        column_data = df[column_name].dropna()
        if len(column_data) == 0:
            return "Other", 0.0
        
        # Sample up to 1000 rows for efficiency
        sample_size = min(1000, len(column_data))
        sample = column_data.sample(n=sample_size, random_state=42) if len(column_data) > sample_size else column_data
        
        scores = {
            'Phone Number': 0.0,
            'Company Name': 0.0,
            'Country': 0.0,
            'Date': 0.0,
            'Other': 0.0
        }
        
        total = len(sample)
        if total == 0:
            return "Other", 0.0
        
        for value in sample:
            if self.is_phone_number(str(value)):
                scores['Phone Number'] += 1
            elif self.is_date(str(value)):
                scores['Date'] += 1
            elif self.is_country(str(value)):
                scores['Country'] += 1
            elif self.is_company_name(str(value)):
                scores['Company Name'] += 1
            else:
                scores['Other'] += 1
        
        # Calculate probabilities
        probabilities = {k: v / total for k, v in scores.items()}
        
        # Get the classification with highest probability
        classification = max(probabilities, key=probabilities.get)
        confidence = probabilities[classification]
        
        return classification, confidence
    
    def classify_all_columns(self, df: pd.DataFrame) -> Dict[str, Tuple[str, float]]:
        """Classify all columns in the dataframe"""
        results = {}
        for col in df.columns:
            classification, confidence = self.classify_column(df, col)
            results[col] = (classification, confidence)
        return results

