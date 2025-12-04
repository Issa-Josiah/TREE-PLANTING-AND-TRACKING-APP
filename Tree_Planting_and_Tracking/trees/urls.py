from django.urls import path
from . import views

urlpatterns = [
    path('', views.tree_list, name='tree_list'),
    path('add/', views.add_tree, name='add_tree'),
    path('my-tree_app/', views.my_trees, name='my_trees'),
]