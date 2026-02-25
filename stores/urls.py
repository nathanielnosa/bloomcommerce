from django.urls import path
from . import views

urlpatterns = [
    # category
    path('categories/', views.CategoryCreateRetrieveView.as_view()),
    path('category/<str:id>/', views.CategoryRetrieveDeleteView.as_view()),
    # products
    path('products/', views.ProductCreateRetrieveView.as_view()),
    path('product/<str:id>/', views.ProductRetrieveDeleteView.as_view()),
    # add to cart
    path('addtocart/<str:id>/', views.AddProductToCart.as_view()),
    # users cart
    path('mycart/', views.MyCartView.as_view()),
    # manage cart
    path('managecart/<str:id>/', views.ManageCartView.as_view()),
]