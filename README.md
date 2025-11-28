# Semantic Data Classification and Parsing System

## Demo Video

https://drive.google.com/drive/folders/1iuhFI2spoDZgNOpjtYP6i5sNKZ6cIrqP?usp=sharing

---

## About

This project implements a system for automatically classifying and parsing data columns. It can identify semantic types (phone numbers, company names, countries, dates) and extract structured information from them.

## Installation

Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Part A: Classification

Classify a column in a CSV file:
```bash
python predict.py --input TrainingData/phone.csv --column number
```

This will output: `phonenumber`, `companyname`, `country`, `date`, or `other`

### Part B: Parsing

Parse phone numbers and company names:
```bash
python parser.py --input TrainingData/phone.csv
```

This creates `output.csv` with parsed fields:
- Phone numbers → Country and Number columns
- Company names → Name and Legal columns

### Part C: MCP Server

Start the MCP server for LLM integration:
```bash
python mcp_server.py
```

The server runs on `http://localhost:8000` and provides REST API endpoints:
- `GET /tools` - List available tools (column_prediction, parser)
- `GET /files` - List available CSV files
- `POST /tools/column_prediction` - Classify a column
- `POST /tools/parser` - Parse a file
- `POST /process` - Complete workflow (prediction + parsing)

## Project Files

- `predict.py` - Classification script (Part A)
- `parser.py` - Parsing script (Part B)
- `semantic_classifier.py` - Core classification logic
- `phone_parser.py` - Phone number parsing
- `company_parser.py` - Company name parsing
- `mcp_server.py` - MCP server for LLM integration (Part C)
- `TrainingData/` - Training and reference data folder

## How It Works

The system uses pattern matching to classify columns:
- Phone numbers: Detects using regex and phonenumbers library
- Company names: Identifies legal suffixes (Ltd, Inc, GmbH, etc.)
- Countries: Matches against reference list
- Dates: Recognizes various date formats

For parsing, it automatically finds the relevant columns and extracts structured information.

The MCP server provides a REST API interface, allowing LLMs (ChatGPT, Claude, etc.) to interact with the classification and parsing tools programmatically.

## Examples

**Classify phone column:**
```bash
python predict.py --input TrainingData/phone.csv --column number
# Output: phonenumber
```

**Parse phone numbers:**
```bash
python parser.py --input TrainingData/phone.csv
# Creates output.csv with PhoneNumber, Country, Number
```

**MCP Server:**
```bash
# Start server
python mcp_server.py

# In another terminal, test the API
curl http://localhost:8000/tools
curl -X POST http://localhost:8000/tools/column_prediction -H "Content-Type: application/json" -d "{\"file_path\": \"TrainingData/phone.csv\", \"column_name\": \"number\"}"
```

## Requirements

- Python 3.8+
- pandas, numpy, phonenumbers, python-dateutil
- fastapi, uvicorn (for MCP server)

## Training Data

The `TrainingData/` folder contains reference files and sample data used by the system.
