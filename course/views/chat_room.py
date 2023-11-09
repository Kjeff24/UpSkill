from django.shortcuts import render, redirect
from course.models import Course, Room, Message
from django.http import JsonResponse
from django.conf import settings
import random
import time
import json
from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import timesince

def chatRoom(request, pk2, pk):

    # Retrieve the currently logged-in employee
    employee = request.user

    # Get all courses in which the employee is a participant
    courses = Course.objects.filter(participants__user=employee)

    # Retrieve the course based on the provided primary key
    course = Course.objects.get(id=pk2)

    # Retrieve the room based on the provided primary key
    room = Room.objects.get(id=pk)

    context = {
        'room': room,
        'courses': courses,
        'course': course,
        'page': 'chat-room'
    }

    # Render the chat room template with the context data
    return render(request, "chat/chat_room.html", context)


def sendMessages(request, pk2, pk):
    # Retrieve the room based on the provided primary key
    room = Room.objects.get(id=pk)
    
    if request.method == 'POST':
        # Create a new message associated with the room
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
    
    
    return JsonResponse({'status': 'success'})


def displayMessages(request, pk2, pk):
    # Retrieve the room based on the provided primary key
    try:
        room = Room.objects.get(id=pk)
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Room does not exist'}, status=404)

    # Retrieve all messages associated with the room, ordered by creation time
    room_messages = room.message_set.all().order_by('-created').reverse()

    # Serialize the messages to JSON
    messages = []

    for message in room_messages:
        serialized_message = {
            'id': message.id,
            'user': message.user.username,
            'user_id': message.user.id,
            'avatar': message.user.avatar.url,
            'room': message.room.id,
            'body': message.body,
            'created': timesince(message.created),
        }
        messages.append(serialized_message)


    # Return the serialized messages as JSON response
    return JsonResponse(messages, safe=False)

