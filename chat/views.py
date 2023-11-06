from django.shortcuts import render, redirect
from users.models import User
from users.serializers import UserSerializer
from chat.models import ChatRoom, ChatMessage, PrivateChat, PrivateMessage
from chat.serializers import ChatRoomSerializer, ChatMessageSerializer, PrivateChatSerializer, PrivateMessageSerializer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify


@login_required
def index(request):
    sticky = ChatRoom.objects.filter(sticky=True)
    member = ChatRoom.objects.filter(users=request.user).exclude(sticky=True)

    context = {
        "sticky": ChatRoomSerializer(sticky, many=True).data,
        "member": ChatRoomSerializer(member, many=True).data
    }

    return render(request, 'chat/index.html', context=context)


@login_required
def create_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')

        if not title:
            messages.error(request, 'Input room name')
            return redirect('create_room')
        
        room = ChatRoom.objects.filter(slug=slugify(str(title)))
        if room.exists():
            messages.error(request, 'Room already exists')
            return redirect('create_room')
        
        room = ChatRoom(title=title)
        room.save()
        room.users.add(request.user)

        return redirect('room', slug=room.slug)

    else:
        return render(request, 'chat/create_room.html')
    

def room_view(request, slug):
    try:
        room = ChatRoom.objects.get(slug=slug)
    except:
        return redirect('home')
    
    room_serializer = ChatRoomSerializer(room)
    room_messages = room.messages.all()
    if len(room_messages) > 50:
        room_messages.order_by('-id')[50:].delete()
    message_serializer = ChatMessageSerializer(room_messages, many=True)

    sticky = ChatRoom.objects.filter(sticky=True)
    member = ChatRoom.objects.filter(users=request.user).exclude(sticky=True)
    
    context = {
        "chat_room": room_serializer.data,
        "chat_messages": message_serializer.data,
        "sticky": ChatRoomSerializer(sticky, many=True).data,
        "member": ChatRoomSerializer(member, many=True).data
    }

    return render(request, 'chat/room.html', context=context)


@login_required
def private_list_view(request):
    private_rooms = PrivateChat.objects.filter(users=request.user)
    if private_rooms.exists():
        room_serializer = PrivateChatSerializer(private_rooms, many=True).data
    else:
        room_serializer = None

    context = {
        'private_rooms': room_serializer
    }

    return render(request, 'chat/private_list.html', context=context)


@login_required
def private_chat_view(request, username):
    user = request.user
    try:
        target_user = User.objects.get(username=username)
    except:
        return redirect('home')
    
    try:
        room = PrivateChat.objects.filter(users__in=[user, target_user])
        room_messages = room[0].messages.all()
        message_serializer = PrivateMessageSerializer(room_messages, many=True).data
    except:
        message_serializer = None

    context = {
        'target_user': UserSerializer(target_user).data,
        'chat_messages': message_serializer,
    }

    return render(request, 'chat/private.html', context=context)