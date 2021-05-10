from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from auth import forms
from django.contrib.auth import login

# Create your views here.


class Login(LoginView):
    template_name = 'auth/login.html'


class Logout(LogoutView):
    def get(self, request):
        return redirect('/')

class Signup(View):
    def get(self, request):                    # Function for handling GET request
        context = {
            'form': forms.SignupForm()
        }
        return render(request, 'auth/signup.html', context)

    def post(self, request):                    # Function for handling POST request
        form = forms.SignupForm(request.POST)
        if form.is_valid():                     # is_valid() will check if form data is valid or not
            user = form.save()                  # save() will successfully save the form data
            login(request, user)                # login() will log the user in
            return redirect('/')                # redirect to home page

        context = {
            'form': form
        }    
        return render(request, 'auth/signup.html', context)  # if form data is not valid redirect to signup page with previous prefilled form
