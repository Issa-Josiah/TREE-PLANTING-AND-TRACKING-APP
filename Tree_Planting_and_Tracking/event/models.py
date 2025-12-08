from django.db import models
from django.contrib.auth.models import User

LOCATION_CHOICES = [
    ('NAIROBI', 'Nairobi'),
    ('MOMBASA', 'Mombasa'),
    ('KISUMU', 'Kisumu'),
    ('OTHER', 'Other'),
]
# create your models here
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=100, default='NAIROBI')
    image = models.ImageField(upload_to='events/', default='events/event.png')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
