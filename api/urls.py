from django.urls import path, include
from . import product_view,user_cart_view,users_view,order_placed_view

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="E-commerce Backend System Development ",
        default_version='v1',
        description="This is a backend system for an e-commerce platform using Python and Django. The system supports product management, user orders, and an analytics dashboard. ",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('products/', product_view.get_all_products, name='get_all_products'),
    path('products/<int:pk>/', product_view.get_product, name='get_product'),
    path('products/add/', product_view.add_product, name='add_product'),
    path('products/update/<int:pk>/', product_view.update_product, name='update_product'),
    path('products/delete/<int:pk>/', product_view.delete_product, name='delete_product'),
    path('products/catogery/', product_view.add_category, name='add_category'),


    path('cart/add-product/', user_cart_view.add_product_to_cart, name='add_to_cart'),
    path('cart/update/<int:pk>/', user_cart_view.update_cart_product, name='update_cart_product'),
    path('cart/all-products/', user_cart_view.get_all_products_from_cart, name='get_all_cart_products'),
    path('cart/delete/<int:pk>/', user_cart_view.delete_cart_product, name='delete_cart_product'),

    path('order/', order_placed_view.place_order, name='order'),

    path('user/all-users/', users_view.user_list, name='user_list'),
    path('user', users_view.UserView.as_view()),
    path('accounts/', include('allauth.urls')),
    path('user/login', users_view.LoginView.as_view()),
    path('user/register', users_view.RegisterView.as_view()),
    path('user/logout', users_view.LogoutView.as_view()),

    path('addresses/', users_view.address_list, name='address_list'),
    path('addresses/<int:pk>/', users_view.address_detail, name='address_detail'),
]