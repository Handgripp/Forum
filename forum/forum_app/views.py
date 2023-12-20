from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Topic, Post
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


@login_required()
def topic_detail(request):
    topics = Topic.objects.all()
    topic_with_posts = []

    for topic in topics:
        posts = Post.objects.filter(topic_id=str(topic._id))
        topic_with_posts.append({'topic_id': str(topic._id), 'topic': topic, 'posts': posts})

    return render(request, 'topic_detail.html', {'topics_with_posts': topic_with_posts})



def base(request):
    return render(request, 'base.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session.set_expiry(600)
            login(request, user)
            messages.success(request, "You have been logged in")

            return redirect('topic_detail')
        else:
            messages.success(request, "There was an error")
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        User = get_user_model()

        if User.objects.filter(username=username,email=email).exists():
            return render(request, 'register.html', {
                'error': 'The username or email address already exists'
            })

        user = User.objects.create_user(username=username, email=email, password=password)

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


@login_required()
def post_creator(request, topic_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            post = Post(topic_id=topic_id, title=title, content=content)
            post.save()
            return redirect('topic_detail')
        else:

            error_message = "Both title and content are required."
            context = {'topic_id': topic_id, 'error_message': error_message}
            return render(request, 'post_creator.html', context)

    context = {'topic_id': topic_id}
    return render(request, 'post_creator.html', context)


