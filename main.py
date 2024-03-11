from fastapi import FastAPI, UploadFile, File
import fitz
from io import BytesIO
from typing import Any

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>PDF Text Extractor</title>
    </head>
    <body>
        <div>
            <h1>PDF Text Extractor</h1>
            <form action="/extract_text" method="post" enctype="multipart/form-data">
                <label for="pdf_file">Upload a PDF file:</label><br>
                <input type="file" id="pdf_file" name="pdf_file"><br><br>
                <input type="submit" value="Submit">
            </form>
            <p>Powered by <a href="https://vercel.com" target="_blank">Vercel</a></p>
        </div>
    </body>
</html>
"""


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