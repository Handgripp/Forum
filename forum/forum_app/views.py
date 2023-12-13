from django.shortcuts import render
from .models import Topic, Post

def topic_detail(request):
    topics = Topic.objects.all()
    topic_with_posts = []

    for topic in topics:
        posts = Post.objects.filter(topic_id=str(topic._id))
        topic_with_posts.append({'topic': topic, 'posts': posts})

    return render(request, 'topic_detail.html', {'topics_with_posts': topic_with_posts})
