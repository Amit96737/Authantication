from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from users.models.users import User

@login_required
def chat_room(request, room_name):
    current_user_id = str(request.user.id)
    other_user_id = str(room_name)

    other_user = None

    if other_user_id != 'global':
        sorted_ids = sorted([current_user_id, other_user_id])
        unique_room_name = f"room_{sorted_ids[0]}_{sorted_ids[1]}"

        try:
            other_user = User.objects.get(id=room_name)
        except User.DoesNotExist:
            other_user = None

    else:
        unique_room_name = 'global'

    old_messages = ChatMessage.objects.filter(room_name=unique_room_name)

    return render(request, 'web_chat/room.html', {
        'room_name': unique_room_name,
        'old_messages': old_messages,
        'other_user': other_user
    })