from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('admin/users/add/', views.admin_add_user, name='admin_add_user'),
    path('admin/delete-user/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),
    path('logout/', views.logout_user, name='logout'),
    path('index/', views.index, name='index'),
    path('payment/', views.mpesaPayement , name='payment'),
path('payments/', views.payments_list, name='payments_list'),

]

