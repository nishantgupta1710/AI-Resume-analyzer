from django.shortcuts import render,redirect
from .models import jobs,Application
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from resume.models import Resume
from django.contrib import messages
from resume.utils import generate_recruiter_questions,extract_text_from_pdf,detect_skills,calculate_resume_score,generate_ai_feedback


# Create your views here

def create_job(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        company_name = request.POST.get('company_name')
        location = request.POST.get('location')
        salary = request.POST.get('salary')
        skills_required = request.POST.get('skills_required')
        description = request.POST.get('description')

        jobs.objects.create(
            recruiter=request.user,
            title=title,
            company_name=company_name,
            location=location,
            salary=salary,
            skills_required=skills_required,
            description=description,
        )

        return redirect('/dashboard/')
    
    return render(request,'create_job.html')

def job_list(request):

    job_list = jobs.objects.all().order_by("-created_at")

    applied_jobs = []

    if request.user.is_authenticated:
        applied_jobs = Application.objects.filter(
            user=request.user
        ).values_list("job_id", flat=True)

    return render(
        request,
        "job_list.html",
        {
            "jobs": job_list,
            "applied_jobs": applied_jobs,
        },
    )

def job_detail(request,job_id):

    job =get_object_or_404(jobs,id =job_id)

    return render(request,'job_detail.html',{'job':job})


@login_required
def apply_job(request,job_id):
    job = jobs.objects.get(id=job_id)

    Application.objects.get_or_create(user=request.user,job=job)

    return redirect('/jobs/')

@login_required
def my_applications(request):
    

    application = Application.objects.filter(user = request.user)

    return render(request,"my_applications.html",{'application':application})

def edit_job(request, id):

    job = jobs.objects.get(id=id)

    if request.method == 'POST':

        job.title = request.POST.get('title')

        job.company_name = request.POST.get('company_name')

        job.save()

        return redirect('recruiter_dashboard')

    return render(
        request,
        'edit_job.html',
        {
            'job': job
        }
    )

def delete_job(request,id):
    job = get_object_or_404(jobs,id=id)

    if request.method=="POST":

        job.delete()

        return redirect('manage_jobs')
    return render(request,"delete_job.html",{'job':job})


def apply_job(request,job_id):
    job = get_object_or_404(jobs,id=job_id)

    resume =Resume.objects.filter(user=request.user).first()

    if not resume or not resume.resume_file:
        messages.error(request,"Please upload resume first")
        return redirect('upload_resume')
    
    already_applied = Application.objects.filter(user = request.user,job =job).exists()

    if already_applied:
        messages.error(request,'You already applied for this job')
        return redirect('job_list')
    
    Application.objects.create(user = request.user,job=job)
    messages.success(request,"Application submitted successfully")

    print(request.user)
    print(Resume.objects.filter(user=request.user).exists())

    return redirect('job_list')


def job_applications(request,job_id):
    job = jobs.objects.get(id=job_id)

    applications = Application.objects.filter(job=job)
    
    return render(request,'view_applications.html',{'job':job,'applications':applications})

def shortlist_application(request,app_id):
    application = get_object_or_404(Application,id=app_id)

    application.status ="Shortlisted"

    application.save()

    return redirect('view_applications',job_id=application.job.id)




def reject_application(request,app_id):
    application = get_object_or_404(Application,id=app_id)

    application.status ="Reject"

    application.save()

    return redirect('view_applications',job_id=application.job.id)



def recruiter_questions(request,job_id):

    job = get_object_or_404(jobs,id=job_id)


    questions = generate_recruiter_questions(job.title,job.skills_required)

    return render(request,'recruiter_questions.html',{'job':job,'questions':questions})

def add_feedback(request,app_id):
    application = get_object_or_404(Application,id=app_id)

    if request.method == 'POST':
        application.feedback = request.POST.get('feedback')
        application.save()

        return redirect('view_applications',job_id=application.job.id)
    
    return render(request,'add_feedback.html',{'application':application})

def ai_feedback(request,app_id):

    application = get_object_or_404(Application,id =app_id)

    resume = Resume.objects.get(user=application.user)

    text = extract_text_from_pdf(resume.resume_file.path)

    skills =detect_skills(text)

    score = calculate_resume_score(skills)

    feedback = generate_ai_feedback(skills,score)
    application.feedback =feedback
    application.save()

    return render(request,"ai_feedback.html",{"application":application,"feedback":feedback,"score":score})

    
  
def job_applications(request,job_id):

    job = jobs.objects.get(id=job_id)

    applications = Application.objects.filter(job=job)

    return render(request,'view_applications.html',{'job':job,'applications':applications})
