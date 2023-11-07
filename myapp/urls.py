from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from .views import authentication_page, front_page, users_page, user_management

# app_name = 'myapp'

urlpatterns = [
    path('', front_page.home, name='home'),
    path('about/', front_page.about, name='about'),
    path('contact/', front_page.contact, name='contact'),
    path('login/', authentication_page.loginPage, name='login'),
    path('logout/', authentication_page.logoutUser, name='logout'),
    path('employee_signup/', authentication_page.employeeSignupPage, name='employee-signup'),
    path('employer_signup/', authentication_page.employerSignupPage, name='employer-signup'),
    path('activate-user/<uidb64>/<token>', authentication_page.activate_user, name='activate'),
    path('employee_home/<str:pk>/', users_page.employeeHome, name='employee-home'),
    path('enrollment_success/', users_page.enrollmentSuccess, name='enrollment-success'),
    path('update_user/<str:pk>/', user_management.updateUser, name='update-user'),
    
    path(
        'reset_password/', 
        auth_views.PasswordResetView.as_view(template_name="password/password_reset.html"), 
        name='password_reset'
    ),
    path(
        'reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="password/password_reset_sent.html"), 
        name='password_reset_done'),
    path(
        'reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_form.html"), 
        name='password_reset_confirm'),
    path(
        'reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="password/password_reset_done.html"), 
        name='password_reset_complete'),
    
]