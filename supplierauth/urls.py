from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='supplier_dashboard'),
    path('available_supplies/', views.available_supplies, name='available_supplies'),
    path('delete_supply/<str:name>', views.delete_supply, name='delete_supply'),
    path('confirm_order/<str:name>/', views.confirm_order, name='confirm_order'),
    path('confirmed_orders/', views.confirmed_orders_list, name='confirmed_orders_list'),
    path('change_status/<str:name>/' , views.change_status, name='change_status'),
    path('contact/<str:name>/', views.contact, name='contact'),
    path('message/<str:name>/', views.message, name='message')


]