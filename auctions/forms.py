from django.forms import ModelForm
from django import forms

from .models import AuctionListing, Comment, Bid


class AuctionListingCreateFrom(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'start_bid', 'img_url', 'category']
        widgets = {'title': forms.TextInput(attrs={
            'class': 'form-control form-group',
            'autofocus': True,
            'placeholder': 'Title'
        }),
            'description': forms.Textarea(attrs={
                'class': 'form-control form-group',
                'rows': 10,
                'placeholder': 'Description of your listing'
            }),
            'start_bid': forms.TextInput(attrs={
                'class': 'form-control form-group',
                'placeholder': 'Starting bid',
                'type': 'number',
                'min': 1,
                'max': 99999.99,
                'step': 0.01
            }),
            'img_url': forms.TextInput(attrs={
                'class': 'form-control form-group',
                'placeholder': 'Image url for your listing'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control form-group'
            })

        }


class CreateCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control form-group',
                'placeholder': 'Write your comment',
                'rows': 4, 'cols': 40})
        }
        labels = {
            'content': ''
        }


class CreateBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['price']
        widgets = {
            'price': forms.TextInput(attrs={
                'class': 'form-control form-group',
                'placeholder': 'Starting bid',
                'type': 'number',
                'min': 1,
                'max': 99999.99,
                'step': 0.01
            }),
        }
        labels = {
            'price': ''
        }
