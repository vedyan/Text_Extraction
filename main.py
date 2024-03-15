from fastapi import FastAPI, UploadFile, File, Query
import fitz
import requests
from typing import Any
import re
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text


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


def extract_skills(text):
    # Define patterns for different skill-related sections
    skill_patterns = {
        "Programming Languages": r"(?i)Programming\s+Languages?:\s*(.+)",
        "Tools": r"(?i)Tools?:\s*(.+)",
        "Databases": r"(?i)Databases?:\s*(.+)",
        "Libraries": r"(?i)Libraries?:\s*(.+)",
        "Skills": r"(?i)Skills?:\s*(.+)",
        "Mathematics": r"(?i)Mathematics?:\s*(.+)",
        "Soft Skills": r"(?i)Soft\s+Skills?:\s*(.+)"
    }

    # Initialize an empty list to store extracted skills
    extracted_skills = []

    # Iterate over each skill pattern
    for section, pattern in skill_patterns.items():
        # Search for the pattern in the text
        match = re.search(pattern, text)
        if match:
            # Extract skills from the matched section
            skills = [skill.strip() for skill in match.group(1).split(',')]
            # Add extracted skills to the list
            extracted_skills.extend(skills)

    return extracted_skills


def extract_experience(text):
    prompt = f"""
    **Resume Analysis:**

    The provided resume contains the following details:
    {text}

    As an experienced text extraction model, your task is to accurately extract and organize the relevant information from the resume.

    Please extract the following details and organize them into a structured response as a list with no heading:

    Extract responsibilities or tasks associated with each job with job title and company name.

    Please ensure that the extracted information is accurate and complete. You may use techniques such as named entity recognition, dependency parsing, or any other suitable methods for extraction.

    For each category, return a list containing the extracted information. If no information is found for a particular category, return an empty list.

    Here's an example of how the response should be structured:

    ["software engineer", "oxyz company", ["Developed and maintained web applications", "Implemented RESTful APIs"], "Web Developer", "ABC company" ,["Designed and implemented responsive web interfaces"]]

    """
    response = get_gemini_response(prompt)
    return response


def extract_projects(text):
    prompt = f"""
    **Resume Analysis:**

    The provided resume contains the following projects section:
    {text}

    As a text extraction model, your task is to accurately extract responsibilities or tasks associated with each project listed under the projects section. For each project, extract the following details:

    1. Project Name
    2. Role/Position
    3. Date (Start date - End date, if available)

    Organize the extracted information into a structured response as a list with no heading. Each item in the list should contain the details for one project.

    Ensure that the extracted information is accurate and complete. You may use techniques such as named entity recognition, dependency parsing, or any other suitable methods for extraction.

    For each project, return a dictionary containing the extracted information. If no information is found for a particular project, skip it in the list.

    Example of the expected response format:
    [
        {{
            "Project Name": "Data Dialect",
            "Role": "Team Lead",
            "Date": "1st September 2023 - 18th January 2024",
            "responsibility":" Built end-to-end application enabling natural language database access using Google PaLM, LangChain, Chroma DB, streamlit and Hugging Face vector embeddings."
        }},
        {{
            "Project Name": "Cell Vision",
            "Role": "Data Collector",
            "Date": "24th June 2021",
            "responsibility":"Led cell segmentation project using YOLO v8 for precise instance segmentation. Built user-friendly Flask app deployed on Azure for scalability"
        }},
    ]

    Please ensure accurate extraction and proper formatting. If you encounter any difficulties or have any questions, feel free to ask.
    """
    response = get_gemini_response(prompt)
    print(response)
    return response


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
        skills = extract_skills(text)
        experience = extract_experience(text)
        projects = extract_projects(text)

        return {
            "text": text,
            "name": name,
            "email": email,
            "number": number,
            "skills": skills,
            "experience": experience,
            "projects": projects
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
        skills = extract_skills(text)
        experience = extract_experience(text)
        projects = extract_projects(text)

        return {
            "text": text,
            "name": name,
            "email": email,
            "number": number,
            "skills": skills,
            "experience": experience,
            "projects": projects
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching PDF from URL: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}