from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('user/sign-in/', views.signin_view, name='sign-in'),
    path('user/sign-up/', views.signup_view, name='sign-up'),
    path('user/sign-out/', views.signout_view, name='sign-out')
]