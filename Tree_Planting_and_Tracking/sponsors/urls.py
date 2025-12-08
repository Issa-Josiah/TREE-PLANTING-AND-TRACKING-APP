
from django.urls import path
from . import views

urlpatterns = [
    path('sponsors/add/', views.add_sponsor, name='add_sponsor'),
]

