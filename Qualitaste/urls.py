from django.urls import path, include
from . import views

urlpatterns = [

    # authentication:: should be accounts/
    path('accounts/login/', views.cutom_login, name='login'),
    path('accounts/logout/', views.custom_logout, name='logout'),
    path('accounts/signup/', views.custom_signup, name='signup'),
    path('accounts/password_reset/', views.custom_password_reset, name='password_reset'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts', include('django.contrib.auth.urls')),


    # regular urls
    path('', views.home, name='home'),
    path('order/', views.order, name='order'),
    path('gallery/', views.gallery, name='gallery'),
    path('help/', views.help, name='help'),

    #payments
    path('order/payments', views.payments, name='payments'),

    # cancel_order
    path('order/cancel/<int:pk>', views.cancel_order, name='cancel_order'),
]