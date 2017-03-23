from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db import connection
# Create your views here.

def index(request):
    #load_tables()
    template = loader.get_template('website/index.html')
    exercice = load_exercise(request).content
    question = load_question(request).content
    label = load_label(request).content

    context = {
        'exercice': exercice,
        'question': question,
        'label': label
    }
    return HttpResponse(template.render(context, request))

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

def expected_request(request):
    exercice_no  = request.POST.get('exercise_no')
    if(exercice_no == None):
        exercice_no = "1"
    question_no  = request.POST.get('question_no')
    if(question_no == None):
        question_no = "1"
    with connection.cursor() as cursor:
        try:
            cursor.execute("select requete from website_question,website_contient_exercice_question,website_exercice where website_question.numero="+question_no+" AND website_question.id=idQuestion AND idExercice=website_exercice.id AND website_exercice.numero="+exercice_no)
            column_name = [col[0] for col in cursor.description]
            row = cursor.fetchall()
            return (column_name,row)
        except:
            template = loader.get_template('website/error_request.html')
            context=None

def display_expected_request(request):
    column_name,row=expected_request(request)
    #blblbl
            
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

def load_label(request):
    exercice_no  = request.POST.get('exercise_no')
    if(exercice_no == None):
        exercice_no = "1"
    question_no  = request.POST.get('question_no')
    if(question_no == None):
        question_no = "1"
    requete = "SELECT intitule FROM website_question,website_contient_exercice_question,website_exercice WHERE website_question.id = website_contient_exercice_question.idQuestion AND website_exercice.id = website_contient_exercice_question.idExercice AND website_exercice.id ="+exercice_no+" AND website_question.id ="+question_no
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

def load_question(request):
    template = loader.get_template('website/question.html')
    exercice_no  = request.POST.get('exercise_no')
    if(exercice_no == None):
        exercice_no = "1"
    requete = "SELECT website_question.numero FROM website_contient_exercice_question,website_question,website_exercice WHERE website_exercice.id=website_contient_exercice_question.idExercice AND website_question.id=website_contient_exercice_question.idQuestion AND website_exercice.numero="+exercice_no
    with connection.cursor() as cursor:
        try:
            cursor.execute(requete)
            row =cursor.fetchall()
            context= {
                'row': row
            }
        except:
            template = loader.get_template('website/error_request.html')
            context = None
            return HttpResponse(template.render(context, request))

        return HttpResponse(template.render(context, request))

def load_exercise(request):
    template = loader.get_template('website/exercise.html')
    
    requete = "SELECT numero FROM website_exercice"
    with connection.cursor() as cursor:
        try:
            cursor.execute(requete)
            row =cursor.fetchall()
            context= {
                'row': row
            }
        except:
            template = loader.get_template('website/error_request.html')
            context = None
            return HttpResponse(template.render(context, request))

        return HttpResponse(template.render(context, request))
