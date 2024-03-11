from fastapi import FastAPI, UploadFile, File
import fitz
from io import BytesIO
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