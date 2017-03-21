from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db import connection
# Create your views here.

def index(request):
    load_tables()
    template = loader.get_template('website/index.html')
    #load_tables()
    return HttpResponse(template.render(None, request))

def request(request):
    # Ajouter un argument "contenu requete"
    # Recupere a l'envoi de la requete par l'utilisateur
    requete = request.POST.get('query');
    print(requete)
    
    
    template = loader.get_template('website/request.html')
    with connection.cursor() as cursor:
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
    
    with connection.cursor() as cursor:
        try:
            cursor.execute('select * from website_table')
            row=cursor.fetchall()
            for line in row:
                tableau=[]
                for l in line:
                    tableau.append(l)
                    print(tableau)
                    tableau[0]=str(tableau[0])
                    tableau[1]=str(tableau[1]) # NOM de la table
                    tableau[2]=str(tableau[2]) # attributs de creation
                    tableau[3]=str(tableau[3]) # Insert into
                    cursor.execute('create table '+tableau[1]+' '+tableau[2])
                    
                tableau[3]=tableau[3].split('\n')
                for insertline in tableau[3]:
                    cursor.execute('insert into '+tableau[1]+insertline)
        except:
            print("lolillo la table existe deja ou on est des merdes !")

def load_question(request):
    exercice_no  = request.POST.get('exercice_no')
    question_no  = request.POST.get('question_no')
    requete = "SELECT intitule FROM website_question WHERE website_question.id = website_contient_exercice_question.idQuestion AND website_exercice.id = website_contient_exercice_question.idExercice AND exercice.id ="+exercice_no+" AND question.id ="+question_no
    with connection.cursor() as cursor:
        try:
            cursor.execute(requete)
            row = cursor.fetchone()[0]
        except:
            template = loader.get_template('website/error_request.html')
            context = None
            return HttpResponse(template.render(context, request))

        return  HttpResponse("<p>"+ row +"</p>")

def load_select(request):
    template = loader.get_template('website/request.html')
#    with connection.cursor() as cursor:
        
        #cursor.execute('SELECT * FROM website_contient')
    
