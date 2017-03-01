from django.db import models

class Question(models.Model):
    #id (ajoute automatiquement)
    intitule = models.TextField()
    requete = models.TextField()

class Contient(models.Model):
    #id
    idQuestion = models.IntegerField()
    idTable = models.IntegerField()

class Table(models.Model):
    #id
    nom = models.CharField(max_length=100)
    attribut = models.TextField()
    remplissage = models.TextField()
