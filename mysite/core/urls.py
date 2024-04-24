from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [

    path('', views.vendor_index, name='vendor_index'),
    path('<slug:slug>/', views.vendor_detail, name='vendor_detail'),
    path('vendor-category/<int:vendor_category_id>/', views.vendor_category, name='vendor_category'),
    path('category-index/', views.category_index, name='category_index'),
    path('category-detail/', views.category_detail, name='category_detail'),
    path('create-category/', views.create_category, name='create_category'),
    # Add more URL patterns as needed
]
