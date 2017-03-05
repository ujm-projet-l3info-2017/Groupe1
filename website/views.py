from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def javascript(request, javascript_file):
    return HttpResponse(loader.get_template('website/js/'+javascript_file).render(None, request))

def style(request, style_file):
    return HttpResponse(loader.get_template('website/css/'+style_file).render(None, request))

def index(request):
    template = loader.get_template('website/index.html')
    context={}
    return HttpResponse(template.render(context, request))

