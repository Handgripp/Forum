from bson import ObjectId

from ..models import Post


class PostRepository:
    @staticmethod
    def create(topic_id, title):
        post = Post(topic_id=topic_id, title=title)
        post.save()
        return post._id

    @staticmethod
    def get_post(post_id):
        post = Post.objects.filter(_id=ObjectId(post_id)).first()
        return post

    @staticmethod
    def get_post_with_topic_id(topic_id):
        post = Post.objects.filter(topic_id=topic_id).first()
        return post._id if post else None
