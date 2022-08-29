from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    pass

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.TextField()
    date = models.DateField(default=datetime.datetime.now())

    def __str__(self):
        return f"({ self.user.username },{ self.date }) :\n{ self.comment}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.IntegerField()
    date = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return f" ( {self.user.username } at {self.date} ) Bid : { self.bid } "

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    description = models.TextField()
    image_url = models.TextField()
    starting_bid = models.IntegerField(default=0)
    date = models.DateField(datetime.datetime.now())
    isclosed = models.BooleanField(default=False)
    comments = models.ManyToManyField(Comment , blank = True)
    bids = models.ManyToManyField(Bid , blank = True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE , related_name='winners')


class Watch_list(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,default=None)

    def __str__(self):
        return f'{ self.user.username } watch list : \n { self.listing }'