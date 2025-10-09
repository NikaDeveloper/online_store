from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home
from . import views


app_name = CatalogConfig.name


urlpatterns = [
    path('', home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/create/', views.create_product, name='create_product'),
]
