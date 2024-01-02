from ..models import Topic, Post


class TopicRepository:
    @staticmethod
    def get_all():
        topics = Topic.objects.all()
        return topics

    @staticmethod
    def filter_posts_by_topic_id(topic_id):
        posts = Post.objects.filter(topic_id=topic_id)
        return posts