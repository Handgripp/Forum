from ..models import Comment


class CommentRepository:
    @staticmethod
    def create(post_id, text, user_id):
        comment = Comment(post_id=post_id, text=text, user_id=user_id)
        comment.save()
        return comment
    @staticmethod
    def get_all(post_id):
        comments = Comment.objects.filter(post_id=post_id)
        return comments