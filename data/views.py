from django.shortcuts import render
from django.shortcuts import HttpResponse

from .models import Host, Interface, Auth, Template, Instance

def index(request):
    host_objs = Host.objects.all()
    data = {'devs': host_objs}
    return render(request, 'data/index.html', context = data)