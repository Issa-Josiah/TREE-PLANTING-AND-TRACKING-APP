from django.db import models
from django.contrib.auth.models import User
from trees.models import Tree

class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='sponsors/')
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name



class Payment(models.Model):
    PAYMENT_TYPES = (
        ("donate", "Donation"),
        ("buy", "Buy Tree"),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    tree = models.ForeignKey(Tree, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=20)
    name = models.CharField(max_length=150)
    transaction_id = models.CharField(max_length=120, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.payment_type} - {self.amount}"
