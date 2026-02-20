from django.urls import path
from . import views

urlpatterns = [
    # category
    path('categories/', views.CategoryCreateRetrieveView.as_view()),
    path('category/<str:id>/', views.CategoryRetrieveDeleteView.as_view()),
    # products
]