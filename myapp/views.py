from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse("<h1>Welcome to Django!</h1><p>Your basic Django application is running successfully.</p>")
