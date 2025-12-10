from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('trees', views.tree_list, name='tree_list'),
    path('add/', views.add_tree, name='add_tree'),
    path('my-trees', views.my_trees, name='my_trees'),

    # tree detail
    path('tree/<int:id>/', views.tree_detail, name='tree_detail'),

#     edit tree
path('tree/<int:id>/edit/', views.edit_tree, name='edit_tree'),
#     deleting a tree
path('tree/<int:id>/delete/', views.delete_tree, name='delete_tree'),

#     leaderboard
    path('leaderboard/', views.leaderboard, name='leaderboard'),

# admin price
path('tree/<int:id>/admin-edit/', views.admin_edit_tree, name='admin_edit_tree'),

#     admin delete
    path('tree/<int:id>/admin-delete/', views.admin_delete_tree, name='admin_delete_tree'),

# admin dashboard
path('dashboard/', views.admina_dashboard, name='admina_dashboard'),
path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

]



