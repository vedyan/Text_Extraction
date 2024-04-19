
# Text Extraction API

# ADD your API key before running or deployment.


## Description

This API extracts text content from uploaded PDF files. It utilizes the PyPDF2 library to process PDFs and returns the extracted text as a string.

## Endpoints

* **POST /extract_text**
    Extracts text from a uploaded PDF file.

## Request Data

**Parameter:**

- **pdf_file** (file, required): The PDF file to extract text from. (**Note:** Must be a PDF file)

**Format:**

The request should include a multipart form data section with a key named `pdf_file` containing the PDF file to be processed.

## Response Data

**Success:**

```json
{
    "text": "(extracted text content here)"
}
```

**Error:**

```json
{
    "error": "(error message)"
}
```

**Example (Success):**

The API response for a successfully extracted PDF might look like:

```json
{
    "text": "This is some sample text content from the first page of the PDF.\nHere's some more text from the second page."
}
```

**Example (Error):**

If an error occurs during processing, the API will return a JSON response with an error message. For instance, if the uploaded file is not a PDF, the response might be:

```json
{
    "error": "Invalid file format. Please upload a PDF file."
}
```

## Required Packages

* `fastapi`
* `PyPDF2`

## Additional Notes

* This API relies on the `PyPDF2` library for PDF processing. Ensure it's installed in your environment.


