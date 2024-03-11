from fastapi import FastAPI, UploadFile, File
from PyPDF2 import PdfReader
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
        pdf_reader = PdfReader(BytesIO(await pdf_file.read()))
        data = ""
        for i in pdf_reader.pages:
            data += i.extract_text() + "\n"

        return {"text": data}
    except Exception as e:
        return {"error": str(e)}
