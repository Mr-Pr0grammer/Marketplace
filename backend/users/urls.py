from django.urls import path
from . import views


urlpatterns = [
    path('complaint/', views.UserComplaintAPIView.as_view()),
    path('profile/', views.UserProfileView.as_view()),
    path('profile/update/', views.UserProfileView.as_view()),
]

