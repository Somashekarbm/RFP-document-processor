import os
import json
import argparse
import openai
from openai import OpenAI
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key not found. Ensure it is set in the .env file.")

SUPPORTED_EXTENSIONS = ['.html', '.htm', '.pdf']

# Initialize OpenAI client
client = OpenAI(
    api_key=openai.api_key
)

def parse_html(file_path):
    """
    Extracts text content from an HTML file.

    Args:
        file_path (str): Path to the HTML file.

    Returns:
        str: Extracted text content.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        text = soup.get_text(separator='\n')
    return text

def parse_pdf(file_path):
    """
    Extracts text content from a PDF file.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        str: Extracted text content.
    """
    text = extract_text(file_path)
    return text

def extract_information(text):
    """
    Extracts structured information from the given text using OpenAI API.

    Args:
        text (str): The input text content.

    Returns:
        dict: Extracted information in JSON format.
    """
    prompt = f"""
            You are a highly skilled assistant specializing in extracting and organizing data from Request for Proposal (RFP) documents.

            Please extract the following details from the provided text and return them in JSON format:
            - Bid Number: Unique identifier of the bid like the solication number or the PORFP number.
            - Title: The title or subject of the RFP.
            - Due Date: The deadline for submission or the proposal due date.
            - Bid Submission Type: The type of submission (e.g., online, in-person).
            - Term of Bid: The duration for which the bid is valid or applicable.
            - Pre-Bid Meeting: Details about any scheduled pre-bid meetings, if applicable.
            - Installation Requirements: Any requirements related to the installation of products/services.
            - Bid Bond Requirement: Any bond requirements associated with the bid.
            - Delivery Date: Expected delivery date for products or services.
            - Payment Terms: Details about payment terms or schedules.
            - Additional Documentation Required: List of additional documents required for submission.
            - MFG for Registration: Manufacturer details for registration, if applicable.
            - Contract or Cooperative to Use: Applicable contracts or cooperatives.
            - Model Number: Model numbers of products mentioned in the RFP.
            - Part Number: Part numbers of products mentioned in the RFP.
            - Product Description: Description of the product(s) or service(s).
            - Contact Information: Contact details for inquiries about the RFP like the mail ,phone number, POC details or any other details specified in the RFP documents.
            - Company Name: The company or organization issuing the RFP.
            - Bid Summary: A concise summary of the bid.
            - Product Specifications: Detailed specifications of the products.

            Text: {text}
            
            Use the following format for your JSON output:
            {{
                "Bid Number": "",
                "Title": "",
                "Due Date": "",
                "Bid Submission Type": "",
                "Term of Bid": "",
                "Pre-Bid Meeting": "",
                "Installation Requirements": "",
                "Bid Bond Requirement": "",
                "Delivery Date": "",
                "Payment Terms": "",
                "Additional Documentation Required": "",
                "MFG for Registration": "",
                "Contract or Cooperative to Use": "",
                "Model Number": "",
                "Part Number": "",
                "Product Description": "",
                "Contact Information": "",
                "Company Name": "",
                "Bid Summary": "",
                "Product Specifications": ""
            }}
            

            Ensure the response is strictly in JSON format without any extra text or commentary.
            """
    try:
        response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    model="gpt-4o-mini",
                    temperature=0.3,
                    max_tokens=2000,
                    response_format= { "type":"json_object" }
                )
        response_message = response.choices[0].message.content.strip()
        extracted_info = json.loads(response_message)
    except json.JSONDecodeError:
        print("Failed to parse JSON from the model's response.")
        extracted_info = {}
    except Exception as e:
        print(f"An error occurred: {e}")
        extracted_info = {}

    return extracted_info

def process_file(file_path):
    """
    Processes a single file to extract structured information.

    Args:
        file_path (str): Path to the input file.

    Returns:
        dict or None: Extracted information or None if unsupported format.
    """
    print(f"Processing file: {file_path}")
    if file_path.endswith(('.html', '.htm')):
        text = parse_html(file_path)
    elif file_path.endswith('.pdf'):
        text = parse_pdf(file_path)
    else:
        print(f"Unsupported file format: {file_path}")
        return None

    extracted_info = extract_information(text)
    return extracted_info

def process_folders(folder_paths, output_dir, combine_output=False):
    """
    Processes multiple folders to extract information from supported files and saves data to a JSON file..

    Args:
        folder_paths (list): List of folder paths to process.
        output_dir (str): Directory to save the output JSON files.
        combine_output (bool): Whether to combine output into a single file per folder.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for folder in folder_paths:
        if not os.path.isdir(folder):
            print(f"The folder {folder} does not exist or is not a directory.")
            continue

        folder_name = os.path.basename(folder)
        combined_data = []

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if not os.path.isfile(file_path):
                continue
            if not any(filename.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                continue

            extracted_info = process_file(file_path)
            if extracted_info:
                if combine_output:
                    combined_data.append(extracted_info)
                else:
                    output_filename = os.path.splitext(filename)[0] + '.json'
                    output_path = os.path.join(output_dir, output_filename)
                    with open(output_path, 'w', encoding='utf-8') as json_file:
                        json.dump(extracted_info, json_file, ensure_ascii=False, indent=4)
                    print(f"Structured data saved to {output_path}")

        if combine_output and combined_data:
            output_filename = f"{folder_name}_processed.json"
            output_path = os.path.join(output_dir, output_filename)
            with open(output_path, 'w', encoding='utf-8') as json_file:
                json.dump(combined_data, json_file, ensure_ascii=False, indent=4)
            print(f"Combined structured data for folder '{folder}' saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract structured information from RFP documents in multiple directories.')
    parser.add_argument('output_dir', help='Path to the directory where output JSON files will be saved.')
    parser.add_argument('--combine', action='store_true', help='Combine all outputs into a single JSON file per folder.')

    args = parser.parse_args()

    input_folders = ["bid1", "bid2"]
    process_folders(input_folders, args.output_dir, args.combine)

