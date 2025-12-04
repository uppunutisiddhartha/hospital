from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('MOD', 'mod'),
        ('INS_ADMIN', 'Insurance_Administrator'),
    )

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    
    # role field
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='MOD')

    def __str__(self):
        return f"{self.username} - {self.role}"

"""
class Appointment(models.Model):
    full_name = models.CharField(max_length=100)
    insurance_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    policy_start_date = models.DateField()
    file = models.FileField(upload_to='documents/', null=True, blank=True)

    def __str__(self):
        return self.full_name
"""
# In your app's models.py file

from django.db import models

class Appointment(models.Model):
    full_name = models.CharField(max_length=100)
    insurance_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    policy_start_date = models.DateField()
    file = models.FileField(upload_to='documents/', null=True, blank=True)

    def __str__(self):
        return self.full_name # Fixed: Added return value for __str__

    @property # Crucial for the template to access this as a property (item.file_type)
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
 
class doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"
    

class Consultation(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    specialist = models.CharField(max_length=100)
    reason = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.specialist} at {self.time}"
