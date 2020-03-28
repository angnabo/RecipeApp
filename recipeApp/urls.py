from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from recipeApp import settings

urlpatterns = [
    path('recipes/', include('recipeApp.recipes.urls')),
    path('users/', include('recipeApp.users.urls')),
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)