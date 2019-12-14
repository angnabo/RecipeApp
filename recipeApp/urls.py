from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('recipes/', include('recipeApp.recipes.urls')),
    path('admin/', admin.site.urls)
]
