from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=2048)
    start_bid = models.DecimalField(max_digits=7,decimal_places=2,
                                    verbose_name="Starting bid for auction(verbose)",
                                    default=1,
                                    validators=[
                                        MaxValueValidator(99999.99),
                                        MinValueValidator(1)
                                    ])
    img_url = models.URLField(max_length=64,verbose_name="Listing image url",blank=True,null=True)
    category = models.CharField(max_length=64,verbose_name="Product category",blank=True,null=True)
    
    
class Bid(models.Model):
    pass

class Comment(models.Model):
    pass