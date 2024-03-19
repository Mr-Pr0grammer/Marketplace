from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.ProductsList.as_view()),
    path('products/<slug:slug>/', views.GetProduct.as_view()),
    path('categories/', views.CategoriesList.as_view()),
]