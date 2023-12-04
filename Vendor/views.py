from rest_framework.response import Response
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializers, PurchseOrderSerializers, PerformanceSerializers
from rest_framework import viewsets


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializers


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchseOrderSerializers


class VendorPerformance(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        if pk is not None:
            try:
                vendor_obj = Vendor.objects.get(id=pk)
                serializer = PerformanceSerializers(vendor_obj)
                return Response(serializer.data)
            except Vendor.DoesNotExist:
                return Response({'error': 'Vendor not found'}, status=404)
