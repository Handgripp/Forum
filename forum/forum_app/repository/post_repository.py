from ..models import Post


class PostRepository:
    @staticmethod
    def create(topic_id, title, content):
        post = Post(topic_id=topic_id, title=title, content=content)
        post.save()
        return post
