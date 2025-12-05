from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import datetime,date
from calendar import monthrange

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
"""def MOD(request):
    # 1. Selected date or today
    selected_date = request.GET.get("date")
    today = date.today()

    # If user clicked a date
    if selected_date:
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
        year = selected_date.year
        month = selected_date.month
    else:
        # Default: current month
        year = today.year
        month = today.month

    # 2. Get total days in month
    total_days = monthrange(year, month)[1]

    # 3. Build list of all dates of the month
    days_list = [date(year, month, d) for d in range(1, total_days + 1)]

    # 4. All consultations in this month
    month_consults = Consultation.objects.filter(date__year=year, date__month=month)

    # Dates that have consultations
    active_dates = {c.date for c in month_consults}

    # 5. If user clicked specific date
    if selected_date:
        consultations = Consultation.objects.filter(date=selected_date)
    else:
        consultations = []

    return render(request, "MOD.html", {
        "days_list": days_list,
        "active_dates": active_dates,
        "consultations": consultations,
        "selected_date": selected_date,
        "current_month": f"{year}-{month:02d}",
    })
"""
from datetime import date, datetime
from calendar import monthrange
from django.shortcuts import render
from .models import Consultation

def MOD(request):
    today = date.today()
    selected_date_str = request.GET.get("date")  # from input or calendar button
    selected_date = None

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

    return render(request, "MOD.html", {
        "days_list": days_list,
        "active_dates": active_dates,
        "consultations": consultations,
        "selected_date": selected_date,
        "current_month": f"{year}-{month:02d}",
    })




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
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')

        if not hasattr(user, 'role'):
            messages.error(request, 'You are not allowed to log in.')
            return render(request, 'login.html')

        if user.role == 'MOD':
            login(request, user)
            return redirect('MOD')

        elif user.role == 'INS_ADMIN':
            login(request, user)
            return redirect('insurance_admin')

        else:
            messages.error(request, 'Unauthorized role.')
            return render(request, 'login.html')

    return render(request, 'login.html')
    