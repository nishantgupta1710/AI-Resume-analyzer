from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Resume
from django.shortcuts import get_object_or_404

from .utils import extract_text_from_pdf,detect_skills,calculate_resume_score,analyze_resume_feedback
from jobs.models import jobs as JobModel,Application
from .utils import calculate_job_match,evaluate_answer,chatboat_response,generate_ai_feedback
from .utils import generate_interview_questions,generate_career_guidance,generate_resume_suggestions,generate_cover_leter
# Create your views here.
@login_required

def upload_resume(request):
    resume_obj, created = Resume.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        resume_file = request.FILES.get('resume_file')

        if resume_file:
            resume_obj.resume_file = resume_file
            resume_obj.save()

        return redirect('/dashboard/') 
    return render(request,'upload_resume.html',{'resume': resume_obj})

@login_required

def analyze_resume(request):
    
    resume = Resume.objects.get(user = request.user)

    text = extract_text_from_pdf(resume.resume_file.path) 

    skills = detect_skills(text)

    questions = generate_interview_questions(skills)
    career_guidance = generate_career_guidance(skills)

    score = calculate_resume_score(skills)
    resume.score = score
    resume.skills = ",".join(skills)
    resume.save()

    strengths,weaknesses = analyze_resume_feedback(text,skills)
    suggestions = generate_resume_suggestions(skills,score,weaknesses)

    

    jobs = JobModel.objects.all()
    job_matches = []

    for job in jobs:
        job_skills = [skill.strip() for skill in job.skills_required.split(',') ]
    
    

        match_score,matched_skills,missing_skills= calculate_job_match(skills,job_skills)
        job_matches.append(
            {
                'job':job,
                'score':match_score,
                'matched':matched_skills,
                'missing':missing_skills,

            }

        )
    
    job_matches.sort(
        key = lambda x:x['score'],
        reverse=True
    )  
    recommended_jobs = job_matches[:5]

    


    return render(request,'analyze_resume.html',{'text':text,'skills':skills,'score':score,'strengths':strengths,'weaknesses':weaknesses,'job_matches':job_matches,'recommended_jobs':recommended_jobs,'questions':questions,'career_guidance':career_guidance,'suggestions':suggestions})
def mock_interview(request):

    

    # 1. Resume hai bhi ya nahi check karo
    try:
        resume = Resume.objects.get(user=request.user)
    except Resume.DoesNotExist:
        return render(request, "upload_resume.html", {
            "error": "Pehle resume upload karo, tabhi mock interview start hoga"
        })

    # 2. File upload hui hai ya khali hai check karo
    if not resume.resume_file:
        return render(request, "upload_resume.html", {
            "error": "Resume file missing hai. Phir se upload kar do"
        })

    # Ab safe hai, file pakka hai
    text = extract_text_from_pdf(resume.resume_file.path)

    skills = detect_skills(text)

    # Questions sirf ek baar generate honge
    if "questions" not in request.session:

        questions = generate_interview_questions(skills)

        request.session["questions"] = questions
        request.session["current_index"] = 0
        request.session["score"] = 0
        request.session["answers"] = []

        print(type(questions))
        print(questions)
        print(type(questions))

    questions = request.session["questions"]
    index = request.session["current_index"]

    current = questions[index]

    question = current["question"]
    options = current["options"]
    correct_answer = current["correct_answer"]

    feedback = ""
    if request.method == "POST":

        selected_answer = request.POST.get("answer")

        answers = request.session.get("answers",[])
        answers.append({
            "question":question,
            "selected":selected_answer,
            "correct":correct_answer,
            "is_correct":selected_answer == correct_answer
        })
        request.session["answers"] = answers

        if selected_answer == correct_answer:
            request.session["score"] += 1

        if index < len(questions) - 1:
            request.session["current_index"] += 1

            return redirect("mock_interview")

        else:
            score = request.session["score"]

            total = len(questions)
            wrong = total - score
            percentage = round((score / total) * 100)

            answers = request.session.get("answers",[])

            if percentage >= 90:
                performance = "Excellent 🏆"
            elif percentage >= 75:
                performance = "Very Good 🌟"
            elif percentage >= 60:
                performance = "Good 👍"
            elif percentage >= 40:
                 performance = "Average 🙂"
            else:
                 performance = "Needs Improvement 📚"

            request.session.pop("questions", None)
            request.session.pop("current_index", None)
            request.session.pop("score", None)
            request.session.pop("answers",None)

            return render(
              request,
              "mock_interview.html",
    {
        "completed": True,
        "score": score,
        "wrong": wrong,
        "percentage": percentage,
        "performance": performance,
        "total_questions": total,
        "answers":answers
    },
)


    return render(
    request,
    "mock_interview.html",
    {
        "question": question,
        "options": options,
        "current_question": index + 1,
        "total_questions": len(questions),
        "score": request.session["score"],
    },
)
def career_chatboat(request):

    answer = ""

    if request.method =="POST":
        message = request.POST.get('message')
        skills = request.POST.get('skills')

        

    
        answer = chatboat_response(message,skills)


    return render(request,'career_chatboat.html',{'answer':answer})

def ai_feedback(request,app_id):

    application = get_object_or_404(Application,id = app_id)

    skills = application.user.resume.skills
    score = application.user.resume.score


    feedback = generate_ai_feedback(skills,score)

    application.feedback = feedback
    application.save()

    return redirect('view_applications',job_id=application.job.id)


def cover_letter(request):
    cover_letter =""

    if request.method == "POST":
        resume = Resume.objects.get(user=request.user)

        resume_text=extract_text_from_pdf(resume.resume_file.path)

        cover_letter = generate_cover_leter(resume_text,"Python Developer")

    return render(request,'cover_letter.html',{'cover_letter':cover_letter})

@login_required
def resume_loading(request):

    return render(
        request,
        "resume_loading.html"
    )