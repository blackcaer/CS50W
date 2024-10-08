from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    def __str__(self) -> str:
        return f"{self.username} {self.email}: pk={self.pk}"
    

    watchlist = models.ManyToManyField('AuctionListing', related_name="users_watching", blank=True)


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    @classmethod
    def get_none_category(cls):
        none_category, created = cls.objects.get_or_create(name="None")
        return none_category.pk

    def __str__(self) -> str:
        return self.name


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=2048)
    is_active = models.BooleanField(default=True)
    start_bid = models.DecimalField(max_digits=7, decimal_places=2,
                                    verbose_name="Starting bid for auction",
                                    default=1,
                                    validators=[
                                        MaxValueValidator(99999.99),
                                        MinValueValidator(1)
                                    ])
    current_max_bid = models.DecimalField(max_digits=7, decimal_places=2,
                                          verbose_name="Current bid for auction",
                                          validators=[
                                              MaxValueValidator(99999.99),
                                              MinValueValidator(1)
                                          ], blank=True, null=True)
    current_max_bid_user = models.ForeignKey(User,
                                             on_delete=models.CASCADE, related_name='max_bid_auctions', blank=True, null=True)
    img_url = models.URLField(
        max_length=1024, verbose_name="Listing image url", blank=True, null=True)

    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE, related_name='owned_auctions')

    category = models.ForeignKey(Category, on_delete=models.SET(Category.get_none_category), related_name='listings',
                                 default=Category.get_none_category,
                                 blank=False, null=False,
                                 verbose_name="Product category")

    def __str__(self) -> str:
        return f"Auction '{self.title}' max_bid={self.current_max_bid} pk={self.pk}"


class Bid(models.Model):
    pass


class Comment(models.Model):
    pass
