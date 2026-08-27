from django.shortcuts import render
from .models import RecruiterProfile
from jobs.models import jobs
from jobs.models import jobs,Application
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required\


# Create your views here.
def recruiter_dashboard(request):

    all_jobs = jobs.objects.all()

    total_jobs = all_jobs.count()

    total_applications = Application.objects.count()

    shortlisted = Application.objects.filter(
        status="Shortlisted"
    ).count()

    rejected = Application.objects.filter(
        status="Reject"
    ).count()

    recent_applications = Application.objects.order_by(
        '-applied_at'
    )[:5]

    recent_jobs = jobs.objects.order_by('-created_at')[:3]

    context = {
        'jobs': all_jobs,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'shortlisted': shortlisted,
        'rejected': rejected,
        'recent_applications': recent_applications,
        'recent_jobs':recent_jobs,
        'active_page':'dashboard'
    }

    return render(
        request,
        'recruiter_dashboard.html',
        context
    )

def manage_jobs(request):
    all_jobs = jobs.objects.all()

    return render(request,'manage_jobs.html',{'jobs':all_jobs,'active_page':'manage_jobs'})

def recruiter_applications(request):
    applications = Application.objects.all()

    return render(request,'recruiter_applications.html',{'applications':applications,'active_page':'applications'})

def update_application_status(request,app_id,status):
    application = get_object_or_404(Application,id=app_id)

    application.status =status
    application.save()
    return redirect('recruiter_applications')

def analytics(request):

    total_jobs = jobs.objects.count()

    total_applications = Application.objects.count()

    shortlisted = Application.objects.filter(status = "Shortlisted").count()

    rejected = Application.objects.filter(status="Rejected").count()

    pending = Application.objects.filter(status="Pending").count()

    context ={
        "total_jobs":total_jobs,
        "total_applications":total_applications,
        "shortlisted":shortlisted,
        "rejected":rejected,
        "pending":pending,
        "active_page":"analytics"
    }
    return render(request,"analytics.html",context)


@login_required
def recruiter_profile(request):

    profile, created = RecruiterProfile.objects.get_or_create(
        user=request.user
    )

    total_jobs = jobs.objects.filter(
        recruiter=request.user
    ).count()

    total_applications = Application.objects.filter(
        job__recruiter=request.user
    ).count()
    active_jobs = jobs.objects.filter(recruiter = request.user).count()

    completion = 0

    if profile.company_name:
        completion += 15

    if profile.hr_name:
        completion += 15

    if profile.phone:
        completion += 15

    if profile.location:
        completion += 15

    if profile.website:
        completion += 20

    if profile.about_company:
        completion += 20

    if completion == 100:
        completion_message = "🎉 Company profile is fully completed."

    elif completion >= 60:
        completion_message = "👍 Complete remaining details."

    else:
        completion_message = "⚠️ Complete your company profile."

    return render(
        request,
        "recruiter_profile.html",
        {
            "profile": profile,
            "total_jobs": total_jobs,
            "total_applications": total_applications,
            "profile_completion": completion,
            "completion_message": completion_message,
            "active_jobs":active_jobs,
        },
    )

def edit_recruiter_profile(request):

    profile, created = RecruiterProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        profile.company_name = request.POST.get("company_name")
        profile.hr_name = request.POST.get("hr_name")
        profile.phone = request.POST.get("phone")
        profile.location = request.POST.get("location")
        profile.website = request.POST.get("website")
        profile.about_company = request.POST.get("about_company")

        profile.save()

        return redirect("recruiter_profile")

    return render(
        request,
        "edit_recruiter_profile.html",
        {
            "profile": profile
        }
    )