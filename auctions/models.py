from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    def __str__(self) -> str:
        return f"{self.username} {self.email}: pk={self.pk}"

    watchlist = models.ManyToManyField(
        'AuctionListing', related_name="users_watching", blank=True)


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
    # current_max_bid = models.DecimalField(max_digits=7, decimal_places=2,
    #                                       verbose_name="Current bid for auction",
    #                                       validators=[
    #                                           MaxValueValidator(99999.99),
    #                                           MinValueValidator(1)
    #                                       ], blank=True, null=True)
    # current_max_bid_user = models.ForeignKey(User,
    #                                          on_delete=models.CASCADE, related_name='max_bid_auctions',
    #                                          blank=True, null=True)
    img_url = models.URLField(
        max_length=1024, verbose_name="Listing image url", blank=True, null=True)

    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE, related_name='owned_auctions')

    category = models.ForeignKey(Category, on_delete=models.SET(Category.get_none_category),
                                 related_name='auctions', default=Category.get_none_category,
                                 blank=False, null=False,
                                 verbose_name="Product category")

    def __str__(self) -> str:
        return f"Auction '{self.title}' category:{self.category} owner:{self.owner} ({self.pk})"


class Bid(models.Model):
    price = models.DecimalField(max_digits=7, decimal_places=2,
                                validators=[
                                    MaxValueValidator(99999.99),
                                    MinValueValidator(1)
                                ], default=1, blank=False, null=False)
    auction = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name='bids', blank=False, null=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bids',
                                verbose_name='User who placed bid', blank=False, null=True)
    def __str__(self) -> str:
        return f"Bid for {self.price} on '{self.auction.title}' by {self.user.username} ({self.pk})"

class Comment(models.Model):
    content = models.CharField(max_length=1024,default="",blank=False)
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE,
                                   related_name='comments',
                                   verbose_name="Commented auction",
                                   blank=False, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='user_comments', verbose_name='User who wrote the comment', blank=False, null=True)
    def __str__(self) -> str:
        return f"Comment on '{self.auction.title}' by {self.user.username} ({self.pk})"