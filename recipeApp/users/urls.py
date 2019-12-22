from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signUp, name='signup'),
    path('login/', views.logIn, name='login'),
    path('logout/', views.logout_view, name='logout')
]
