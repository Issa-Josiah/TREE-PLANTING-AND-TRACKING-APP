from django.urls import path
from . import views

urlpatterns = [

    path('', views.event_list, name='event_list'),
    path('add/', views.add_event, name='add_event'),
    path('<int:id>/edit/', views.edit_event, name='edit_event'),
    path('<int:id>/delete/', views.delete_event, name='delete_event'),
    path('pay/<int:id>/', views.event_payment, name='event_payment'),

]
