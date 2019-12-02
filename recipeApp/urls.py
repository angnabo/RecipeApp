from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('recipes/', include('recipes.urls')),
    path('admin/', admin.site.urls)
]
