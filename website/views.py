from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db import connection
# Create your views here.

def index(request):
    load_tables()
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
    
def load_tables():
    # On charge les donnees de l'exercice > a passer en argument POST (formulaire)

    #CECI
    #NE
    #FONCTIONNE
    #PAS
    #(mais c'est joli)
    
    with connection.cursor() as cursor:
        print("YOYOYYOO1")
        try:
            cursor.execute('select * from website_table')
            row=cursor.fetchall()    
            print("YOYOYYOO3 ")
            
            tableau=[]
            for line in row:
                i=0
                for l in line:
                    tableau.append(l)
                    print (i, l)
                    i+=1
            print (tableau)
            print ("\n"*5)
            print
            cursor.execute('create table '+line[0]+' '+line[1])
            print("YOYOYYOO5")
                #row[2].split(' ')
                #for insertline in row[2]:
                #    cursor.execute('insert into '+line[0]+insertline)
        except:
            print("lolillo")

