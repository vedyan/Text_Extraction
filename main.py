from fastapi import FastAPI, UploadFile, File, Query
import fitz
import requests
from typing import Any


app = FastAPI()


@app.post("/extract_text")
async def extract_text(pdf_file: UploadFile = File(...)) -> Any:
    try:
        # Extract text from the PDF
        pdf_data = await pdf_file.read()
        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")

        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()

        return {"text": text}
    except Exception as e:
        return {"error": str(e)}


@app.post("/extract_text")
async def extract_text_from_s3(pdf_url: str = Query(..., description="URL of the PDF file on S3")) -> Any:
    try:
        # Fetch the PDF content from the provided URL
        response = requests.get(pdf_url)
        response.raise_for_status()
        pdf_data = response.content

        # Extract text from the PDF
        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")

        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()

        return {"text": text}
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching PDF from URL: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}