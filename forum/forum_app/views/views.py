from datetime import datetime, timedelta
import jwt
from django.contrib.auth.password_validation import validate_password
from django.forms import forms
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from ..repository.user_repository import UserRepository
from ..repository.post_repository import PostRepository
from ..repository.topic_repository import TopicRepository
from ..repository.comment_repository import CommentRepository
from django.conf import settings
from ..tasks import send_async_email
from decouple import config


def create_confirmation_token(user):
    expiration_time = datetime.utcnow() + timedelta(hours=48)

    payload = {
        'user_id': str(user._id),
        'username': user.username,
        'email': user.email,
        'exp': expiration_time,
    }

    token = jwt.encode(payload, config("SECRET_KEY"), algorithm='HS256')
    return token


@login_required()
def topic_detail(request):
    topics = TopicRepository.get_all()
    topic_with_posts = []

    for topic in topics:
        posts = TopicRepository.filter_posts_by_topic_id(str(topic._id))
        for post in posts:
            post_id = post._id
        topic_with_posts.append({'topic_id': str(topic._id), 'topic': topic, 'posts': posts})

    return render(request, 'topic_detail.html', {'topics_with_posts': topic_with_posts, 'post_id': post_id})


def base(request):
    return render(request, 'base.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        user_from_db = UserRepository.get_one(username)
        if user_from_db.is_active is False:
            messages.error(request, "Your account is not active. Please click on the link in your email.")
            return redirect('login')
        else:
            if user is not None:
                request.session.set_expiry(600)
                login(request, user)
                messages.success(request, "You have been logged in")
                return redirect('topic_detail')
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('login')
    else:
        return render(request, 'base.html', {})


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            validate_password(password)
        except forms.ValidationError as errors:
            for error in errors:
                messages.error(request, f"{error}")

            return redirect('register')

        exists_email = get_user_model().objects.filter(email=email)

        if len(exists_email) > 0:
            messages.error(request, "The email address already exists")
            return redirect('register')

        exists_username = get_user_model().objects.filter(username=username)

        if len(exists_username) > 0:
            messages.error(request, "The username already exists")
            return redirect('register')

        user = UserRepository.create(username, email, password)

        if user:
            login(request, user)
            messages.success(request, "You create account successfully, confirm your account by clicking the link in your mail")
            confirmation_token = create_confirmation_token(user)
            activation_link = f'http://127.0.0.1:8000/confirm-account/?token={confirmation_token}'
            subject = 'Welcome to Ferrari Forum'
            message = f'Hi {user.username}, thank you for registering in Ferrari Forum. Please confirm your account by clicking the link below:\n\n{activation_link}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['austin.hane20@ethereal.email']
            send_async_email.delay(subject, message, email_from, recipient_list)
            return redirect('topic_detail')
        else:
            messages.error(request, "The username or email address already exists")
            return redirect('register')
    else:
        return render(request, 'register.html')


@login_required()
def post_creator(request, topic_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        topic = TopicRepository.get_one(topic_id)
        if topic is None:
            messages.error(request, "You cannot add a post, the topic does not exist")
            return redirect('topic_detail')
        if title and content:
            if request.user.is_authenticated:
                user = UserRepository.get_one(request.user.username)
                post = PostRepository.create(topic_id, title, str(user._id))
                CommentRepository.create(post, content, str(user._id))
                messages.success(request, "You create post successfully")
                return redirect('topic_detail')
        else:

            error_message = "Both title and content are required."
            messages.error(request, f"{error_message}")
            context = {'topic_id': topic_id, 'error_message': error_message}
            return render(request, 'post_creator.html', context)

    context = {'topic_id': topic_id}
    return render(request, 'post_creator.html', context)


@login_required()
def post_detail(request, post_id):
    if request.method == 'POST':
        text = request.POST.get('text')

        if request.user.is_authenticated:
            user = UserRepository.get_one(request.user.username)
            CommentRepository.create(post_id, text, str(user._id))
            return redirect('post_detail', post_id=post_id)
        else:
            messages.error(request, "Error with session")
            return redirect('post_detail')
    else:
        post = PostRepository.get_post(post_id)
        comments = CommentRepository.get_all(post_id)
        for comment in comments:
            comment.user = UserRepository.get_one_with_id(comment.user_id)

    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'post_id': post_id})


@api_view(['GET'])
def confirm_account(request):
    token = request.query_params.get('token', None)

    if not token:
        messages.error(request, "Token not provided")
        return redirect('base')

    try:
        payload = jwt.decode(token, config("SECRET_KEY"), algorithms=['HS256'])
        user = UserRepository.get_one_with_id(payload['user_id'])
    except jwt.ExpiredSignatureError:
        messages.error(request, "Token has expired")
        return redirect('base')
    except jwt.InvalidTokenError:
        messages.error(request, "Invalid token")
        return redirect('base')

    if not user.is_active:
        UserRepository.change_to_active(user._id)
        messages.success(request, "Account confirmed successfully, please login in below")
        return redirect('base')
    else:
        messages.success(request, "Account already confirmed, please login in below")
        return redirect('base')
