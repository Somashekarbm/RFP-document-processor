# README: Extracting Structured Data from RFP Documents

## Overview
This Python script processes Request for Proposal (RFP) documents in HTML and PDF formats, extracting structured information such as bid numbers, titles, due dates, and more. The extracted information is saved as JSON files, either individually for each file or combined for each folder.

---

## Features
- Supports processing of files in two folders: `bid1` and `bid2`.
- Extracts predefined fields from RFP documents using OpenAI's GPT-based model.
- Supports two output modes:
  1. Individual JSON files for each document.
  2. Combined JSON files for all documents in a folder.
- Processes `.html`, `.htm`, and `.pdf` files.

---

## Prerequisites
1. **Python 3.7 or later**: Ensure Python is installed on your machine.
2. **Required Libraries**: Install the necessary libraries using pip:
   ```bash
   pip install openai beautifulsoup4 pdfminer.six python-dotenv
   ```
3. **OpenAI API Key**: 
   - Obtain an API key from [OpenAI](https://platform.openai.com/).
   - Create a `.env` file in the project directory and add your API key:
     ```bash
     OPENAI_API_KEY=your_api_key_here
     ```

---

## Installation
1. Copy and paste the main.py file.
2. Ensure the project directory contains the `.env` file with your OpenAI API key.
3. Place the RFP documents in the `bid1` and `bid2` folders.

---

## Usage
### Basic Command
Run the script with the following command:
```bash
python main.py <output_dir>
```
- `<output_dir>`: The directory where the output JSON files will be saved.

### Combine Outputs
To combine all processed files from a folder into a single JSON file, use the `--combine` flag:
```bash
python main.py <output_dir> --combine
```

### Example
#### Without Combining:
```bash
python main.py output
```
- Outputs individual JSON files for each document in `output/`.

#### With Combining:
```bash
python main.py output --combine
```
- Outputs:
  - `output/bid1_processed.json`: Combined JSON for all files in `bid1/`.
  - `output/bid2_processed.json`: Combined JSON for all files in `bid2/`.

---

## Input Folders
The script expects the following folder structure:
```
.
├── bid1/
│   ├── file1.html
│   ├── file2.pdf
│   └── ...
├── bid2/
│   ├── file3.html
│   ├── file4.pdf
│   └── ...
├── main.py
└── .env
```

---

## Output
1. **Individual Outputs**:
   - Files from `bid1/` are saved as `output/file1.json`, `output/file2.json`, etc.
   - Files from `bid2/` are saved similarly.

2. **Combined Outputs (with `--combine`)**:
   - All files from `bid1/` are saved in `output/bid1_processed.json`.
   - All files from `bid2/` are saved in `output/bid2_processed.json`.

---

## Extracted Fields
The following fields are extracted from each document and saved in the JSON output:
- **Bid Number**
- **Title**
- **Due Date**
- **Bid Submission Type**
- **Term of Bid**
- **Pre-Bid Meeting**
- **Installation Requirements**
- **Bid Bond Requirement**
- **Delivery Date**
- **Payment Terms**
- **Additional Documentation Required**
- **MFG for Registration**
- **Contract or Cooperative to Use**
- **Model Number**
- **Part Number**
- **Product Description**
- **Contact Information**
- **Company Name**
- **Bid Summary**
- **Product Specifications**

---

## Debugging
1. **Unsupported File Format**:
   Ensure the files are in `.html`, `.htm`, or `.pdf` format.
2. **Environment Variables**:
   Verify the `.env` file contains a valid OpenAI API key.
3. **Dependencies**:
   Ensure all required libraries are installed.

---
# RFP-document-processor
