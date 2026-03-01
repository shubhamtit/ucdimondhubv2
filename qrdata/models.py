# models.py
from django.db import models
from cloudinary.models import CloudinaryField

class PaymentQR(models.Model):
    name = models.CharField(max_length=100)
    package_name = models.CharField(
        max_length=200, 
        help_text="Package name like '60 UC BGMI', '300 UC BGMI', etc.",
        default="Default Package"  # Added default
    )
    package_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Package amount",
        default=0.00  # Added default
    )
    qr_image = CloudinaryField("image")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['package_amount']
        verbose_name = "Payment QR Code"
        verbose_name_plural = "Payment QR Codes"

    def __str__(self):
        return f"{self.package_name} - ₹{self.package_amount}"