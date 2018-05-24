from django.shortcuts import render
from django.views import generic

# Create your views here.

def shop(request):

    return render(request,'shop.html',context={})
