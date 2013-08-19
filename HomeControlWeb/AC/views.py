# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'AC/index.html', {})

def command(request):
    return HttpResponse('Command stub')

def webcam(request):
    return HttpResponse('WebCam stub')
