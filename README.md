# Semantic Data Classification and Parsing System

## Overview

A system for classifying and parsing data columns into semantic types (Phone Number, Company Name, Country, Date, Other) and extracting structured information.

## Quick Start

### Installation
```bash
pip install -r requirements.txt
python create_sample_data.py
```

### Usage

**Part A: Classification**
```bash
python predict.py --input data/phoneNumber.csv --column ph_nb
# Output: phonenumber
```

**Part B: Parsing**
```bash
python parser.py --input data/phoneNumber.csv
# Creates output.csv with parsed fields
```

### Test Everything
```bash
python test_assignment.py
```

## Project Structure

```
├── predict.py                 # Part A: Classification script
├── parser.py                   # Part B: Parsing script
├── semantic_classifier.py     # Classification logic
├── phone_parser.py            # Phone number parsing
├── company_parser.py          # Company name parsing
├── mcp_server.py             # Part C: MCP server (optional)
├── requirements.txt          # Dependencies
├── Countries.txt             # Country reference data
└── legal.txt                 # Legal suffix reference data
```

## How It Works

### Classification (Part A)
- Analyzes column values using pattern matching
- Uses regex, phonenumbers library, and reference data
- Returns classification: phonenumber, companyname, country, date, or other

### Parsing (Part B)
- Automatically identifies Phone/Company columns
- Selects column with highest classification confidence
- Parses Phone Numbers → Country + Number
- Parses Company Names → Name + Legal
- Outputs to output.csv

### MCP Server (Part C)
- REST API for LLM integration
- Endpoints: /tools, /files, /tools/column_prediction, /tools/parser, /process
- Run: `python mcp_server.py`

## Example Outputs

**Classification:**
```
Input: python predict.py --input data/phoneNumber.csv --column ph_nb
Output: phonenumber
```

**Phone Parsing:**
```
Input: +91 6796233790
Output: Country: India, Number: 6796233790
```

**Company Parsing:**
```
Input: Tresata pvt ltd.
Output: Name: tresata, Legal: pvt ltd
```

## Requirements

- Python 3.8+
- pandas, numpy, phonenumbers, python-dateutil
- fastapi, uvicorn (for MCP server)

See requirements.txt for full list.

## Files

- `predict.py` - Classification script (Part A)
- `parser.py` - Parsing script (Part B)
- `mcp_server.py` - MCP server (Part C)
- `test_assignment.py` - Test script to verify everything works
- `DEMO_VIDEO_GUIDE.md` - Guide for 2-minute demo video
- `HOW_TO_RUN.txt` - Simple instructions

## Testing

Run the test script to verify all functionality:
```bash
python test_assignment.py
```

This will test both classification and parsing, and show expected outputs.
