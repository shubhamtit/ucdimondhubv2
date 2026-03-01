# admin.py
from django.contrib import admin
from qrdata.models import PaymentQR


@admin.register(PaymentQR)
class PaymentQRAdmin(admin.ModelAdmin):
    list_display = ['package_name', 'package_amount', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['package_name', 'package_amount']
    list_editable = ['is_active']
    ordering = ['package_amount']
    
    fieldsets = (
        ('Package Information', {
            'fields': ('name', 'package_name', 'package_amount')
        }),
        ('QR Code', {
            'fields': ('qr_image',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )