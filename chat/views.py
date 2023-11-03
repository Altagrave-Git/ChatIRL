from django.shortcuts import render, redirect
from chat.models import ChatRoom
from chat.serializers import ChatRoomSerializer
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
    
    serializer = ChatRoomSerializer(room)
    context = serializer.data
    return render(request, 'chat/room.html', context=context)