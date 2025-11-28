#!/usr/bin/env python3
"""
Script to create sample data files for testing
"""

import pandas as pd
import os

# Create data directory
os.makedirs('data', exist_ok=True)

# Sample phone numbers
phone_data = {
    'ph_nb': [
        '+91 6796233790',
        '+1 2312953582',
        '+44 2028323322',
        '4853859590',
        '+1 475-216-2114',
        '(080) 1234 5678',
        '+91 9876543210'
    ]
}
pd.DataFrame(phone_data).to_csv('data/phoneNumber.csv', index=False)

# Sample company names
company_data = {
    'CompanyName': [
        'Tresata pvt ltd.',
        'Enno Roggemann GmbH & Co. KG',
        'First National Bank',
        'Debrunner Acifer AG',
        'Microsoft Corporation',
        'Apple Inc.',
        'Google LLC'
    ]
}
pd.DataFrame(company_data).to_csv('data/Company.csv', index=False)

# Sample dates
date_data = {
    'Date': [
        '2024-01-15',
        '12/25/2023',
        '15-03-2024',
        'January 1, 2024',
        '2024/06/30',
        '03-15-2024'
    ]
}
pd.DataFrame(date_data).to_csv('data/Dates.csv', index=False)

# Countries reference file
countries = [
    'India',
    'United States',
    'United Kingdom',
    'Canada',
    'Australia',
    'Germany',
    'France',
    'China',
    'Japan',
    'Brazil',
    'Mexico',
    'Italy',
    'Spain',
    'Russia',
    'South Korea'
]
with open('Countries.txt', 'w') as f:
    for country in countries:
        f.write(country + '\n')

# Legal suffixes reference file
legal_suffixes = [
    'ltd',
    'limited',
    'inc',
    'incorporated',
    'corp',
    'corporation',
    'llc',
    'gmbh',
    'ag',
    'pvt',
    'private',
    'co',
    'kg',
    'plc',
    'sa',
    'nv',
    'bv'
]
with open('legal.txt', 'w') as f:
    for suffix in legal_suffixes:
        f.write(suffix + '\n')

print("Sample data files created successfully!")
print("- data/phoneNumber.csv")
print("- data/Company.csv")
print("- data/Dates.csv")
print("- Countries.txt")
print("- legal.txt")

