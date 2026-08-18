from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Max
from .models import Message

@login_required
def chat_list_view(request):
    users = User.objects.exclude(id=request.user.id)
    
    users_with_avatars = []
    for u in users:
        avatar_url = None
        # Перевіряємо, чи є у користувача профіль та аватарка
        if hasattr(u, 'profile') and u.profile and u.profile.avatar:
            avatar_url = u.profile.avatar.url
        elif hasattr(u, 'userprofile') and u.userprofile and u.userprofile.avatar:
            avatar_url = u.userprofile.avatar.url
            
        users_with_avatars.append({
            'user': u,
            'avatar_url': avatar_url
        })

    return render(request, 'chat/chat_list.html', {'users': users_with_avatars})

@login_required
def chat_room_view(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    users = User.objects.exclude(id=request.user.id)
    
    users_with_avatars = []
    for u in users:
        avatar_url = None
        if hasattr(u, 'profile') and u.profile and u.profile.avatar:
            avatar_url = u.profile.avatar.url
        elif hasattr(u, 'userprofile') and u.userprofile and u.userprofile.avatar:
            avatar_url = u.userprofile.avatar.url
            
        users_with_avatars.append({
            'user': u,
            'avatar_url': avatar_url
        })

    context = {
        'receiver': receiver,
        'users': users_with_avatars,
    }
    return render(request, 'chat/chat_room.html', context)

@login_required
def get_messages(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=receiver) |
        Q(sender=receiver, receiver=request.user)
    )

    data = []
    for msg in messages:
        if msg.receiver == request.user and not msg.is_read:
            msg.is_read = True
            msg.save(update_fields=['is_read'])

        sender_avatar = msg.sender.profile.avatar.url if hasattr(msg.sender, 'profile') and msg.sender.profile.avatar else None

        data.append({
            'sender': msg.sender.username,
            'sender_avatar': sender_avatar,
            'text': msg.text if msg.text else "",
            'image_url': msg.image.url if msg.image else None,
            'time': msg.created_at.strftime('%H:%M'),
            'is_me': msg.sender == request.user
        })
    return JsonResponse(data, safe=False)

@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        image = request.FILES.get('image')
        
        if text or image:
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                text=text,
                image=image
            )
            return JsonResponse({'status': 'ok'})
            
    return JsonResponse({'status': 'error'}, status=400)