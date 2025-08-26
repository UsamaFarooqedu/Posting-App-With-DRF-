from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib import messages

@login_required
def setup_2fa(request):
    if request.method == 'POST':
        device = TOTPDevice.objects.get_or_create(user=request.user, confirmed=False)[0]
        if not device.confirmed:
            # Generate a new secret key if not confirmed
            device = TOTPDevice.objects.create(user=request.user, confirmed=False)
        
        # Verify the token
        token = request.POST.get('token')
        if token and device.verify_token(token):
            device.confirmed = True
            device.save()
            messages.success(request, 'Two-factor authentication has been enabled.')
            return redirect('home')
        elif token:
            messages.error(request, 'Invalid token. Please try again.')
    
    else:
        device = TOTPDevice.objects.get_or_create(user=request.user, confirmed=False)[0]
    
    # Get the provisioning URI for the QR code
    provisioning_uri = device.config_url
    
    return render(request, 'accounts/setup_2fa.html', {
        'provisioning_uri': provisioning_uri,
    })