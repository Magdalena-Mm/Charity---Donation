from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from charity.forms import *
from charity.models import *
from charity.tokens import account_activation_token


class LandingPageView(View):
    def get(self, request):
        quantity = Donation.objects.aggregate(Sum('quantity'))['quantity__sum']
        institution = Donation.objects.aggregate(Count('institution'))['institution__count']
        category = Category.objects.filter(category__categories__name='FUN')
        fundacja = Institution.objects.filter(type='FUN')
        organizacja = Institution.objects.filter(type='ORG')
        zbiorka = Institution.objects.filter(type='ZBL')
        return render(request, 'charity/index.html',
                      {'quantity': quantity, 'institution': institution, 'fundacja': fundacja,
                       'organizacja': organizacja, 'zbiorka': zbiorka, 'category': category})


class AddDonationView(View):
    def get(self, request):
        return render(request, 'charity/form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'charity/login.html')


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'charity/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm()
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            user.set_password(user.password)
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            form = RegistrationForm
            return render(request, 'charity/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
