from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Vendor import views

router=DefaultRouter()
router.register('vendors', views.VendorViewSet, basename='vendors')
router.register('purchase_orders', views.PurchaseOrderViewSet, basename='purchase_orders')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/vendors/<int:pk>/performance/', views.VendorPerformance.as_view({'get': 'retrieve'}), name='vendor-performance'),
]