import os
import PyPDF2
import google.generativeai as genai
import json

from dotenv import load_dotenv

load_dotenv()


genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)
for m in genai.list_models():
 print(m.name)
 model = genai.GenerativeModel("gemini-2.5-flash")


 def extract_text_from_pdf(pdf_path):
    text =""
    with open(pdf_path,'rb') as file:
        reader = PyPDF2.PdfReader(file)

        for page in reader.pages:
            text +=page.extract_text()

    return text
  
def detect_skills(text):
    skill_lists = [
              "Python",
              "Django",
              "HTML",
              "CSS",
              "Bootstrap",
              "javascript",
              "MYSQL",
              "JAVA",
              "C++",
              "React",
              "REST API",
              "Github",
              "Machine Learning",
              "VS-Code",
              "jupyter notebook",
              "numpy",
              "pandas",
              "matplotlib",
              "seaborn",
              "scikitlearn",
              "tensorflow",
              "EDA",
              "data analysis",
              "My-sql",
              "flutter",
              "aws",
              "docker",
              "fast API",
              "KERAS",
              "pytorch",
              "kotlin",
              "web scaping",
              "automation",
              "communication",
              "leadership",
              "problem solving",
              "data science",
              "generative ai",
              "agentic ai",
              "prompt engineering",
              "graphic designing",
              "content creation",
              "video editing",
              


    ]

    found_skills = []

    for skill in skill_lists:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills

def calculate_resume_score(skills):

    score = 0
    score += min(len(skills)*5,40)

    print("Skills:",skills)
    print("Skills Count:",len(skills))
    print("Current Score:",score)

    return min(score,100)

def analyze_resume_feedback(text,skills):
    strengths = []
    weaknesses =[]

    if len(skills)>=5:
        strengths.append("Good technical skills")

    else:
        weaknesses.append("Add More technical skills")

    if "github" in text.lower():
        strengths.append("Github Profile Found")

    else:
        weaknesses.append('Github Profile is missing')

    if "linkedin" in text.lower():
        strengths.append("Linkedin Profile is Found")

    else:
        weaknesses.append("Linkedin Profile is missing")


    
    if "project" in text.lower():
        strengths.append("Projects Section Found")

    else:
        weaknesses.append("Project Section is missing")

    return strengths,weaknesses


def calculate_job_match(resume_skills,job_skills):
    matched_skills =[]
    missing_skills =[]
    for skill in job_skills:
        if skill.lower() in [
            s.lower()
            for s in resume_skills
        ]:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    if len(job_skills) == 0:
        return 0,[]
    match_score = int((len(matched_skills)/len(job_skills))*100) if job_skills else 0
        
    return match_score,matched_skills,missing_skills


def generate_interview_questions(skills):

    prompt = f"""
You are an expert technical interviewer.

Generate EXACTLY 15 multiple choice interview questions
based on these skills:

{skills}

Rules:

1. Questions should be for freshers.
2. Every question must have exactly 4 options.
3. Only one option should be correct.
4. Keep questions easy to medium.
5. Return ONLY valid JSON.
6. Do not write markdown.
7. Do not write explanation outside JSON.

Return format:

[
    {{
        "question":"What is Python?",
        "options":[
            "Programming Language",
            "Database",
            "Operating System",
            "Browser"
        ],
        "correct_answer":"Programming Language"
    }}
]
"""

    try:
        response = model.generate_content(prompt)

        text = response.text.strip()

        print(text)   # Debug

        if text.startswith("json"):
               text = text.replace("json", "").replace("", "").strip()

        elif text.startswith(""):
              text = text.replace("```", "").strip()

        questions = json.loads(text)

        return questions

    except Exception as e:

        print("Question Generation Error :", e)

        return []


def generate_career_guidance(skills):

    prompt = f"""
             Generate career guidance based on these skills:

             {skills}
             1.Suitable job roles
             2.Missing skills
             3.Learning Roadmap
             """
    response = model.generate_content(prompt)
    return response.text

def test_gemini():
    response = model.generate_content("hello")
    print(response.text)


def generate_recruiter_questions(job_title,skills):
    prompt = f"""Job Title: {job_title}

         Required skills: {skills}

         Generate 10 interview questions.

         Include:
         - Technical Questions 
         - HR Questions

         Level: Fresher

         Return only questions.

        """
    response = model.generate_content(prompt)

    return response.text
        

def generate_resume_suggestions(skills,score,weaknesses):
    
    prompt = f"""

             Resume skills:
             {skills}

             Resume score:
             {score}

            Resume weakn areas:

            {weaknesses}

            Give practical suggesstions 
            to improve resume and placement chances.
             """
    

    response = model.generate_content(prompt)

    return response.text


def evaluate_answer(question, answer):

    prompt = f"""
You are an experienced technical interviewer.

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer professionally.

Return in this format only:

Score: X/10

Correct Answer:
(Write an ideal interview answer.)

Review:
(Explain what the candidate did well and what mistakes were made.)

Improvement Tips:
(Give 3-5 practical suggestions.)

Keep the language simple and professional.
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print("Gemini Error:", e)
        return f"Error: {e}"



def chatboat_response(message,skills):

         
    
         prompt = f"""
          You are AI Career Assistant
           User Skills:
          {skills}
          User Question:
          {message}

          Give practical and simple advice for students and freshers.
          Give answer in proffesional way step by step and next step start with new line
 
         """
         try:
           response = model.generate_content(prompt)
           return response.text
         except Exception as e:
             print("Gemini Error:, e")
             return "AI service temporarily unavailable.Please try again later."


        

  

def generate_ai_feedback(skills,score):

    prompt = f"""
     Generate professional recruiter feedback.

     

     Skills:
     {skills}

     Resume Score:
     {score}
   Give:
   1.Strengths
   2.Weaknesses
   3.Final Recommendation
          
"""
    response = model.generate_content(prompt)

    return response.text


def generate_cover_leter(resume_text,job_title):
    prompt = f"""

     Write a professional cover letter.

     Candidate Resume:
     {resume_text}

   Job title:
   {job_title}

  Keep it proffesional.

   """
    response = model.generate_content(prompt)

    return response.text




    

