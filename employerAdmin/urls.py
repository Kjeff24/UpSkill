from django.urls import path, include
from .employer_admin import employer_admin_site

# distinguish between different applications in cases where multiple applications have URL patterns with the same name.
app_name = 'tutor_admin'
