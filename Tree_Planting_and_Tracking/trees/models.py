
from django.db import models
from django.contrib.auth.models import User


# models creation

class Tree(models.Model):
    name = models.CharField(max_length=200)
    second_name = models.CharField(max_length=100, null=True, blank=True)

    description = models.TextField()
    image = models.ImageField(upload_to='trees/', default='images/logo.png')

    location = models.CharField(max_length=200)

    # Only admin can set these fields
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # Track who added the tree
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Contact(models.Model):
        name = models.CharField(max_length=100)
        email = models.EmailField()
        message = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"{self.name} - {self.email}"


