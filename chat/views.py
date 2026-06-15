from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message
from login.models import CustomUser

@login_required(login_url='login-view')
def home_view(request):
    # current user ke saare messages
    all_messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    )

    # unique users nikaal jinse baat ki hai
    user_ids = set()
    for msg in all_messages:
        if msg.sender != request.user:
            user_ids.add(msg.sender.id)
        if msg.receiver != request.user:
            user_ids.add(msg.receiver.id)

    chat_users = CustomUser.objects.filter(id__in=user_ids)

    return render(request, 'chat/home.html', {
        'chat_users': chat_users,
    })





@login_required(login_url='login-view')
def conversation_view(request, username):
    other_user = get_object_or_404(CustomUser, username=username)

    # dono ke beech ke messages
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    )

    # messages read mark karo
    Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    # POST - naya message save karo
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        photo = request.FILES.get('photo')

        if text or photo:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                text=text,
                photo=photo
            )
        return redirect('chat:conversation-view', username=username)

    return render(request, 'chat/conversation.html', {
        'other_user': other_user,
        'messages': messages,
    })


@login_required(login_url='login-view')
def search_view(request):
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        results = CustomUser.objects.filter(
            username__icontains=query
        ).exclude(id=request.user.id)  # khud ko exclude karo

    return render(request, 'chat/search.html', {
        'results': results,
        'query': query,
    })