from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from .views import custom_404
from employerAdmin.employer_admin import employer_admin_site

# NB exclude admin when hosting app



urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("myapp.urls")),
    path("", include("course.urls")),
    path('employer_admin/', employer_admin_site.urls),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)