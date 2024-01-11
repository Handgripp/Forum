from django.contrib import admin
from .models import Topic, Post



@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title',)

