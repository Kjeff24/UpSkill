from django.urls import path
from .views import (
    CourseListAPIView, CourseDetailAPIView,
    ResourceListAPIView, ResourceDetailAPIView,
    AnnouncementListAPIView, AnnouncementDetailAPIView,
    RoomListAPIView, RoomDetailAPIView,
    MessageListAPIView, MessageDetailAPIView,
    ParticipantsListAPIView, 
    UserRegister, UserLogin,
    UserLogout, UserView, UserChangePasswordAPIView, UserUpdateAPIView,
    QuizListView, QuizDetailView, QuizDataAPIView, QuizSubmissionAPIView, ResultListAPIView
)

urlpatterns = [
	path('register/', UserRegister.as_view(), name='register'),
	path('login/', UserLogin.as_view(), name='login'),
	path('logout/', UserLogout.as_view(), name='logout'),
	path('user/', UserView.as_view(), name='user'),
	path('user/update', UserUpdateAPIView.as_view(), name='user'),
	path('change_password/', UserChangePasswordAPIView.as_view(), name='change-password'),
    path('courses/', CourseListAPIView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailAPIView.as_view(), name='course-detail'),
    path('resources/', ResourceListAPIView.as_view(), name='resource-list'),
    path('resources/<int:pk>/', ResourceDetailAPIView.as_view(), name='resource-detail'),
    path('announcements/', AnnouncementListAPIView.as_view(), name='announcement-list'),
    path('announcements/<int:pk>/', AnnouncementDetailAPIView.as_view(), name='announcement-deatail'),
    path('rooms/', RoomListAPIView.as_view(), name='room-list'),
    path('rooms/<int:pk>/', RoomDetailAPIView.as_view(), name='room-detail'),
    path('messages/', MessageListAPIView.as_view(), name='message-list'),
    path('messages/<int:pk>/', MessageDetailAPIView.as_view(), name='message-detail'),
    path('participants/', ParticipantsListAPIView.as_view(), name='participants-list'),
    path('quizzes/', QuizListView.as_view(), name='quizzes-list'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quizzes-detail'),
    path('quiz/<int:pk>/data/', QuizDataAPIView.as_view(), name='quiz-data-list'),
    path('quiz/<int:pk>/save/', QuizSubmissionAPIView.as_view(), name='quiz-data-save'),
    path('results/', ResultListAPIView.as_view(), name='quiz-data-save'),
]
