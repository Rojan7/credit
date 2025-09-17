from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.add_customer, name="add_customer"),
    path("customer/<int:pk>/", views.customer_detail, name="customer_detail"),
    path("entry/<int:entry_id>/delete/", views.delete_entry, name="delete_entry"),
    path("entry/<int:entry_id>/edit/", views.edit_entry, name="edit_entry"),
    path('customer/<int:pk>/delete/', views.delete_customer, name='delete_customer'),
]
