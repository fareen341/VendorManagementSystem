from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder
from django.utils import timezone
from django.db.models import Avg, F, ExpressionWrapper, fields
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import timedelta


# logic for each aspect is different cuz it might evolve independently over time
# On-Time Delivery Rate
@receiver(post_save, sender=PurchaseOrder)
def on_time_delevery_rate(sender, instance, **kwargs):
    if instance.status == 'completed':
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now()).count()
        total_completed_pos = completed_pos.count()

        if total_completed_pos > 0:
            vendor.on_time_delivery_rate = (on_time_deliveries / total_completed_pos) * 100
            vendor.save()


# Quality Rating Average
@receiver(post_save, sender=PurchaseOrder)
def quality_rating_avg(sender, instance, **kwargs):
    if instance.status == 'completed' and instance.quality_rating is not None:
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')

        quality_rating_avg = completed_pos.aggregate(Avg('quality_rating'))['quality_rating__avg']
        if quality_rating_avg is not None:
            vendor.quality_rating_avg = quality_rating_avg
            vendor.save()


# Average Response Time
@receiver(post_save, sender=PurchaseOrder)
def average_response_time(sender, instance, **kwargs):
    if instance.acknowledgment_date is not None:
        vendor = instance.vendor
        response_times = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)\
            .annotate(response_time=ExpressionWrapper(
                F('acknowledgment_date') - F('issue_date'),
                output_field=fields.DurationField()
            ))\
            .aggregate(Avg('response_time'))

        vendor.average_response_time = timedelta(0)
        average_response_time = response_times['response_time__avg']
        if average_response_time is not None:
            # saving the data in duration field
            vendor.average_response_time = average_response_time
            # to store it in minute, and changing the models to floatfield:
            # vendor.average_response_time = average_response_time.total_seconds() / 60
        vendor.save()


# Fulfilment Rate
@receiver(post_save, sender=PurchaseOrder)
def fulfilment_rate(sender, instance, **kwargs):
    vendor = instance.vendor
    fulfilled_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', issue_date__isnull=False)
    total_pos = PurchaseOrder.objects.filter(vendor=vendor).count()

    vendor.fulfillment_rate = 0
    if total_pos > 0:
        vendor.fulfillment_rate = (fulfilled_pos.count() / total_pos) * 100
    vendor.save()

# Authentication Code
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)