from django.urls import path
from .views.views import login_view, register_view, topic_detail, base, post_creator, post_detail

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', base, name='base'),
    path('topic/', topic_detail, name='topic_detail'),
    path('register/', register_view, name='register'),
    path('post_creator/<str:topic_id>/', post_creator, name='post_creator'),
    path('post/<str:post_id>/', post_detail, name='post_detail'),
]