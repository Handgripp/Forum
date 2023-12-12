from django.shortcuts import render
from .models import Topic

def topic_detail(request):
    topics = Topic.objects.all()
    return render(request, 'topic_detail.html', {'topics': topics})