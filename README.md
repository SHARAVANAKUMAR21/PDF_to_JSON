# PDF to JSON Converter

This Python application reads a PDF file, extracts structured data from it, and converts this data into a JSON format using Pydantic models for data validation and serialization.

## Description

The PDF to JSON Converter is designed to streamline the process of extracting data from PDF files and converting it into a structured JSON format. This tool can handle various types of data within a PDF, including tables, text blocks, and images. By leveraging the power of `pdfplumber` for PDF manipulation and `pydantic` for data validation and serialization, this application ensures that the extracted data is accurate and well-structured.

This tool is particularly useful for scenarios where automated data extraction and transformation are required, such as data analysis, reporting, and integration with other systems.


## Features

- **PDF Reading**: Reads a PDF file using `pdfplumber`.
- **Data Extraction**: Extracts tables, text blocks, and images from the PDF.
- **Data Validation and Serialization**: Utilizes Pydantic models to define the schema for the extracted data and serialize it to JSON format.
- **Output**: Generates a JSON file containing the structured data extracted from the PDF.

## Requirements
- `create a venv` 
- `Python` 3.12.4 (3.7 + any will work) 
- `pdfplumber` library
- `pydantic` library

## Setup

### Step 1: Clone the Repository

First, clone the repository to your local machine using the following command:

```bash
https://github.com/SHARAVANAKUMAR21/PDF_to_JSON.git
cd PDF_to_JSON
