from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('MOD', 'mod'),
        ('hr', 'HR'),
        ('INS_ADMIN', 'Insurance_Administrator'),
        ('general_manager', 'General_Manager'),
    )
    status_choices = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('hold', 'On Hold'),
    )

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=20, choices=status_choices, default='inactive')
    
    # role field
    #date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='MOD')

    def __str__(self):
        return f"{self.username} - {self.role} - {self.status} - {self.full_name}"

# In your app's models.py file
class Appointment(models.Model):
    full_name = models.CharField(max_length=100)
    insurance_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    policy_start_date = models.DateField()
    email = models.EmailField()
    file = models.FileField(upload_to='documents/', null=True, blank=True)

    def __str__(self):
        return self.full_name # Fixed: Added return value for __str__

    @property 
    def file_type(self):
        """Determines if the uploaded file is an image, pdf, or other."""
        if not self.file:
            return None
        
        # Get the file extension in lowercase
        file_url = self.file.url.lower()
        
        if file_url.endswith('.pdf'):
            return 'pdf'
        elif file_url.endswith(('.jpg', '.jpeg', '.png')):
            return 'image'
        else:
            return 'other'
 
# class doctor(models.Model):
#     name = models.CharField(max_length=100)
#     specialization = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone = models.CharField(max_length=15)

#     def __str__(self):
#         return f"Dr. {self.name} - {self.specialization}"
    

class Consultation(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('responded', 'Responded'),
    )
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    specialist = models.CharField(max_length=100)
    reason = models.TextField()
    responded_by=models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True,on_delete=models.SET_NULL,limit_choices_to={'role': 'MOD'})
    responded_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='pending')
    def __str__(self):

        return f"{self.name} - {self.specialist} at {self.time}"


class InsuranceNotes(models.Model):
    insurance = models.ForeignKey(Appointment,on_delete=models.CASCADE,related_name="notes")
    admin_name = models.CharField(max_length=100)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin_name} - {self.created_at.strftime('%d %b %Y %I:%M %p')}"
    


class jobnotification(models.Model):
    status_choices = (
        ('open', 'Open'),
        ('closed', 'Closed'),
    )
    experiance_choices = (
        ('Fresher', 'Fresher'),
        ('1-3 years', '1-3 years'),
        ('3-5 years', '3-5 years'),
        ('5+ years', '5+ years'),
    )
    job_type=(
        ('full-time','Full-Time'),
        ('part-time','Part-Time'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    job_type = models.CharField(max_length=20, choices=job_type, default='full-time')
    location = models.CharField(max_length=100)
    vaccancy_count = models.IntegerField()
    status = models.CharField(max_length=10, choices=status_choices, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()
    salary = models.CharField(max_length=100)
    is_published = models.BooleanField(default=False)
    experiance=models.CharField(max_length=20, choices=experiance_choices, default='Fresher')

    def __str__(self):
        return self.title
    

class jobapplication(models.Model):
    job = models.ForeignKey(jobnotification, on_delete=models.CASCADE, related_name="applications")
    applicant_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant_name} - {self.job.title}"
    


class Post(models.Model):

    action=[
        ('hold','Hold'),
        ('publish','Publish'),
    ]
    status=models.CharField(max_length=10,choices=action,default='hold')
    title = models.CharField(max_length=200)
    image= models.ImageField(upload_to='post_images/')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    




class newsletter_subscribers(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email