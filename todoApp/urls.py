from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('todopage/', views.todo),
    path('sign-in/', views.signin_view, name='sign-in'),
    path('sign-up/', views.signup_view, name='sign-up'),
    path('sign-out/', views.signout_view, name='sign-out'),
    path('delete_todo/<int:srno>', views.delete_todo),
    path('edit_todo/<int:srno>', views.edit_todo, name='edit_todo'),
]