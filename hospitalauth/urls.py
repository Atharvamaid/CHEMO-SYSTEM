from django.contrib import admin
from django.contrib.auth.views import PasswordChangeView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from django.urls import path
from . import views
urlpatterns = [
    path('', views.Home, name='Home'),
    path('signup/', views.CreateAccount, name='signup'),
    path('supplier_signup/', views.create_supplier_account, name='supplier_signup'),
    path('supplier_login/', views.supplier_login, name='supplier_login'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('covid_data/', views.TrackCases, name='trackcases'),
    path('update_data/', views.update_data, name='update'),
    path('search_hospitals/', views.Search, name='search'),
    path('search_hospital/<str:name>/', views.chat, name='chat'),
    path('request_supplies/', views.request_supplies, name='request_supplies'),
    path('place_order/<int:id>/', views.place_order, name="place_order"),
    path('my_orders/', views.my_orders, name='myorders'),
    path('password-reset/',PasswordResetView.as_view(template_name='hospitalauth/forget_password.html'),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name='hospitalauth/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='hospitalauth/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(
             template_name='hospitalauth/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('send_message/<str:name>', views.send_message, name='send_message')

]