import openai
from PyPDF2 import PdfReader

# Initialize OpenAI client
#openai.api_key = 'your-api-key-here'
from openai import OpenAI
client = OpenAI()


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
print("Extracted PDF Content:")
print(pdf_content)

# Ask OpenAI questions about the PDF content
question = input("Enter your question about the PDF content: ")
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"PDF Content:\n{pdf_content}\n\nQuestion: {question}"
        }
    ]
)

print(completion.choices[0].message)