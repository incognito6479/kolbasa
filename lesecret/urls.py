"""lesecret URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from lesecret.router import DefaultRouter
from order.api_view import ChangeInvoiceStatus
from product.urls import router as product_router
from counter_party.urls import router as counter_party_router
from order.urls import router as order_router
from payment.urls import router as payment_router

router = DefaultRouter()
router.extend(product_router)
router.extend(counter_party_router)
router.extend(order_router)
router.extend(payment_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.urls')),
    path('', include('payment.urls')),
    path('', include('income.urls')),
    path('', include('warehouse.urls')),
    path('', include('order.urls')),
    path('', include('movement.urls')),
    path('', include('counter_party.urls')),
    path('', include('user.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/invoice_status_change/', ChangeInvoiceStatus.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
