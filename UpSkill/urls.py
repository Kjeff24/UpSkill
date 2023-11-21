from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from .views import custom_404
from employerAdmin.employer_admin import tutor_admin_site
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
# NB exclude admin when hosting app

schema_view = get_schema_view(
   openapi.Info(
      title="UPSKILL",
      default_version='v1',
      description="UPSKILL",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="upskill@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("api/", include("rest_api.urls")),
    path("", include("myapp.urls")),
    path("", include("course.urls")),
    path("", include("quiz.urls")),
    path('tutor_admin/', tutor_admin_site.urls),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)