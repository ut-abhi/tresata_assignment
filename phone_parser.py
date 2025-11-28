"""
Phone Number Parser
"""

import phonenumbers
from phonenumbers import geocoder, carrier
import re
import pandas as pd
from typing import Tuple, Optional


class PhoneParser:
    """Parses phone numbers into country and number components"""
    
    # Country code to country name mapping
    COUNTRY_MAP = {
        'IN': 'India',
        'US': 'US',
        'GB': 'UK',
        'CA': 'Canada',
        'AU': 'Australia',
        'DE': 'Germany',
        'FR': 'France',
        'CN': 'China',
        'JP': 'Japan',
    }
    
    def parse(self, phone_str: str) -> Tuple[str, str]:
        """
        Parse phone number into (Country, Number)
        Returns (Country, Number) or ("", Number) if country cannot be determined
        """
        if not phone_str or pd.isna(phone_str):
            return "", ""
        
        phone_str = str(phone_str).strip()
        if not phone_str:
            return "", ""
        
        try:
            # Try to parse with phonenumbers library
            # First try with no default region
            parsed = phonenumbers.parse(phone_str, None)
            
            if phonenumbers.is_valid_number(parsed):
                country_code = phonenumbers.region_code_for_number(parsed)
                country = self.COUNTRY_MAP.get(country_code, country_code)
                
                # Get national number (without country code)
                national_number = str(parsed.national_number)
                
                return country, national_number
        except:
            pass
        
        # Fallback parsing
        try:
            # Try with different default regions
            for default_region in ['US', 'IN', 'GB']:
                try:
                    parsed = phonenumbers.parse(phone_str, default_region)
                    if phonenumbers.is_valid_number(parsed):
                        country_code = phonenumbers.region_code_for_number(parsed)
                        country = self.COUNTRY_MAP.get(country_code, country_code)
                        national_number = str(parsed.national_number)
                        return country, national_number
                except:
                    continue
        except:
            pass
        
        # Manual parsing fallback
        cleaned = re.sub(r'[\s\-\(\)\.]', '', phone_str)
        
        # Check for country codes
        if cleaned.startswith('91') and len(cleaned) >= 10:
            return "India", cleaned[2:]
        elif cleaned.startswith('1') and len(cleaned) == 11:
            return "US", cleaned[1:]
        elif cleaned.startswith('44') and len(cleaned) >= 10:
            return "UK", cleaned[2:]
        
        # If no country code detected, return empty country
        return "", cleaned

