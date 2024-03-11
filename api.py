from fastapi import FastAPI, UploadFile, File
from PyPDF2 import PdfReader
from io import BytesIO
from typing import Any

app = FastAPI()


@app.post("/extract_text")
async def extract_text(pdf_file: UploadFile = File(...)) -> Any:
    try:
        # Extract text from the PDF
        pdf_reader = PdfReader(BytesIO(await pdf_file.read()))
        data = ""
        for i in pdf_reader.pages:
            data += i.extract_text() + "\n"

        return {"text": data}
    except Exception as e:
        return {"error": str(e)}
