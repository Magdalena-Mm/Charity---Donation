from django.shortcuts import render
from PortfolioLab.settings import EMAIL_HOST_USER
from . import forms
from django.core.mail import send_mail


#DataFlair #Send Email
def subscribe(request):
    sub = forms.Subscribe()
    if request.method == 'POST':
        sub = forms.Subscribe(request.POST)
        subject = 'Welcome to Charity Donation'
        message = 'If you want to join a charity donation, click on the link:'
        recepient = str(sub['Email'].value())
        send_mail(subject,
            message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        return render(request, 'subscribe/success.html', {'recepient': recepient})
    return render(request, 'subscribe/index.html', {'form':sub})