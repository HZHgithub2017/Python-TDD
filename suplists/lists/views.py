from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render
def home_page(request):
    return render(request,'home.html')