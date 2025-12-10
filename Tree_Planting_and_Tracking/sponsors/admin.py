from django.contrib import admin
from .models import Sponsor
from .models import Payment

# Register your models here.
admin.site.register(Sponsor)
admin.site.register(Payment)
