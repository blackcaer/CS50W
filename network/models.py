from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    def __str__(self) -> str:
        return f"User {self.username} {self.email} (pk={self.pk})"


class Post(models.Model):
    content = models.CharField(max_length=2048)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    date_created = models.DateTimeField(auto_now_add=True)
    users_liking = models.ManyToManyField(User,related_name='liked')
    def get_likes_count(self):
        return self.users_liking.count()
    def __str__(self) -> str:
        return f"Post by {self.author.username} likes: {self.get_likes_count()} pk: {self.pk} '{self.content[:50]}'"



#posts, likes, and followers.