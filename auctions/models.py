from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    name = models.CharField(max_length=64)

class Bid(models.Model):
    pass

class Comment(models.Model):
    pass