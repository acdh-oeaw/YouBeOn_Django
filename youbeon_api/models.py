from django.db import models

# Create your models here.
class Ort(models.Model):
    id = models.AutoField(primary_key=True)
    bezeichnung = models.CharField(max_length=100)
    bemerkung = models.CharField(max_length=200)
    koordinate_b = models.CharField(max_length=50)
    koordinate_l = models.CharField(max_length=50)
    osm_id = models.IntegerField()

class Influencer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    bemerkung = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    osm_id = models.IntegerField()
    gnd = models.CharField(max_length=100)


class Kategorie(models:Model):
    id = id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class Religion(models:Model):
    id = id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class Idee(models:Model):
    id = id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

