import google.generativeai as genai

genai.configure(api_key='AIzaSyAqmRO04L7vpSAiAYXGEOBMlStrvajKh40')


def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text


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
    4. Responsibility

    Organize the extracted information into a structured response as a list with no heading. Each item in the list should contain the details for one project.

    Ensure that the extracted information is accurate and complete. You may use techniques such as named entity recognition, dependency parsing, or any other suitable methods for extraction.

    For each project, return a dictionary containing the extracted information. If no information is found for a particular project, skip it in the list.

    Example of the expected response format:
    [
        {{
            "Project Name": "Data Dialect",
            "Role": "Team Lead",
            "Date": "1st September 2023 - 18th January 2024",
            "Responsibility":" Built end-to-end application enabling natural language database access using Google PaLM, LangChain, Chroma DB, streamlit and Hugging Face vector embeddings."
        }},
        {{
            "Project Name": "Cell Vision",
            "Role": "Data Collector",
            "Date": "24th June 2021",
            "Responsibility":"Led cell segmentation project using YOLO v8 for precise instance segmentation. Built user-friendly Flask app deployed on Azure for scalability"
        }},
    ]

    """
    response = get_gemini_response(prompt)
    return response


def extract_skills(text):
    prompt = f"""
    **Resume Analysis:**

    The provided resume contains the following details:
    {text}

    As an experienced text extraction model, your task is to accurately extract and organize the relevant information from the resume.

    Please extract the following details and organize them into a structured response as a list with no heading:

    Extract skills and competencies mentioned in the resume.

    Please ensure that the extracted information is accurate and complete. You may use techniques such as named entity recognition, keyword extraction, or any other suitable methods for extraction.

    For each category, return a list containing the extracted information. If no information is found for a particular category, return an empty list.

    Here's an example of how the response should be structured:

    ["Python", "JavaScript", "Data Analysis", "Machine Learning", "Team Management"]
    """

    response = get_gemini_response(prompt)
    return response