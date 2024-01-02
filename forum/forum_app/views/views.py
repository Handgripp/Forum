from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..repository.user_repository import UserRepository
from ..repository.post_repository import PostRepository
from ..repository.topic_repository import TopicRepository


@login_required()
def topic_detail(request):
    topics = TopicRepository.get_all()
    topic_with_posts = []

    for topic in topics:
        posts = TopicRepository.filter_posts_by_topic_id(str(topic._id))
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
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            user_from_db = UserRepository.get_all()

            if user_from_db.objects.filter(username=username).exists():
                return render(request, 'register.html', {
                    'error': 'The username or email address already exists'
                })

            user = UserRepository.create(username, email, password)

            if user:
                login(request, user)
                messages.success(request, "You create account successfully")
                return redirect('topic_detail')
            else:
                return render(request, 'register.html', {
                    'error': 'Failed to create user'
                })
        else:
            return render(request, 'register.html')
    except Exception as e:
        return render(request, 'register.html', {
            'error': f'{e}'
        })


@login_required()
def post_creator(request, topic_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            PostRepository.create(topic_id, title, content)
            messages.success(request, "You create post successfully")
            return redirect('topic_detail')
        else:

            error_message = "Both title and content are required."
            context = {'topic_id': topic_id, 'error_message': error_message}
            return render(request, 'post_creator.html', context)

    context = {'topic_id': topic_id}
    return render(request, 'post_creator.html', context)
