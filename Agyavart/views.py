from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
	return render(request,'Login.html')

def register(request):
	return render(request,'signup.html')