from django.urls import path
from catalog.apps import CatalogConfig
from .views import ProductListView, ContactsTemplateView, ProductDetailView, ProductCreateView


app_name = CatalogConfig.name


urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='create_product'),
]
