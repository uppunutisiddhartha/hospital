from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import datetime,date
from calendar import monthrange
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404

# Create your views here.
def index(request):
    if request.method == 'POST':
        
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        specialist = request.POST.get('specialist')
        reason = request.POST.get('reason')

        date_str = request.POST.get('date')
        time_str = request.POST.get('time')

        # Convert date string to date object
        date = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Convert "09:00" → time object
        time = datetime.strptime(time_str, "%H:%M").time()

        Consultation.objects.create(
            name=name,
            phone=phone,
            email=email,
            date=date,
            time=time,
            specialist=specialist,
            reason=reason
        )

    return render(request, 'index.html')


def pre_consultation(request):
    appointments = Appointment.objects.all()
    return render(request, 'pre_consultation.html' , {'appointments': appointments})


def doctors(request):
    doctors = doctor.objects.all()
    return render(request, 'doctors.html', {'doctors': doctors})


@login_required
def MOD(request):
    today = date.today()
    selected_date_str = request.GET.get("date")  # from input or calendar button
    selected_date = None

    total_consultations = Consultation.objects.count()
    #month_consultations = Consultation.objects.filter(date__year=today.year, date__month=today.month).count()
    
    month_consultations = Consultation.objects.filter(date__year=today.year, date__month=today.month).count()
    # Parse the date safely
    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        except ValueError:
            selected_date = None

    # Determine month/year for the calendar
    year = selected_date.year if selected_date else today.year
    month = selected_date.month if selected_date else today.month

    # Build list of all dates in the month
    total_days = monthrange(year, month)[1]
    days_list = [date(year, month, d) for d in range(1, total_days + 1)]

    # Get all consultations in this month
    month_consults = Consultation.objects.filter(date__year=year, date__month=month)
    active_dates = {c.date for c in month_consults}

    # Get consultations for selected date
    consultations = Consultation.objects.filter(date=selected_date) if selected_date else []

    return render(request, "dashboards/MOD.html", {
        "days_list": days_list,
        "active_dates": active_dates,
        "consultations": consultations,
        "selected_date": selected_date,
        "current_month": f"{year}-{month:02d}",
        "total_consultations": total_consultations,
        "month_consultations": month_consultations,
    })



@login_required
def insurance_admin(request):
    insurance_list = Appointment.objects.all()
    return render(request, 'insurance_admin.html', {'insurance_list': insurance_list})

def insurance_list(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        insurance_name = request.POST.get('insurance_name')
        phone = request.POST.get('phone')
        policy_start_date = request.POST.get('policy_start_date')
        file = request.FILES.get('file')  # IMPORTANT

        Appointment.objects.create(
            full_name=full_name,
            insurance_name=insurance_name,
            phone=phone,
            policy_start_date=policy_start_date,
            file=file
        )

        return redirect('insurance_list')

    return render(request, 'insurance_list.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            return redirect('login')

        # STATUS CHECK
        if user.status == 'inactive':
            return render(request, 'error_pages/inactive.html')

        if user.status == 'suspended':
            return render(request, 'error_pages/suspended.html')

        if user.status == 'hold':
            return render(request, 'error_pages/hold.html')

        # LOGIN USER
        login(request, user)

        # ROLE REDIRECT
        if user.role == 'MOD':
            return redirect('MOD')

        elif user.role == 'INS_ADMIN':
            return redirect('insurance_admin')

        elif user.role == 'hr':
            return redirect('hr_dashboard')

        return redirect('login')

    return render(request, 'login.html')   


@login_required
def hr_dashboard(request):
    if request.user.role != 'hr':
        return redirect('login')
    return render(request, 'dashboards/hr_dashboard.html')

@login_required
def employemanagement(request):
    if request.user.role != 'hr':
        return redirect('login')
    user=CustomUser.objects.all()
    return render(request, 'employee_management.html',{'users':user})

def create_job(request):
    if request.method == "POST":
        jobnotification.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            vaccancy_count=int(request.POST.get("vaccancy_count")),
            deadline=request.POST.get("deadline"),
            salary=request.POST.get("salary"),
            experiance=request.POST.get("experiance"),
        )
        return redirect("career")

    return render(request, "create_job.html")

def career(request):
   if request.method=="POST":
       jobapplication.objects.create(
          applicant_name=request.POST.get("applicant_name"),
           email=request.POST.get("email"),
           phone=request.POST.get("phone"),
           resume=request.FILES.get("resume"),
           job_id=int(request.POST.get("job_id")),
       )
       return redirect("career")
   jobnofications=jobnotification.objects.filter(is_published=True,status='open')
   context={
       'jobnotifications':jobnofications
       }
   return render(request, 'career.html',context)

'''
def job_applications(request):
    applications = jobapplication.objects.all()
    return render(request, 'job_applications.html', {'applications': applications})
'''
def hr_all_applications(request):
    jobs = jobnotification.objects.prefetch_related('applications')

    return render(request, 'job_applications.html', {
        'jobs': jobs
    })

def job_notification(request):
    job= jobnotification.objects.all()
    return render(request, 'job_notification.html', {'job': job})

def publish_job(request, id):
    job = get_object_or_404(jobnotification, id=id)
    job.is_published = True
    job.save()
    return redirect('job_notification')


def unpublish_job(request, id):
    job = get_object_or_404(jobnotification, id=id)
    job.is_published = False
    job.save()
    return redirect('job_notification')


def delete_job(request, id):
    job = get_object_or_404(jobnotification, id=id)
    job.delete()
    return redirect('job_notification')

@login_required
def save_insurance_note(request):
    if request.method == "POST":
        insurance_id = request.POST.get("item_id")
        note_text = request.POST.get("admin_note")

        insurance = Appointment.objects.get(id=insurance_id)

        InsuranceNotes.objects.create(
            insurance=insurance,
            admin_name=request.user.username,
            notes=note_text
        )

        return redirect('insurance_admin')



@login_required
def update_user_status(request, user_id):
    if request.user.role != 'hr':
        return redirect('login')

    user = get_object_or_404(CustomUser, id=user_id)
    status = request.POST.get('status')

    if status not in ['active', 'hold', 'inactive', 'suspended']:
        messages.error(request, "Invalid status")
        return redirect('employee-management')

    user.status = status
    user.save()

    messages.success(request, f"{user.username} status updated to {status}")
    return redirect('employee_management')
