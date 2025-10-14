from django.urls import path
from blog.apps import BlogConfig
from .views import (
    BlogEntryCreateView,
    BlogEntryListView,
    BlogEntryDetailView,
    BlogEntryUpdateView,
    BlogEntryDeleteView
)


app_name = BlogConfig.name

urlpatterns = [
    # CRUD
    path('create/', BlogEntryCreateView.as_view(), name='create'),
    path('', BlogEntryListView.as_view(), name='list'),
    path('view/<slug:slug>/', BlogEntryDetailView.as_view(), name='view'),
    path('edit/<slug:slug>/', BlogEntryUpdateView.as_view(), name='edit'),
    path('delete/<slug:slug>/', BlogEntryDeleteView.as_view(), name='delete'),
]
