from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from users.models.users import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

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

@csrf_exempt
def upload_chat_audio(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
        room_name = request.POST.get('room_name')

        chat_msg = ChatMessage.objects.create(
            user=request.user,
            room_name=room_name,
            message_type='audio',
            audio_file=audio_file,
            message='[Voice Note]'
        )

        return JsonResponse({
            'status': 'success',
            'audio_url': chat_msg.audio_file.url,
            'message_id': chat_msg.id
        })
    return JsonResponse({'status': 'failed'}, status=400)


def upload_file(request):
    if request.method == 'POST':
        try:
            if 'file' not in request.FILES:
                return JsonResponse({'status': 'error', 'error': 'file not found in request'}, status=400)

            uploaded_file = request.FILES['file']
            room_name = request.POST.get('room_name', 'global')

            ext = os.path.splitext(uploaded_file.name)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                msg_type = 'image'
            elif ext in ['.mp3', '.wav', '.m4a', '.ogg']:
                msg_type = 'audio'
            elif ext == '.pdf':
                msg_type = 'pdf'
            elif ext in ['.xls', '.xlsx', '.csv']:
                msg_type = 'excel'
            else:
                msg_type = 'file'

            chat_message = ChatMessage.objects.create(
                user=request.user,
                room_name=room_name,
                message=uploaded_file.name,
                message_type=msg_type,
                audio_file=uploaded_file
            )

            return JsonResponse({
                'status': 'success',
                'file_name': uploaded_file.name,
                'message_type': msg_type,
                'file_url': chat_message.audio_file.url
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'error': 'Invalid request method'}, status=405)

