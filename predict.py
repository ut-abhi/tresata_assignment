"""
Semantic Classification Script
Classifies a column in a CSV file into semantic types:
Phone Number, Company Name, Country, Date, Other
"""

import argparse
import sys
import pandas as pd
from semantic_classifier import SemanticClassifier


def main():
    parser = argparse.ArgumentParser(
        description='Classify semantic type of a column in a CSV file'
    )
    parser.add_argument(
        '--input',
        type=str,
        required=True,
        help='Path to the input CSV file'
    )
    parser.add_argument(
        '--column',
        type=str,
        required=True,
        help='Name of the column to classify'
    )
    
    args = parser.parse_args()
    
    try:
        # Read the CSV file
        df = pd.read_csv(args.input)
        
        # Initialize classifier
        classifier = SemanticClassifier()
        
        # Classify the column
        classification, confidence = classifier.classify_column(df, args.column)
        
        # Convert to lowercase format as required
        output = classification.lower().replace(' ', '')
        print(output)
        
        return 0
        
    except FileNotFoundError:
        print(f"Error: File '{args.input}' not found", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())

