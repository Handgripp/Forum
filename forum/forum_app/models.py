from djongo import models


class Topic(models.Model):
    _id = models.ObjectIdField()
    title = models.CharField(max_length=255)
    description = models.TextField()


class Post(models.Model):
    _id = models.ObjectIdField()
    topic_id = models.CharField(max_length=20)
    title = models.CharField(max_length=255)


class Comment(models.Model):
    _id = models.ObjectIdField()
    post_id = models.CharField(max_length=20)
    text = models.CharField(max_length=255)
