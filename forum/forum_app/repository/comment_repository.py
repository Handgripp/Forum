from ..models import Comment


class CommentRepository:
    @staticmethod
    def create(post_id, text):
        comment = Comment(post_id=post_id, text=text)
        comment.save()
        return comment
    @staticmethod
    def get_all(post_id):
        comments = Comment.objects.filter(post_id=post_id)
        return comments