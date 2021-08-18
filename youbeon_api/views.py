from rest_framework import viewsets
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from collections import Counter
from django import forms

from youbeon_api.serializer import KategorieSerializer, IdeeSerializer, ReligionSerializer, InfluencerSerializer, OrtSerializer
from youbeon_api.models import Kategorie, Idee, Religion, Influencer, Ort


class UploadFileForm(forms.Form):
    file = forms.FileField()

class InfluencerViewSet(viewsets.ModelViewSet):
    queryset = Influencer.objects.all()
    serializer_class = InfluencerSerializer


class OrtViewSet(viewsets.ModelViewSet):
    queryset = Ort.objects.all()
    serializer_class = OrtSerializer


class KategorieViewSet(viewsets.ModelViewSet):
    queryset = Kategorie.objects.all()
    serializer_class = KategorieSerializer

def idee_detail(request):
    try:
        ids = request.GET.get('ids')
        ids = ids.split(',')
        ideen = Idee.objects.filter(pk__in=ids)
    except Idee.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = IdeeSerializer(ideen, many=True)
        return JsonResponse(serializer.data, safe=False)

def kategorie_detail(request):
    try:
        ids = request.GET.get('ids')
        ids = ids.split(',')
        kat = Kategorie.objects.filter(pk__in=ids)
    except Idee.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = KategorieSerializer(kat, many=True)
        return JsonResponse(serializer.data, safe=False)

def idee_menge(request):
    religionGet = request.GET.get('religion')
    orte = OrtSerializer(Ort.objects.filter(religion = religionGet), many=True).data
    influencer = InfluencerSerializer(Influencer.objects.filter(religion = religionGet), many=True).data
    allIdeas = []
    for ort in orte:
        allIdeas.extend(ort['idee'])
    for influ in influencer:
        allIdeas.extend(influ['idee'])

    return JsonResponse(Counter(allIdeas))

class IdeeViewSet(viewsets.ModelViewSet):
    queryset = Idee.objects.all()
    serializer_class = IdeeSerializer


class ReligionViewSet(viewsets.ModelViewSet):
    queryset = Religion.objects.all()
    serializer_class = ReligionSerializer

def import_data(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)

        def choice_func(row):
            q = Question.objects.filter(slug=row[0])[0]
            row[0] = q
            return row

        if form.is_valid():
            request.FILES["file"].save_book_to_database(
                models=[Question, Choice],
                initializers=[None, choice_func],
                mapdicts=[
                    ["question_text", "pub_date", "slug"],
                    {"Question": "question", "Choice": "choice_text", "Votes": "votes"},
                ],
            )
            return redirect("handson_view")
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        "upload_form.html",
        {
            "form": form,
            "title": "Import excel data into database example",
            "header": "Please upload sample-data.xls:",
        },
    )
