from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db import connection
from .similarity.similarity import compare_table
from .similarity.mapping import Mapping
from .parser.syntax import SQLSyntaxParser
# Create your views here.

def index(request):
    #load_tables()
    template = loader.get_template('website/index.html')
    exercice = load_exercise(request).content
    question = load_question(request).content
    label = load_label(request).content
    expected_request=load_expected_request(request).content
    tables = load_tables_exercise(request).content
    context = {
        'exercice': exercice,
        'question': question,
        'label': label,
        'expected_request': expected_request,
        'tables': tables
    }
    return HttpResponse(template.render(context, request))

def request(request):
    # Ajouter un argument "contenu requete"
    # Recupere a l'envoi de la requete par l'utilisateur
    requete = request.POST.get('query');
    column_expected, table_expected = expected_request(request)
    template = loader.get_template('website/request.html')
    with connection.cursor() as cursor:
        try:
            cursor.execute(requete)
            column_name = [col[0] for col in cursor.description]
            row = cursor.fetchall()
            row = [[str(row[i][j]) for j in range(len(row[i]))] for i in range(len(row))]
            color_table =compare_table(table_expected, row, column_expected, column_name)
            table = [[[color_table[i][j], row[i][j]] for j in range(len(row[i]))] for i in range(len(row))]
            context= {
                'column_name': column_name,
                'table': table
            }
        except Exception as e:
            error = str(e)
            context= {
                'error': error
            }
            template = loader.get_template('website/error_request.html')

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
            expected_request = str(cursor.fetchone()[0])

        except Exception as e:
            error = str(e)
            context= {
                'error': error
            }
            template = loader.get_template('website/error_request.html')
        try:
            print(expected_request)
            cursor.execute(expected_request)
            column_name = [col[0] for col in cursor.description]
            row = cursor.fetchall()
            row = [[str(row[i][j]) for j in range(len(row[i]))] for i in range(len(row))]
            return (column_name,row)
        except Exception as e:
            error = str(e)
            context= {
                'error': error
            }
            template = loader.get_template('website/error_request.html')

def load_hint(request):
    user_request = request.POST.get('query')
    # We take the expected request
    exercice_no  = request.POST.get('exercise_no')
    if(exercice_no == None):
        exercice_no = "1"
    question_no  = request.POST.get('question_no')
    if(question_no == None):
        question_no = "1"
    with connection.cursor() as cursor:
        try:
            cursor.execute("select requete from website_question,website_contient_exercice_question,website_exercice where website_question.numero="+question_no+" AND website_question.id=idQuestion AND idExercice=website_exercice.id AND website_exercice.numero="+exercice_no)
            # We have now the expected request
            expected_request = str(cursor.fetchone()[0])

        except Exception as e:
            error = str(e)
            context= {
                'error': error
            }
            template = loader.get_template('website/error_request.html')
    p = SQLSyntaxParser(expected_request)
    t1 = p.parse()
    p = SQLSyntaxParser(user_request)
    t2 = p.parse()
    mapping = Mapping(t1, t2)
    mapping.compare()
    context = {
        'hint': mapping.hint
    }
    template = loader.get_template('website/hint.html')
    return HttpResponse(template.render(context, request))
    
    
            
def load_expected_request(request):
    column_name,row=expected_request(request)
        
    template = loader.get_template('website/expected_request.html')
    context= {
        'row': row,
        'column_name': column_name
    }    
    return HttpResponse(template.render(context, request))

def load_tables(request):
    # On charge les donnees de l'exercice > a passer en argument POST (formulaire)
    
    exercice_no  = request.POST.get('exercise_no')
    if(exercice_no == None):
        exercice_no = "1"

    print("DAns load tables: "+exercice_no)

        
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT * FROM website_table,website_contient_exercice_table,website_exercice WHERE website_exercice.numero="+exercice_no+" AND website_exercice.id=idExercice AND idTable=website_table.id")
            row=cursor.fetchall()
            for line in row:
                tableau=[]
                for l in line:
                    tableau.append(l)
                tableau[0]=str(tableau[0])
                tableau[1]=str(tableau[1]) # NOM de la table
                tableau[2]=str(tableau[2]) # attributs de creation
                tableau[3]=str(tableau[3]) # Insert into
                cursor.execute('create table '+tableau[1]+' '+tableau[2])
                tableau[3]=tableau[3].split('\n')
                for insertline in tableau[3]:
                    cursor.execute('INSERT INTO '+tableau[1]+" "+insertline)
        except:
            print("Erreur: la table existe deja !")


def drop_tables(request):
    #supprime toutes les tables de l'exo, une amelio serait de chopper l'ancien num d'exo
    print("JE DROP")
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT nom FROM website_table")
            row=cursor.fetchall()
            for line in row:
                for l in line:
                    cursor.execute('drop table if exists '+str(l))
        except:
            print("Erreur: drop table a foire !")
    #je charge les bonnes tables maintenant
    load_tables(request)

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
        except Exception as e:
            error = str(e)
            context= {
                'error': error
            }
            template = loader.get_template('website/error_request.html')
            return HttpResponse(template.render(context, request))

        return  HttpResponse("<p>"+ row +"</p>")

def load_question(request):
    template = loader.get_template('website/question.html')
    exercice_no  = request.POST.get('exercise_no')
    if(exercice_no == None):
        exercice_no = "1"
    requete = "SELECT website_question.numero FROM website_contient_exercice_question,website_question,website_exercice WHERE website_exercice.id=website_contient_exercice_question.idExercice AND website_question.id=website_contient_exercice_question.idQuestion AND website_exercice.numero="+exercice_no


    # On enleve les autres tables
    drop_tables(request)
    # On charge les tables de l'exercice

    #######################################################################################################
    #
    # /!\ CHARGE 2 FOIS toutes les fonctions: au clic du menu deroulant, au clic du choix
    # > Devrait faire qu'au choix.
    #
    #######################################################################################################
    
    with connection.cursor() as cursor:
        try:
            cursor.execute(requete)
            row =cursor.fetchall()
            context= {
                'row': row
            }
        except Exception as e:
            error = str(e)
            context= {
                'error': error
            }
            template = loader.get_template('website/error_request.html')
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
        except Exception as e:
            error = str(e)
            context= {
                'error': error
            }
            template = loader.get_template('website/error_request.html')
            return HttpResponse(template.render(context, request))

    return HttpResponse(template.render(context, request))

def load_tables_exercise(request):
    template = loader.get_template('website/tables_exercise.html')
    exercice_no  = request.POST.get('exercise_no')
    if(exercice_no == None):
        exercice_no = "1"
    requete = "SELECT website_table.nom FROM website_table, website_exercice, website_contient_exercice_table WHERE website_contient_exercice_table.idExercice=website_exercice.numero AND website_contient_exercice_table.idtable=website_table.id AND numero="+exercice_no
   
    with connection.cursor() as cursor:
        try:
            cursor.execute(requete)
            row =cursor.fetchall()
            # always one name per tuple
            name =  [str(row[j][0]) for j in range(len(row))]
            tables=list()
            for nom in row:
                requete = "SELECT * FROM "+nom[0]
                cursor.execute(requete)
                column_name = [col[0] for col in cursor.description]
                row = cursor.fetchall()
                row = [[str(row[i][j]) for j in range(len(row[i]))] for i in range(len(row))]
                tables.append((column_name, row))
                context= {
                    'tables': tables,
                    'name': name 
                }
        except Exception as e:
            error = str(e)
            context= {
                'error': error
            }
            template = loader.get_template('website/error_request.html')
            return HttpResponse(template.render(context, request))

    return HttpResponse(template.render(context, request))
