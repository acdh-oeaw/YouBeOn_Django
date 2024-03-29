from django.db import connection
from rest_framework import viewsets
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.fields import CharField
from rest_framework.parsers import JSONParser
from collections import Counter
from django import forms
from csv import reader
from django.contrib.auth.decorators import login_required

from youbeon_api.serializer import KategorieSerializer, IdeeSerializer, ReligionSerializer, InfluencerSerializer, OrtSerializer
from youbeon_api.models import Kategorie, Idee, Religion, Influencer, Ort


class UploadFileForm(forms.Form):
    connections = forms.FileField()
    accounts = forms.FileField()
    koordinaten = forms.FileField()
    zitate = forms.FileField()


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
    orte = OrtSerializer(Ort.objects.filter(
        religion=religionGet), many=True).data
    influencer = InfluencerSerializer(
        Influencer.objects.filter(religion=religionGet), many=True).data
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


def trunc_at(s, d, n=2):
    "Returns s truncated at the n'th (2nd by default) occurrence of the delimiter, d."
    return d.join(s.split(d, n)[:n])


def getName(idea):
    return idea.name


@login_required
def import_data(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            connections = request.FILES["connections"].get_array()
            accounts = request.FILES["accounts"].get_array()
            koordinaten = request.FILES["koordinaten"].get_array()
            quotes = request.FILES["zitate"].get_array()
            # check if data is in the correct format
            if(connections[0] == ['ID', 'Referenz', 'Kodes', 'Dokument']):
                # get a clean slate before adding new data (ideally that wouldnt be necessary -> only add elements that do not exist yet and deal with connections accordingly => should be done later)
                Ort.objects.all().delete()
                Influencer.objects.all().delete()
                Idee.objects.all().delete()
                Religion.objects.all().delete()
                Kategorie.objects.all().delete()
                for entry in connections:
                    kodes = entry[2]
                    kodes = kodes.split('\n')
                    trueReligionField = False
                    # variables for Influencer/Ort
                    influencerVerknüpfungen = []
                    ortVerknüpfungen = []
                    ideen = []
                    kategorien = []
                    religionen = []
                    if(any(item.replace(" ", "") == 'Insta:Religion' for item in kodes)):
                        trueReligionField = True
                    for data in kodes:
                        if(data.startswith('I:')):
                            nameToAdd = data.replace('I: ', '')
                            tempIdee = Idee.objects.get_or_create(name=nameToAdd)[
                                0]
                            if entry[3].split("-")[1] not in tempIdee.interviews:
                                tempIdee.interviews.append(
                                    entry[3].split("-")[1])
                            tempIdee.save()
                            ideen.append(tempIdee)

                        elif(data.startswith('R:')):
                            nameToAdd = data.replace('R: ', '')
                            religionen.append(
                                Religion.objects.get_or_create(name=nameToAdd)[0])

                        elif(data.startswith('K:')):
                            nameToAdd = data.replace('K: ', '')
                            kategorien.append(
                                Kategorie.objects.get_or_create(name=nameToAdd)[0])

                        elif(data.startswith('A:')):
                            nameToAdd = data.replace('A: ', '')
                            filteredLinks = filter(
                                lambda x: x[1] == data, accounts)
                            influencerVerknüpfungen.append(
                                [nameToAdd, list(filteredLinks)[0][2], entry[3].split("-")[1]])

                        elif(data.startswith('O: ') or data.startswith('OS: ') or data.startswith('OR: ') or data.startswith('OL: ')):
                            nameToAdd = data.replace('O: ', '')
                            nameToAdd = nameToAdd.replace('OS: ', '')
                            nameToAdd = nameToAdd.replace('OR: ', '')
                            nameToAdd = nameToAdd.replace('OL: ', '')
                            filteredCoordinates = filter(
                                lambda x: x[1] == data, koordinaten)
                            listCoordinatees = list(filteredCoordinates)
                            if(listCoordinatees != []):
                                coordRemoveDouble = listCoordinatees[0][2].split(
                                    ' - ')[0].replace(' ', '')
                                splitCoordinates = [0, 0]
                                splitCoordinates[1] = trunc_at(
                                    coordRemoveDouble, ',')
                                splitCoordinates[0] = coordRemoveDouble.replace(
                                    splitCoordinates[1] + ',', '')
                                splitCoordinates[0].replace(',', '.')
                                splitCoordinates[1].replace(',', '.')
                            else:
                                splitCoordinates = ['noData', 'noData']
                            ortVerknüpfungen.append(
                                [nameToAdd, splitCoordinates, entry[3]]
                            )

                    for influencer in influencerVerknüpfungen:
                        influencerUnit = Influencer.objects.get_or_create(
                            name=influencer[0], link=influencer[1])[0]
                        influencerUnit.trueReligion = trueReligionField
                        if (influencerUnit.mentions is not None):
                            influencerUnit.mentions += 1
                            if influencer[2] not in influencerUnit.interviews:
                                influencerUnit.interviews.append(influencer[2])
                        else:
                            influencerUnit.interviews = [influencer[2]]
                            influencerUnit.mentions = 1
                        for idee in ideen:
                            influencerUnit.idee.add(idee)
                        for kategorie in kategorien:
                            influencerUnit.kategorie.add(kategorie)
                        for religion in religionen:
                            influencerUnit.religion.add(religion)
                        influencerUnit.save()

                    for ort in ortVerknüpfungen:
                        ortUnit = Ort.objects.get_or_create(
                            bezeichnung=ort[0], koordinate_l=ort[1][0], koordinate_b=ort[1][1])[0]
                        for idee in ideen:
                            ortUnit.idee.add(idee)
                        for kategorie in kategorien:
                            ortUnit.kategorie.add(kategorie)
                        for religion in religionen:
                            ortUnit.religion.add(religion)
                        if ortUnit.interview is None:
                            ortUnit.interview = [ort[2]]
                        else:
                            if ort[2] not in ortUnit.interview:
                                ortUnit.interview.append(ort[2])
                        ortUnit.save()

                    for idee in ideen:
                        idee = Idee.objects.get(id=idee.id)
                        for zitateEntry in quotes:
                            if zitateEntry[1].replace("I: ", "") == idee.name:
                                for zitat in zitateEntry[2::]:
                                    if(zitat != '' and zitat not in idee.zitate):
                                        idee.zitate.append(zitat)
                        temp_cooc = list(
                            set(map(getName, ideen)) - set([idee.name]))
                        if(idee.cooccurence != None):
                            idee.cooccurence = idee.cooccurence + \
                                list(set(temp_cooc) - set(idee.cooccurence))
                        else:
                            idee.cooccurence = temp_cooc
                        idee.save()
            else: return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        "upload_form.html",
        {
            "form": form,
            "title": "Datenbank befüllen",
            "header": "Bitte wähle die entsprechenden Dateien aus",
        },
    )
