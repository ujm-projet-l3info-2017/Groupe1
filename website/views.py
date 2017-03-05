from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db import connection
# Create your views here.

def index(request):
    template = loader.get_template('website/index.html')
    return HttpResponse(template.render(None, request))

def request(request):
    # Ajouter un argument "contenu requete"
    # Recupere a l'nevoie de la requete par l'utilisateur
    requete = request.POST.get('query');
    print(requete)
        
    
    template = loader.get_template('website/request.html')
    with connection.cursor() as cursor:
        
        #cursor.execute('SELECT * FROM website_contient')
        try:
            cursor.execute(requete)
            column_name = [col[0] for col in cursor.description]
            row = cursor.fetchall()
            context= {
                'row': row,
                'column_name': column_name
            }
        except:
            template = loader.get_template('website/error_request.html')
            context = None

        
        return HttpResponse(template.render(context, request))
    
