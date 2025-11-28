"""
Parser Script
Parses Phone Number and Company Name columns from CSV files
"""

import argparse
import sys
import pandas as pd
from semantic_classifier import SemanticClassifier
from phone_parser import PhoneParser
from company_parser import CompanyParser


def main():
    parser = argparse.ArgumentParser(
        description='Parse Phone Number and Company Name columns from CSV file'
    )
    parser.add_argument(
        '--input',
        type=str,
        required=True,
        help='Path to the input CSV file'
    )
    
    args = parser.parse_args()
    
    try:
        # Read the CSV file
        df = pd.read_csv(args.input)
        
        if df.empty:
            print("Error: Input file is empty", file=sys.stderr)
            return 1
        
        # Initialize classifiers and parsers
        classifier = SemanticClassifier()
        phone_parser = PhoneParser()
        company_parser = CompanyParser()
        
        # Classify all columns
        classifications = classifier.classify_all_columns(df)
        
        # Find Phone Number and Company Name columns
        phone_columns = []
        company_columns = []
        
        for col, (classification, confidence) in classifications.items():
            if classification == 'Phone Number':
                phone_columns.append((col, confidence))
            elif classification == 'Company Name':
                company_columns.append((col, confidence))
        
        # Pick column with highest confidence if multiple matches
        phone_column = None
        company_column = None
        
        if phone_columns:
            phone_columns.sort(key=lambda x: x[1], reverse=True)
            phone_column = phone_columns[0][0]
        
        if company_columns:
            company_columns.sort(key=lambda x: x[1], reverse=True)
            company_column = company_columns[0][0]
        
        # Prepare output dataframe
        output_df = df.copy()
        
        # Parse Phone Number column
        if phone_column:
            phone_countries = []
            phone_numbers = []
            
            for phone in df[phone_column]:
                country, number = phone_parser.parse(phone)
                phone_countries.append(country)
                phone_numbers.append(number)
            
            # Rename the original column to PhoneNumber if needed
            if phone_column != 'PhoneNumber':
                output_df = output_df.rename(columns={phone_column: 'PhoneNumber'})
            
            # Add Country and Number columns
            output_df['Country'] = phone_countries
            output_df['Number'] = phone_numbers
        
        # Parse Company Name column
        if company_column:
            company_names = []
            company_legals = []
            
            for company in df[company_column]:
                name, legal = company_parser.parse(company)
                company_names.append(name)
                company_legals.append(legal)
            
            # Rename the original column to CompanyName if needed
            if company_column != 'CompanyName':
                output_df = output_df.rename(columns={company_column: 'CompanyName'})
            
            # Add Name and Legal columns
            output_df['Name'] = company_names
            output_df['Legal'] = company_legals
        
        # Reorder columns to put parsed fields first
        column_order = []
        
        if phone_column or 'PhoneNumber' in output_df.columns:
            column_order.extend(['PhoneNumber', 'Country', 'Number'])
        
        if company_column or 'CompanyName' in output_df.columns:
            column_order.extend(['CompanyName', 'Name', 'Legal'])
        
        # Keep other columns at the end
        for col in output_df.columns:
            if col not in column_order:
                column_order.append(col)
        
        output_df = output_df[column_order]
        
        # Write to output.csv
        output_df.to_csv('output.csv', index=False)
        
        print("Parsing completed. Output written to output.csv")
        return 0
        
    except FileNotFoundError:
        print(f"Error: File '{args.input}' not found", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

