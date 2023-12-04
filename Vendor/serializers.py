from rest_framework import serializers
from .models import Vendor, PurchaseOrder


class VendorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class PurchseOrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class PerformanceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = (
            'id', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate'
        )
