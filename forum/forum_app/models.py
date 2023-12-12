import uuid
from djongo import models


class Topic(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
