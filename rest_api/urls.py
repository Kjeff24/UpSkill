from django.urls import path
from .views import (
    CourseListView, CourseDetailView,
    ResourceListView, ResourceDetailView,
    AnnouncementListView, AnnouncementDetailView,
    RoomListView, RoomDetailView,
    MessageListView, MessageDetailView,
    ParticipantsListView, ParticipantsDetailView,
    UserRegister, UserLogin,
    UserLogout, UserView,
)

urlpatterns = [
	path('register', UserRegister.as_view(), name='register'),
	path('login', UserLogin.as_view(), name='login'),
	path('logout', UserLogout.as_view(), name='logout'),
	path('user', UserView.as_view(), name='user'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('resources/', ResourceListView.as_view(), name='resource-list'),
    path('resources/<int:pk>/', ResourceDetailView.as_view(), name='resource-detail'),
    path('announcements/', AnnouncementListView.as_view(), name='announcement-list'),
    path('announcements/<int:pk>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
    path('rooms/', RoomListView.as_view(), name='room-list'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('messages/', MessageListView.as_view(), name='message-list'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('participants/', ParticipantsListView.as_view(), name='participants-list'),
    path('participants/<int:pk>/', ParticipantsDetailView.as_view(), name='participants-detail'),
]
