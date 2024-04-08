from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from orders.views import place_order
from products.views import add_product, add_category, get_all_products,get_product,update_product,delete_product,update_category,get_all_categories,delete_category
from users_cart.views import add_product_to_cart,get_all_products_from_cart,update_cart_product,delete_cart_product
from users.views import user_list, UserView, LoginView,LogoutView,RegisterView,address_list,address_detail


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

    path('products/', get_all_products, name='get_all_products'),
    path('products/<int:pk>/', get_product, name='get_product'),
    path('product/', add_product, name='add_product'),
    path('product/update<int:pk>/', update_product, name='update_product'),
    path('product/<int:pk>/', delete_product, name='delete_product'),
    
    path('catogery/', add_category, name='add_category'),
    path('catogery/update<int:id>/', update_category, name='update_category'),
    path('catogeries/', get_all_categories, name='get_all_categories'),
    path('catogery/<int:id>/', delete_category, name='delete_category'),

    path('cart', add_product_to_cart, name='add_to_cart'),
    path('cart/update<int:pk>/', update_cart_product, name='update_cart_product'),
    path('cart/products/', get_all_products_from_cart, name='get_all_cart_products'),
    path('cart/<int:pk>/', delete_cart_product, name='delete_cart_product'),

    path('order/', place_order, name='order'),

    path('users/', user_list, name='user_list'),
    path('user', UserView.as_view()),
    path('accounts/', include('allauth.urls')),
    path('user/login', LoginView.as_view()),
    path('user/register', RegisterView.as_view()),
    path('user/logout', LogoutView.as_view()),

    path('addresses/', address_list, name='address_list'),
    path('addresses/<int:pk>/', address_detail, name='address_detail'),
]