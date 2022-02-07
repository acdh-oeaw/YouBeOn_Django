from email.policy import default
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.forms import BooleanField

# Create your models here.


class Kategorie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class Religion(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class Idee(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    cluster = models.CharField(max_length=100, null=True, blank=True)
    cooccurence = ArrayField(models.CharField(
        max_length=100), null=True, blank=True)
    interviews = ArrayField(models.CharField(
        max_length=100), default=list)


class Ort(models.Model):
    id = models.AutoField(primary_key=True)
    bezeichnung = models.CharField(max_length=100)
    bemerkung = models.CharField(max_length=200, null=True, blank=True)
    koordinate_b = models.CharField(max_length=50, null=True, blank=True)
    koordinate_l = models.CharField(max_length=50, null=True, blank=True)
    kategorie = models.ManyToManyField(Kategorie)
    idee = models.ManyToManyField(Idee)
    religion = models.ManyToManyField(Religion)
    interview = models.CharField(max_length=100)


class Influencer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    bemerkung = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    kategorie = models.ManyToManyField(Kategorie)
    idee = models.ManyToManyField(Idee)
    religion = models.ManyToManyField(Religion)
    trueReligion = models.BooleanField(default=False)
    link = models.CharField(max_length=200, null=True, blank=True)
    mentions = models.IntegerField(null=True, blank=True)
    interviews = ArrayField(models.CharField(
        max_length=100), null=True, blank=True)
