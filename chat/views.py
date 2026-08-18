from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Message


def _get_user_avatar(user):
    try:
        if hasattr(user, 'profile') and user.profile and user.profile.avatar:
            return user.profile.avatar.url
    except Exception:
        pass
    return None


@login_required
def chat_list_view(request):
    users = User.objects.exclude(id=request.user.id)
    users_with_avatars = [
        {'user': u, 'avatar_url': _get_user_avatar(u)}
        for u in users
    ]
    return render(request, 'chat/chat_list.html', {'users': users_with_avatars})


@login_required
def chat_room_view(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    return render(request, 'chat/chat_room.html', {'receiver': receiver})


@login_required
def get_messages(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=receiver) |
        Q(sender=receiver, receiver=request.user)
    ).order_by('created_at')

    data = []
    for msg in messages:
        if msg.receiver == request.user and not msg.is_read:
            msg.is_read = True
            msg.save(update_fields=['is_read'])

        image_url = None
        if msg.image:
            try:
                image_url = msg.image.url
            except ValueError:
                image_url = None

        data.append({
            'id': msg.id,
            'sender': msg.sender.username,
            'sender_avatar': _get_user_avatar(msg.sender),
            'text': msg.text or "",
            'image_url': image_url,
            'time': msg.created_at.strftime('%H:%M'),
            'is_me': msg.sender == request.user
        })
        
    return JsonResponse({'status': 'ok', 'messages': data})


@login_required
def send_message(request, receiver_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    receiver = get_object_or_404(User, id=receiver_id)
    text = request.POST.get('text', '').strip()
    image = request.FILES.get('image')
    
    if text or image:
        msg = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            text=text,
            image=image
        )
        return JsonResponse({
            'status': 'ok',
            'message': {
                'id': msg.id,
                'text': msg.text,
                'time': msg.created_at.strftime('%H:%M'),
                'is_me': True
            }
        })
        
    return JsonResponse({'status': 'error', 'message': 'Empty message'}, status=400)