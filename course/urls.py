from django.urls import path
from .views import announcement_page, course_page, resource_page, room_page
from .views import chat_room, quiz_page, profile_page


urlpatterns = [
    path('course/<str:pk>/', course_page.coursePage, name='course'),
    path('all_events/<str:pk>/', course_page.all_events, name='all_events'),
    path('course/<str:pk>/resource', resource_page.resourcePage, name='resource'),
    path('resource/<int:pk>/download/', resource_page.downloadFile, name='increment_downloads'),
    path('preview_pdf/<int:pk>/', resource_page.previewPdf, name='preview_pdf'),
    path('course/<str:pk>/announcement', announcement_page.announcementPage, name='announcement'),
    path('course/<str:pk>/chat_room', room_page.roomPage, name='room-page'),
    path('course/<str:pk>/quiz_page', quiz_page.quizPage, name='quiz-page'),
    path('course/<str:pk2>/chat_room/<str:pk>/', chat_room.chatRoom, name='chat-room'),
    path('course/<str:pk2>/chat_room/<str:pk>/send-message', chat_room.sendMessages, name='send-message'),
    path('course/<str:pk2>/chat_room/<str:pk>/get-messages', chat_room.displayMessages, name='get-messages'),
    path('profile/<str:pk>/', profile_page.profile, name='profile'),
]