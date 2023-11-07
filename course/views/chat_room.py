from django.shortcuts import render, redirect
from course.models import Course, Room, Message, VideoStreamMember
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
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


def videoStream(request, pk):
    channel_name = Room.objects.get(id=pk)
    context = {'channel_name':channel_name}
    return render(request, "chat/video_stream.html", context)


def getToken(request):
    appId = settings.APP_ID
    appCertificate = settings.APP_CERTIFICATE
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = VideoStreamMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = VideoStreamMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    try:
        member = VideoStreamMember.objects.get(
            name=data['name'],
            uid=data['UID'],
            room_name=data['room_name']
        )
        member.delete()
        return JsonResponse('Member deleted', safe=False)
    except VideoStreamMember.DoesNotExist:
        return JsonResponse('Member does not exist', safe=False)

