from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# These are the database models 
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default =  timezone.now) # now is a function but we do dont want to return a value we want to pass the function
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):# Search for this magic function and OOP in Python
        return self.title
