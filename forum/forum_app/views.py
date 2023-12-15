from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Topic, Post
from django.contrib.auth import login
from django.contrib.auth.models import User


def topic_detail(request):
    topics = Topic.objects.all()
    topic_with_posts = []

    for topic in topics:
        posts = Post.objects.filter(topic_id=str(topic._id))
        topic_with_posts.append({'topic': topic, 'posts': posts})

    return render(request, 'topic_detail.html', {'topics_with_posts': topic_with_posts})


def base(request):
    return render(request, 'base.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.get(username=username)

        print(user)

        if user is not None and user.check_password(password):
            login(request, user)
            return redirect('topic_detail')
        else:
            return render(request, 'login.html', {
                'error': 'Bad login or password'
            })
    else:
        return render(request, 'login.html', {})


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(
            username=username,
            email=email
        ).exists():
            return render(request, 'register.html', {
                'error': 'The username or email address already exists'
            })

        user = User(username=username, email=email, password=password)
        user.save()

        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        if user:
            login(request, user)
            return redirect('topic_detail')
        else:
            return render(request, 'register.html', {
                'error': 'Failed to create user'
            })
    else:
        return render(request, 'register.html')