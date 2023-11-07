from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from .views import front_page

# app_name = 'myapp'

urlpatterns = [
    path('', front_page.home, name='home'),
]