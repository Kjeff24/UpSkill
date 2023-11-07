from django.urls import path
from .views import quiz_view, quiz_data_view, save_quiz_view, quiz_list_view

# distinguish between different applications in cases where multiple applications have URL patterns with the same name.
app_name = 'quizes'

urlpatterns = [
    path('course/<str:pk2>/quiz/', quiz_list_view, name='main-view'),
    path('course/<str:pk2>/quiz/<pk>/', quiz_view, name='quiz-view'),
    path('course/<str:pk2>/quiz/<pk>/save/', save_quiz_view, name='save-view'),
    path('course/<str:pk2>/quiz/<pk>/data/', quiz_data_view, name='quiz-data-view'),
]