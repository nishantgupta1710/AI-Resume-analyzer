from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import CandidateProfile
from jobs.models import jobs,Application
from resume.utils import calculate_job_match
from resume.models import Resume
from django.contrib import messages
from resume.utils import generate_resume_suggestions 
# Create your views here.

def home(request):
    return render(request,'home.html',{})

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    


        user = authenticate(request,username = username,password = password)
        print("User:",user)

        if user is not None:
        
            login(request,user)
            
            profile= CandidateProfile.objects.get(user=user)
            if profile.role == "Recruiter":
                   print("recruiter")
                   return redirect("/recruiter_dashboard/")
            else:
            
                print("candidate")
                return redirect('/dashboard/')
               
            
    
         
        
        
            
            
    return render(request,'login.html',{})

def signup_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print("POST data:",request.POST)
        email = request.POST.get('email')
        password= request.POST.get('password')
        role = request.POST.get('role')

        user = User.objects.create_user(username,email,password)

        CandidateProfile.objects.create(user =user,role=role)
        
        return redirect('/login/')
    return render(request,'signup.html',{})

@login_required
def dashboard(request):

    total_jobs = jobs.objects.count()

    total_applied = Application.objects.filter(
        user=request.user
    ).count()

    shortlisted = Application.objects.filter(
        user=request.user,
        status="Shortlisted"
    ).count()

    rejected = Application.objects.filter(
        user=request.user,
        status="Reject"
    ).count()

    recent_applications = Application.objects.filter(
        user=request.user
    ).order_by('-id')[:5]

    # Resume
    resume = Resume.objects.filter(user=request.user).first()

    resume_score = 0

    if resume:
        resume_score = resume.score

    # User Skills
    user_skills = []

    if resume and resume.skills:
        user_skills = [
            skill.strip().lower()
            for skill in resume.skills.split(",")
            if skill.strip()
        ]

    # Top Matching Jobs
    job_matches = []

    all_jobs = jobs.objects.all()[:5]

    for job in all_jobs:

        job_skills = [
            skill.strip().lower()
            for skill in job.skills_required.split(",")
            if skill.strip()
        ]

        matched = len(set(user_skills) & set(job_skills))

        if len(job_skills) > 0:
            score = int((matched / len(job_skills)) * 100)
        else:
            score = 0

        job_matches.append({
            "job": job,
            "score": score
        })

    return render(
        request,
        "dashboard.html",
        {
            "total_jobs": total_jobs,
            "total_applied": total_applied,
            "shortlisted": shortlisted,
            "rejected": rejected,
            "recent_applications": recent_applications,
            "job_matches": job_matches,
            "resume_score": resume_score,
        }
    )
def logout_page(request):
    logout(request)
    return redirect('/login/')
 
@login_required
def profile_page(request):

    profile, created = CandidateProfile.objects.get_or_create(
        user=request.user
    )

    skills_list = []

    if profile.skills:
        skills_list = [
        skill.strip()
        for skill in profile.skills.split(",")
        if skill.strip()
    ]
    
    completion = 0

    # Username
    if request.user.username:
         completion += 20

    # Phone
    if profile.phone:
         completion += 20

    # College
    if profile.college:
         completion += 20

    # Skills
    if profile.skills:
         completion += 20

    # Resume Uploaded
    resume = Resume.objects.filter(user=request.user).first()

    if resume and resume.resume_file:
        completion += 20


    if completion == 100:
        completion_message = "🎉 Your profile is fully completed."

    elif completion >= 60:
        completion_message = "👍 Complete the remaining details to improve your profile."

    else:
        completion_message = "⚠️ Complete your profile to get better job recommendations."

    if resume and resume.resume_file:
        resume_status = "Uploaded"
    else:
        resume_status = "Not Uploaded"

    skills_count = len(skills_list)

    if request.method == "POST":

        profile.phone = request.POST.get("phone")
        profile.college = request.POST.get("college")
        profile.skills = request.POST.get("skills")

        profile.save()

        return redirect("profile")
    

    return render(
        request,
        "profile.html",
        {
            "profile": profile,
            "profile_completion":completion,
            "completion_message":completion_message,
            "skills_list":skills_list,
            "resume_status":resume_status,
            "skills_count":len(skills_list),
            "joined_date":request.user.date_joined,
        },
    )
@login_required
def edit_profile(request):

    profile, created = CandidateProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        profile.phone = request.POST.get("phone")
        profile.college = request.POST.get("college")
        profile.skills = request.POST.get("skills")

        profile.save()
        messages.success(request,"Profile updated successfully.")

        return redirect("profile")

    return render(
        request,
        "edit_profile.html",
        {
            "profile": profile,
        },
    )
