from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/shop/', include('shop.urls')),
    path('api/users/', include('users.urls')),
    path('api/drf-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

