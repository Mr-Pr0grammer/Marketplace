from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/shop/', include('shop.urls')),
    path('api/drf-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# http://127.0.0.1:8000/auth/users/ - для регистрации, метод POST. Нужно ввести form-data (username и password)

# http://127.0.0.1:8000/auth/jwt/create/ - для создания токена, метод POST. Вернет access и refresh. Нужны username и password существующего юзера

# http://127.0.0.1:8000/auth/jwt/refresh/ - для получения access, метод POST. Потребует refresh


# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

