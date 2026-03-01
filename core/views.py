import json
import logging
from django.http import JsonResponse
from django.shortcuts import render, redirect
from qrdata.models import PaymentQR
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


def home(request):
    return render(request, "home.html")


@csrf_exempt
def checkout(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            request.session["payment_data"] = data
            logger.info(f"Checkout data saved: {data}")
            return JsonResponse({"status": "ok"})
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return JsonResponse({"status": "error", "message": "Invalid data"}, status=400)
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


def payment(request):
    data = request.session.get("payment_data")
    
    # Redirect to home if no payment data
    if not data:
        logger.warning("Payment page accessed without session data")
        return redirect('home')
    
    # Default values
    qr = None
    qr_url = None
    
    package_name = data.get("package", "")
    amount = data.get("amount", "")
    
    logger.info(f"Looking for QR - Package: {package_name}, Amount: {amount}")
    
    # Strategy 1: Try to find QR by exact package name match
    if package_name:
        qr = PaymentQR.objects.filter(
            package_name__iexact=package_name,
            is_active=True
        ).first()
        
        if qr:
            logger.info(f"QR found by package name: {qr.name}")
    
    # Strategy 2: If not found by package name, try to match by amount
    if not qr and amount:
        try:
            amount_decimal = float(amount)
            qr = PaymentQR.objects.filter(
                package_amount=amount_decimal,
                is_active=True
            ).first()
            
            if qr:
                logger.info(f"QR found by amount: {qr.name}")
        except (ValueError, TypeError) as e:
            logger.error(f"Error converting amount to decimal: {e}")
    
    # Strategy 3: Fallback to first active QR if no match found
    if not qr:
        qr = PaymentQR.objects.filter(is_active=True).first()
        if qr:
            logger.warning(f"Using fallback QR: {qr.name}")
        else:
            logger.error("No active QR codes found in database")
    
    # Get QR URL
    if qr:
        qr_url = qr.qr_image.url
    
    return render(request, "payment.html", {
        "data": data,
        "qr_url": qr_url,
        "qr_name": qr.name if qr else None
    })