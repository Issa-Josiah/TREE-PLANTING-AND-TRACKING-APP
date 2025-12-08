from django.db import models

class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='sponsors/')
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
