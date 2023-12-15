from django.urls import path, include
from .views import login_view, register_view, topic_detail, base

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', base, name='base'),
    path('topic/', topic_detail, name='topic_detail'),
    path('register/', register_view, name='register'),
]