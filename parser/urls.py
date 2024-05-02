from django.urls import path, include

from .views import ProductView

urlpatterns = [
    path('products/', ProductView.as_view(), name='products-view'), 
    path('products/<int:product_id>', ProductView.as_view(), name='product-view')
]