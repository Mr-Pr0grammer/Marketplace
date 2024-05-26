from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.ProductsList.as_view()),
    path('products/category/<slug:slug>/', views.ProductsListByCategory.as_view()),
    path('products/price/<str:str>/', views.ProductsListByPrice.as_view()),
    path('products/<slug:slug>/', views.GetProduct.as_view()),

    path('categories/', views.CategoriesList.as_view()),

    path('product_cart/add/', views.ProductCartItemAPIView.as_view()),
    path('product_cart/list/', views.ProductCartItemAPIView.as_view()),
    path('product_cart/delete/', views.ProductCartItemAPIView.as_view()),
    path('product_cart/delete_all/', views.DeleteCartItemsAll.as_view()),
    path('own_product/add/', views.AddProductView.as_view())
]
