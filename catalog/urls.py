from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from .views import (ProductListView, ContactsTemplateView, ProductDetailView,
                    ProductCreateView, ProductUpdateView, ProductDeleteView, ProductsByCategoryListView)


app_name = CatalogConfig.name


urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete_product'),
    path('category/<int:pk>/', ProductsByCategoryListView.as_view(), name='products_by_category'),
]
