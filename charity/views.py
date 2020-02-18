from django.shortcuts import render, get_object_or_404
from django.views import View
from charity.models import *


class LandingPageView(View):
    def get(self, request): #, id):
#        institution = get_object_or_404(Institution, pk=id)
        return render(request, 'charity/index.html') #, {'institution': institution})


class AddDonationView(View):
    def get(self, request):
        return render(request, 'charity/form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'charity/login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'charity/register.html')

    def post(self, request):
        name = request.POST['name']


