from django.urls import path
from rest_framework import routers

from product.api_view import WarehouseProductViewSet
from product.views import HomeView, ProductCategoryCreateView, ProductCreateView, ProductDeleteView, \
    ProductCategoryDeleteView, ProductUpdateView, ProductCategoryUpdateView, UserLoginView, UserLogoutView, \
    ProductReport, ProductDetailReport

router = routers.SimpleRouter()
router.register(r'products', WarehouseProductViewSet)
urlpatterns = router.urls

urlpatterns += [
    path('', HomeView.as_view(), name="home_view"),
    path('user/login_view/', UserLoginView.as_view(), name="user_login_view"),
    path('user/logout_view/', UserLogoutView.as_view(), name="user_logout_view"),
    path('product/category_create/', ProductCategoryCreateView.as_view(), name="product_category_create"),
    path('product/category_update/<int:pk>/', ProductCategoryUpdateView.as_view(), name="product_category_update"),
    path('product/category_delete/<int:pk>/', ProductCategoryDeleteView.as_view(), name="product_category_delete"),
    path('product/create/', ProductCreateView.as_view(), name="product_create"),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name="product_update"),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name="product_delete"),
    path('product/report/', ProductReport.as_view(), name="product_report"),
    path('product/detail_report/<int:pk>/', ProductDetailReport.as_view(), name="product_detail_report"),
]
