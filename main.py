from fastapi import FastAPI, UploadFile, File, Query
import fitz
import requests
from typing import Any
import re
from utils import extract_projects, extract_experience, extract_skills

app = FastAPI()


def extract_mobile_number(text):
    mobile_number = re.findall(r'[7-9][0-9]{9}', text)
    return mobile_number


def extract_email(text):
    email_pattern = r"\b([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]{1,64})\b"  # Optimized pattern
    email_match = re.search(email_pattern, text)
    return email_match.group(0) if email_match else ""


def extract_name(text):
    name_match = re.search(r"([A-Z][a-z]+\s+){1,3}", text)
    name = name_match.group(0).strip() if name_match else ""
    return name


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

        name = extract_name(text)
        email = extract_email(text)
        number = extract_mobile_number(text)

        return {
            "text": text,
            "name": name,
            "email": email,
            "number": number
        }

    except Exception as e:
        return {"error": str(e)}


@app.post("/extract_text_from_url")
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

        name = extract_name(text)
        email = extract_email(text)
        number = extract_mobile_number(text)

        return {
            "text": text,
            "name": name,
            "email": email,
            "number": number
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching PDF from URL: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}


@app.post("/extract_experience")
async def extract_experience_from_text(text) -> Any:
    try:
        experience = extract_experience(text)

        return {
            "experience": experience
        }

    except Exception as e:
        return {"error": str(e)}


@app.post("/extract_projects")
async def extract_projects_from_text(text) -> Any:
    try:
        projects = extract_projects(text)

        return {
            "projects": projects
        }

    except Exception as e:
        return {"error": str(e)}


@app.post("/extract_skills")
async def extract_skills_from_text(text) -> Any:
    try:
        skills = extract_skills(text)

        return {
            "skills": skills
        }

    except Exception as e:
        return {"error": str(e)}

