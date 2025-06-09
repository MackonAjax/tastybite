from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Cake(models.Model):

    # model for a cake

    image = models.ImageField(upload_to='media/')
    catalog = models.CharField(max_length=100)
    price = models.FloatField(null=True)
    weight = models.FloatField(null=True)


class Orders(models.Model):

    # an order stored in this model

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    cake = models.JSONField()
    delivery_date = models.DateField()
    date_of_order = models.DateTimeField(default=timezone.now)
    location = models.CharField()
    extra_note = models.TextField(null=True)


class Payments(models.Model):

    # payments handling

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Orders, on_delete=models.SET_NULL, null=True)
    date_of_payment = models.DateTimeField(default=timezone.now)
    paid = models.FloatField()
    balance = models.FloatField()


class Profile(models.Model):

    # profile of a user 

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_cakes = models.JSONField(null=True)
    wishlist = models.JSONField(null=True)
    # orders = models.JSONField()


class Comment(models.Model):

    # what customers say about a given cake

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    

class AboutUs(models.Model):

    # what customers say about us

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
