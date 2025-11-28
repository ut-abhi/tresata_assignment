"""
MCP (Model Context Protocol) Server
Acts as a connector for LLMs (ChatGPT, Claude, etc.)
Provides tools for column prediction and parsing
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import pandas as pd
from semantic_classifier import SemanticClassifier
from phone_parser import PhoneParser
from company_parser import CompanyParser


class MCPServer:
    """MCP Server for semantic classification and parsing"""
    
    def __init__(self, data_directory: str = "data"):
        self.data_directory = Path(data_directory)
        self.data_directory.mkdir(exist_ok=True)
        self.classifier = SemanticClassifier()
        self.phone_parser = PhoneParser()
        self.company_parser = CompanyParser()
    
    def list_files(self) -> List[str]:
        """List all available CSV files in the data directory"""
        files = []
        if self.data_directory.exists():
            for file_path in self.data_directory.glob("*.csv"):
                files.append(str(file_path))
        return files
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools"""
        return [
            {
                "name": "column_prediction",
                "description": "Classify the semantic type of a column in a CSV file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the CSV file"
                        },
                        "column_name": {
                            "type": "string",
                            "description": "Name of the column to classify"
                        }
                    },
                    "required": ["file_path", "column_name"]
                }
            },
            {
                "name": "parser",
                "description": "Parse Phone Number and Company Name columns from a CSV file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the input CSV file"
                        }
                    },
                    "required": ["file_path"]
                }
            }
        ]
    
    def column_prediction(self, file_path: str, column_name: str) -> Dict[str, Any]:
        """Classify a column's semantic type"""
        try:
            df = pd.read_csv(file_path)
            classification, confidence = self.classifier.classify_column(df, column_name)
            
            return {
                "success": True,
                "classification": classification,
                "confidence": confidence,
                "column": column_name,
                "file": file_path
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def parser(self, file_path: str) -> Dict[str, Any]:
        """Parse Phone Number and Company Name columns"""
        try:
            df = pd.read_csv(file_path)
            
            if df.empty:
                return {
                    "success": False,
                    "error": "Input file is empty"
                }
            
            # Classify all columns
            classifications = self.classifier.classify_all_columns(df)
            
            # Find Phone Number and Company Name columns
            phone_columns = []
            company_columns = []
            
            for col, (classification, confidence) in classifications.items():
                if classification == 'Phone Number':
                    phone_columns.append((col, confidence))
                elif classification == 'Company Name':
                    company_columns.append((col, confidence))
            
            # Select columns with highest confidence
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
                    country, number = self.phone_parser.parse(phone)
                    phone_countries.append(country)
                    phone_numbers.append(number)
                
                if phone_column != 'PhoneNumber':
                    output_df = output_df.rename(columns={phone_column: 'PhoneNumber'})
                
                output_df['Country'] = phone_countries
                output_df['Number'] = phone_numbers
            
            # Parse Company Name column
            if company_column:
                company_names = []
                company_legals = []
                
                for company in df[company_column]:
                    name, legal = self.company_parser.parse(company)
                    company_names.append(name)
                    company_legals.append(legal)
                
                if company_column != 'CompanyName':
                    output_df = output_df.rename(columns={company_column: 'CompanyName'})
                
                output_df['Name'] = company_names
                output_df['Legal'] = company_legals
            
            # Reorder columns
            column_order = []
            
            if phone_column or 'PhoneNumber' in output_df.columns:
                column_order.extend(['PhoneNumber', 'Country', 'Number'])
            
            if company_column or 'CompanyName' in output_df.columns:
                column_order.extend(['CompanyName', 'Name', 'Legal'])
            
            for col in output_df.columns:
                if col not in column_order:
                    column_order.append(col)
            
            output_df = output_df[column_order]
            
            # Write to output.csv
            output_path = Path(file_path).parent / 'output.csv'
            output_df.to_csv(output_path, index=False)
            
            return {
                "success": True,
                "output_file": str(output_path),
                "phone_column": phone_column,
                "company_column": company_column,
                "rows_processed": len(output_df)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """Process a file: first prediction, then parsing"""
        results = {
            "file": file_path,
            "predictions": {},
            "parsing": None
        }
        
        try:
            df = pd.read_csv(file_path)
            
            # Step 1: Predict all columns
            classifications = self.classifier.classify_all_columns(df)
            results["predictions"] = {
                col: {
                    "classification": cls,
                    "confidence": conf
                }
                for col, (cls, conf) in classifications.items()
            }
            
            # Step 2: Parse the file
            parsing_result = self.parser(file_path)
            results["parsing"] = parsing_result
            
            return results
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# FastAPI-based MCP server for HTTP access
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="MCP Server for Semantic Classification")

mcp_server = MCPServer()


class PredictionRequest(BaseModel):
    file_path: str
    column_name: str


class ParserRequest(BaseModel):
    file_path: str


@app.get("/tools")
async def list_tools():
    """List available tools"""
    return {"tools": mcp_server.list_tools()}


@app.get("/files")
async def list_files():
    """List available files"""
    return {"files": mcp_server.list_files()}


@app.post("/tools/column_prediction")
async def column_prediction(request: PredictionRequest):
    """Classify a column"""
    result = mcp_server.column_prediction(request.file_path, request.column_name)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Unknown error"))
    return result


@app.post("/tools/parser")
async def parser(request: ParserRequest):
    """Parse a file"""
    result = mcp_server.parser(request.file_path)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Unknown error"))
    return result


@app.post("/process")
async def process_file(request: ParserRequest):
    """Process a file (prediction + parsing)"""
    result = mcp_server.process_file(request.file_path)
    if not result.get("success", True):
        raise HTTPException(status_code=400, detail=result.get("error", "Unknown error"))
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

