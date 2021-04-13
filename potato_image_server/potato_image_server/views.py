from django.shortcuts import render

from .utils import Proxy


def index(request):
    #dates = Proxy.get_dates()
    dates = []
    return render(request, 'index.html', {'dates': dates})
