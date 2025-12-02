from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import datetime

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


def MOD(request):
    consultations = Consultation.objects.all().order_by('-date')
    return render(request, 'MOD.html', {'consultations': consultations})


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

        # ❌ User not found
        if user is None:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')

        # ❌ User has no role → do NOT allow login
        if not hasattr(user, 'role') or user.role == "" or user.role is None:
            messages.error(request, 'You are not allowed to log in.')
            return render(request, 'login.html')

        # 🔥 MOD login
        if user.role == 'MOD':
            login(request, user)
            return render(request, 'MOD.html')

        # 🔥 Insurance Admin login
        elif user.role == 'INS_ADMIN':
            login(request, user)
            return render(request, 'insurance_admin.html')

        # ❌ Any unknown role
        else:
            messages.error(request, 'Unauthorized role.')
            return render(request, 'login.html')

    return render(request, 'login.html')
    