from django.urls import path
from . import views


urlpatterns = [
   path('', views.index, name='index'),
   path('pre_consultation/', views.pre_consultation, name='pre_consultation'),
   path('doctors/', views.doctors, name='doctors'),
   path('login/', views.login_view, name='login'),
   path('MOD/', views.MOD, name='MOD'),
   path('insurance_admin/', views.insurance_admin, name='insurance_admin'),
   path('insurance_list/', views.insurance_list, name='insurance_list'),
   path('save-insurance-note/', views.save_insurance_note, name='save_insurance_note'),
   path('hr/', views.hr_dashboard, name='hr_dashboard'),
   path('hr/update-status/<int:user_id>/', views.update_user_status, name='update_user_status'),
   ]
