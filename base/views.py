import email
from email.message import EmailMessage
from django.shortcuts import render,redirect
from .models import *
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime,date
from calendar import monthrange
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.utils.timezone import now
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
from .utils import send_post_newsletter


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

        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        time = datetime.strptime(time_str, "%H:%M").time()

        # Save consultation
        Consultation.objects.create(
            name=name,
            phone=phone,
            email=email,
            date=date,
            time=time,
            specialist=specialist,
            reason=reason
        )

        # Save message (optional)

        # 📧 SEND EMAIL TO USER
        subject = "Consultation Confirmation"
        message = f"""
Hello {name},

Your consultation has been successfully booked.

📅 Date: {date}
⏰ Time: {time}
👨‍⚕️ Specialist: {specialist}
📝 Reason: {reason}

Thank you for choosing us.
"""
        send_mail(
            subject,
            message,
            None,             
            [email],          
            fail_silently=False
        )

    post = Post.objects.filter(status='publish').order_by('-created_at')
    context = {'posts': post}
    return render(request, 'index.html', context)


def pre_consultation(request):
    appointments = Appointment.objects.all()
    return render(request, 'pre_consultation.html' , {'appointments': appointments})



def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        full_name = request.POST.get('full_name')
        password = request.POST.get('password')
        role = request.POST.get('role')
        email=request.POST.get('email')
        phone_number=request.POST.get('number')
        role = request.POST.get('role') or 'MOD'
        date_joined=date.today()

        CustomUser.objects.create_user(
            username=username,
            password=password,
            role=role,
            email=email,
            full_name=full_name,
            phone_number=phone_number,
            date_joined=date_joined,
            status='inactive'

        )
        html_content = render_to_string('email_templates/welcome_email.html', {'full_name': full_name,
        })
        email = EmailMessage(
            subject="Welcome to Pioneer Hospital",
            body=html_content,
            from_email=settings.EMAIL_HOST_USER,  
            to=[email],
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)

        return redirect('login')

    return render(request, 'register.html')

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
    
   # Monthly consultations QuerySet
    month_consults = Consultation.objects.filter(date__year=year, date__month=month)
    pending_responses_count_month = month_consults.filter(status='pending').count()
    responded_responses_count_month = month_consults.filter(status='responded').count()

# Daily consultations QuerySet
    consultations = Consultation.objects.filter(date=selected_date) if selected_date else Consultation.objects.none()
    pending_responses_count = consultations.filter(status='pending').count()
    responded_responses_count = consultations.filter(status='responded').count()

    responded_consultations = Consultation.objects.filter(
        date=selected_date,
        status='responded'
    ) if selected_date else []

    pending_consultations = Consultation.objects.filter(
        date=selected_date,
        status='pending'
    ) if selected_date else []

    return render(request, "dashboards/MOD.html", {
        "days_list": days_list,
        "active_dates": active_dates,
        "consultations": consultations,
        "selected_date": selected_date,
        "current_month": f"{year}-{month:02d}",
        "total_consultations": total_consultations,
        "month_consultations": month_consultations,
        "responded_consultations": responded_consultations,
        "pending_consultations": pending_consultations,
        "pending_responses_count": pending_responses_count,
        "responded_responses_count": responded_responses_count,
        "pending_responses_count_month": pending_responses_count_month,
        "responded_responses_count_month": responded_responses_count_month,
        
    })

@login_required
def respond_consultation(request, consultation_id):
    consultation = get_object_or_404(
        Consultation,
        id=consultation_id,
        status='pending'
    )

    consultation.status = 'responded'
    consultation.responded_by = request.user
    consultation.responded_at = now()
    consultation.save()

    return redirect(request.META.get("HTTP_REFERER", "MOD"))

@login_required
def insurance_admin(request):
    insurance_list = Appointment.objects.all()
    return render(request, 'dashboards/insurance_admin.html', {'insurance_list': insurance_list})

def insurance_list(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        insurance_name = request.POST.get('insurance_name')
        phone = request.POST.get('phone')
        policy_start_date = request.POST.get('policy_start_date')
        email = request.POST.get('email')
        file = request.FILES.get('file')  # IMPORTANT

        Appointment.objects.create(
            full_name=full_name,
            insurance_name=insurance_name,
            phone=phone,
            email=email,
            policy_start_date=policy_start_date,
            file=file
        )

        messages.success(request, "Insurance appointment created successfully.")
    
        html_content = render_to_string('email_templates/insurance_consultaion_conform.html', {'full_name': full_name,
        })
        email = EmailMessage(
            subject="Insurance Consultation Confirmation",
            body=html_content,
            from_email=settings.EMAIL_HOST_USER,  
            to=[email],       
        )
        email.content_subtype = "html"  
        email.send(fail_silently=False)

        return redirect('insurance_list')

    return render(request, 'insurance_list.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password")
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
        
        elif user.role == 'general_manager':
            return redirect('general_manager_dashboard')

        elif user.role == 'hr':
            return redirect('hr_dashboard')

        return redirect('login')

    return render(request, 'login.html')   


@login_required
def hr_dashboard(request):
    if request.user.role != 'hr':
        return redirect('login')
    active_jobs = jobnotification.objects.filter(is_published=True, status='open').count()
    inactive_jobs = jobnotification.objects.filter(is_published=False).count()
    total_applicants = jobapplication.objects.count()

    job_notification=jobnotification.objects.filter(is_published=True,status='open')

    #applied_jobs = jobapplication.objects.values_list('job_id', flat=True).count()
    #applied_jobs = jobapplication.objects.values('job_id').annotate(applicant_count=Count(''))
    job_notifications = jobnotification.objects.filter(
        is_published=True,
        status='open'
    ).annotate(
        applied_jobs=Count('applications')
    ) 
    context = {
        'active_jobs': active_jobs,
        'inactive_jobs': inactive_jobs,
        'total_applicants': total_applicants,
        'job_notifications': job_notifications,
        
    }
    return render(request, 'dashboards/hr_dashboard.html', context)

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
            location=request.POST.get("location"),
            job_type=request.POST.get("job_type"),
            description=request.POST.get("description"),
            vaccancy_count=int(request.POST.get("vaccancy_count")),
            deadline=request.POST.get("deadline"),
            salary=request.POST.get("salary"),
            experiance=request.POST.get("experiance"),
        )
        return redirect("job_notification")

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
    # Send email notification to user about status change
    html_content = render_to_string('email_templates/status_update.html', {'user': user, 'status': status})
    
    email = EmailMessage(
        subject="Status Update Notification",
        body=html_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
    )
    email.content_subtype = "html"  
    email.send(fail_silently=False)


    messages.success(request, f"{user.username} status updated to {status}")
    return redirect('employee_management')

def update_user_role(request, user_id):
    if request.user.role != 'hr':
        return redirect('login')

    user = get_object_or_404(CustomUser, id=user_id)
    role = request.POST.get('role')

    if role not in ['MOD', 'hr', 'INS_ADMIN', 'general_manager']:
        messages.error(request, "Invalid role")
        return redirect('employee_management')

    user.role = role
    user.save()

    messages.success(request, f"{user.username} role updated to {role}")
    return redirect('employee_management')

@login_required
def general_manager_dashboard(request):
    if request.user.role != 'general_manager':
        return redirect('login')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        Post.objects.create(
            title=title,
            content=content,
            image=image,
            status='hold'
        )

        
        return redirect('general_manager_dashboard')

    posts = Post.objects.all().order_by('-created_at')

    return render(request, 'dashboards/general_manager.html', {
        'posts': posts,
        'published_count': Post.objects.filter(status='publish').count(),
        'pending_count': Post.objects.filter(status='hold').count(),
    })

@login_required
def gm_update_post_status(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "publish":
            post.status = "publish"
            post.save()

            send_post_newsletter(post)


        elif action == "hold":
            post.status = "hold"
            post.save()

    return redirect("general_manager_dashboard")


def delete_post(request,id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('general_manager_dashboard')


def healthy_savings(request):
    post=Post.objects.filter(status='publish').order_by('-created_at')
    context={
        'posts':post
    }
    return render(request, 'healthy_savings.html', context)



@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# the news letter subscribe view in the index page, careee
def newsletter_subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if not email:
            messages.error(request, "Please enter a valid email.")
            return redirect("career")

        if newsletter_subscribers.objects.filter(email=email).exists():
            messages.info(request, "You are already subscribed.")
            return redirect("career")

        newsletter_subscribers.objects.create(email=email)

        html_content = render_to_string(
            'email_templates/newsletter_subscription.html',
            {'email': email}
        )

        mail = EmailMessage(
            subject="Thanks for Subscribing to Our Newsletter",
            body=html_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
        )
        mail.content_subtype = "html"
        mail.send()

        messages.success(request, "Successfully subscribed to the newsletter.")
        return redirect("career")

    return redirect("career")