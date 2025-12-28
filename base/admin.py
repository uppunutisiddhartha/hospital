from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {
            'fields': ('role', 'status'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {
            'fields': ('role', 'status'),
        }),
    )

    list_display = ('username', 'email', 'role', 'status', 'is_active')
    list_filter = ('role', 'status', 'is_active')
    search_fields = ('username', 'email', 'full_name')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Appointment)
#admin.site.register(doctor)
admin.site.register(Consultation)
admin.site.register(InsuranceNotes)
admin.site.register(jobnotification)
admin.site.register(jobapplication)
admin.site.register(Post)
admin.site.register(newsletter_subscribers)
