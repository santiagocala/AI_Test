
from PyPDF2 import PdfReader
from pydantic import BaseModel
from openai import OpenAI
import json
import streamlit as st

client = OpenAI(api_key='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')

st.title("PDF to JSON Converter")

def read_pdf_file(file_path):
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        pdf_content = ""
        for page in reader.pages:
            pdf_content += page.extract_text()
        return pdf_content

# Example usage
pdf_file_path = input("Enter the path to the PDF file: ")
pdf_content = read_pdf_file(pdf_file_path)

# Generate JSON with certain values using Structured Outputs
json_generation = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "Your task is to generate a JSON object from the PDF content. What you are supposed to recieve are quotes from different allies and we need you to give them to us in the JSON Schema defined in the response format."},
        {
            "role": "user",
            "content": f"PDF Content:\n{pdf_content}\n\nGenerate JSON"
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "quote_response",
            "schema": {
                "type": "object",
                "properties": {
                    "alternatives": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "items": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "concept": {"type": "string"},
                                            "amount": {"type": "integer"},
                                            "price": {"type": "number"}
                                        },
                                        "required": ["concept", "amount", "price"],
                                        "additionalProperties": False
                                    }
                                }
                            },
                            "required": ["items"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["alternatives"],
                "additionalProperties": False
            },          
            "strict": True
        }
    }
)

# Convert JSON string to Python dictionary
json_data = json.loads(json_generation.choices[0].message.content)

# Pretty print the JSON
print("Generated JSON:")
print(json.dumps(json_data, indent=4))
