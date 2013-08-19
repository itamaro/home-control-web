# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse('Home stub')

def command(request):
    return HttpResponse('Command stub')

def webcam(request):
    return HttpResponse('WebCam stub')
