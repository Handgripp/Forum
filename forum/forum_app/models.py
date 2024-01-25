from djongo import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    _id = models.ObjectIdField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Topic(models.Model):
    _id = models.ObjectIdField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Post(models.Model):
    _id = models.ObjectIdField()
    topic_id = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    user_id = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    _id = models.ObjectIdField()
    post_id = models.CharField(max_length=20)
    text = models.CharField(max_length=255)
    user_id = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
