from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    following = models.ManyToManyField(
        'self', symmetrical=False, related_name='followers')

    def serialize(self):
       
        return {
            "id": self.id,
            "username": self.username
        }
    

    def __str__(self) -> str:
        return f"User {self.username} {self.email} (pk={self.pk})"


class Post(models.Model):
    content = models.CharField(max_length=2048)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    date_created = models.DateTimeField(auto_now_add=True)
    users_liking = models.ManyToManyField(User,related_name='liked_posts')

    def get_likes_count(self):
        return self.users_liking.count()
    
    def serialize(self):
        users_liking = self.users_liking.all()
        return {
            "id": self.id,
            "author": self.author.serialize(),
            "users_liking": [user.username for user in users_liking],
            "content": self.content,
            "date_created": self.date_created.strftime("%b %d %Y, %I:%M %p"),
        }
    
    def __str__(self) -> str:
        return f"Post by {self.author.username} likes: {self.get_likes_count()} pk: {self.pk} '{self.content[:50]}'"
