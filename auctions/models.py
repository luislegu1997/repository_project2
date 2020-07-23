from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone



class User(AbstractUser):
    pass

class Listing(models.Model):
    Title = models.CharField(max_length=60)
    Price = models.DecimalField(decimal_places=2, max_digits=8)
    Description = models.TextField()
    categories = (('Home','Home'),('Fashion','Fashion'),('Jewlelery','Jewlelery'),('Electronics','Electronics'),('Toys','Toys'),('Other','Other'))
    Category = models.CharField(max_length=16, choices=categories, blank=True)
    time= models.DateField("date added", auto_now_add=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    imgURL= models.URLField(blank=True, max_length=200)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name='winner')

    def __str__(self):
        return self.Title

class Bid(models.Model):
   Value = models.DecimalField(max_digits=10, decimal_places=2)
   user= models.ForeignKey(User, on_delete=models.CASCADE)
   listing = models.ForeignKey('Listing', on_delete=models.CASCADE)


class Comment(models.Model):
    entry = models.TextField()
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    