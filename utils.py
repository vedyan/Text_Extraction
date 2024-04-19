import google.generativeai as genai
import re
genai.configure(api_key='apikey')


def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text


def extract_experience(text):
    prompt = f"""
    **Resume Analysis:**

    The provided resume includes the following details:
    {text}

    Your task is to extract responsibilities or tasks associated with each job, including the job title and company name.

    Organize the extracted information into a structured list with no heading.

    Ensure accuracy and completeness in the extracted information. Techniques like named entity recognition or dependency parsing can be used for extraction.

    Return a list for each category. If no information is found for a particular category, return an empty list.

    Example of the expected response format:
    {{
        "experience": [
            {{
                "Role": "Software Engineer",
                "company name": "XYZ",
                "Responsibility": ["Developed and maintained web applications", "Implemented RESTful APIs"]
            }},
            {{
                "Role": "Web Developer",
                "company name": "ABC Company",
                "Responsibility": ["Designed and implemented responsive web interfaces"]
            }}
        ]
    }}
    """
    response_str = get_gemini_response(prompt)
    return response_str


def extract_projects(text):
    prompt = f"""
    **Resume Analysis:**

    The provided resume includes a projects section with the following details:
    {text}

    Your task is to extract responsibilities or tasks associated with each project listed.
    For each project, extract: Project Name, Role/Position, Date (Start date - End date, if available) ,Responsibility

    Organize the extracted information into a structured list with no heading.

    Ensure accuracy and completeness in the extracted information. Techniques like named entity recognition or dependency parsing can be used for extraction.

    Return a list for each category. If no information is found for a particular category, return an empty list.

    Example of the expected response format:
    {{
        "projects": [
            {{
                "Project Name": "Data Dialect",
                "Role": "Team Lead",
                "Responsibility": ["Built end-to-end application enabling natural language database access using Google PaLM, LangChain, Chroma DB, streamlit and Hugging Face vector embeddings."]
            }},
            {{
                "Project Name": "Cell Vision",
                "Role": "Data Collector",
                "Responsibility": ["Led cell segmentation project using YOLO v8 for precise instance segmentation. Built user-friendly Flask app deployed on Azure for scalability"]
            }}
        ]
    }}
    """
    response_str = get_gemini_response(prompt)
    return response_str


def extract_skills(text):
    prompt = f"""
    **Resume Analysis:**

    The provided resume contains the following details:
    {text}

    Your task is to extract skills and competencies mentioned in the resume and organize them into a structured list.

    Ensure accuracy and completeness in the extracted information. You can use techniques like named entity recognition or keyword extraction for extraction.

    Return a list containing all skills and competencies. If no information is found, return an empty list.

    Example response structure:

    ["Python", "JavaScript", "Data Analysis", "Machine Learning", "Team Management"]
    """

    response = get_gemini_response(prompt)
    skills_list = re.findall(r'\b[A-Za-z0-9]+\b', response)

    return skills_list