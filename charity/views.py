from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.views import View

from charity.forms import *
from charity.models import *


class LandingPageView(View):
    def get(self, request):
        quantity = Donation.objects.aggregate(Sum('quantity'))['quantity__sum']
        institution = Donation.objects.aggregate(Sum('institution'))['institution__sum']
        fundacja = Institution.objects.filter(type='FUN')
        organizacja = Institution.objects.filter(type='ORG')
        zbiorka = Institution.objects.filter(type='ZBL')
        paginator1 = Paginator(fundacja, 5)
        paginator2 = Paginator(organizacja, 5)
        paginator3 = Paginator(zbiorka, 5)
        page_number = request.GET.get('page')
        fundacjapag = paginator1.get_page(page_number)
        return render(request, 'charity/index.html', {'quantity': quantity, 'institution': institution, 'fundacja': fundacja, 'organizacja': organizacja, 'zbiorka': zbiorka, 'fundacjapag': fundacjapag})


class AddDonationView(View):
    def get(self, request):
        return render(request, 'charity/form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'charity/login.html')


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'charity/register.html', {'form': form})

    def post(self, request):
        pass



