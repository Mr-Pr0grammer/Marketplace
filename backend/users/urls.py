from django.urls import path
from . import views


urlpatterns = [
    path('complaint/', views.UserComplaintAPIView.as_view()),
    # path('logout/', views.LogoutView.as_view(), name='auth_logout')
]

