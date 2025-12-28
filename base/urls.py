from django.urls import path
from . import views


urlpatterns = [
   path('', views.index, name='index'),
   path('pre_consultation/', views.pre_consultation, name='pre_consultation'),
   path('register/', views.register, name='register'),
   path('login/', views.login_view, name='login'),
   path('MOD/', views.MOD, name='MOD'),
   path('insurance_admin/', views.insurance_admin, name='insurance_admin'),
   path('insurance_list/', views.insurance_list, name='insurance_list'),
   path('save-insurance-note/', views.save_insurance_note, name='save_insurance_note'),
   path('hr/', views.hr_dashboard, name='hr_dashboard'),
   path('employee-management/', views.employemanagement, name='employee_management'),
   path('hr/update-status/<int:user_id>/', views.update_user_status, name='update_user_status'),
   path('career/', views.career, name='career'),
   path('create-job/', views.create_job, name='create_job'),
   path('job-notification/', views.job_notification, name='job_notification'),
   #path('update-job-status/<int:job_id>/', views.update_job_status, name='update_job_status'),
   path('jobs/publish/<int:id>/', views.publish_job, name='publish_job'),
   path('jobs/unpublish/<int:id>/', views.unpublish_job, name='unpublish_job'),
   path('jobs/delete/<int:id>/', views.delete_job, name='delete_job'),
   path('hr/applications/', views.hr_all_applications, name='hr_all_applications'),
   path('general-manager-dashboard/', views.general_manager_dashboard, name='general_manager_dashboard'),
   path('gm/post/status/<int:post_id>/', views.gm_update_post_status, name='gm_update_post_status'),
   path('gm/post/delete/<int:id>/', views.delete_post, name='delete_post'),
   path('healthy-savings/', views.healthy_savings, name='healthy_savings'),
   path('update_user_role/<int:user_id>/', views.update_user_role, name='update_user_role'),
   path('logout/', views.logout_view, name='logout'),
   #path('main_admin/', views.main_admin, name='main_admin'),
   path('mod/respond/<int:consultation_id>/', views.respond_consultation, name='respond_consultation'),
   path('newsletter/subscribe/', views.newsletter_subscribe, name='subscribe_newsletter'),
]
   

