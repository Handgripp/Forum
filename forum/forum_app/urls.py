from django.urls import path
from .views import login_view, register_view, topic_detail, base, post_creator

urlpatterns = [
    path('login/', login_view, name='login'),
    path('', base, name='base'),
    path('topic/', topic_detail, name='topic_detail'),
    path('register/', register_view, name='register'),
    path('post_creator/<str:topic_id>/', post_creator, name='post_creator')

]