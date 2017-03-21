from django.db import models

class Exercice(models.Model):
    #id
    titre = models.TextField()
    numero = models.IntegerField()
    
class Question(models.Model):
    #id (ajoute automatiquement)
    numero = models.IntegerField()
    intitule = models.TextField()
    requete = models.TextField()

class Contient_Exercice_Table(models.Model):
    #id
    idExercice = models.IntegerField()
    idTable = models.IntegerField()

class Table(models.Model):
    #id
    nom = models.CharField(max_length=100)
    attribut = models.TextField()
    remplissage = models.TextField()
    
class Contient_Exercice_Question(models.Model):
    #id
    idExercice = models.IntegerField()
    idQuestion = models.IntegerField()
