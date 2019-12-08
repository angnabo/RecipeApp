from django.urls import path

from . import views

app_name = 'recipes'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:recipe_id>/', views.details, name='details'),
    path('<int:recipe_id>/like/', views.like, name='like')
]