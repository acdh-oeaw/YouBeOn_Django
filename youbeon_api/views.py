from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from youbeon_api.serializer import KategorieSerializer, IdeeSerializer, ReligionSerializer, InfluencerSerializer, OrtSerializer
from youbeon_api.models import Kategorie, Idee, Religion, Influencer, Ort


class InfluencerViewSet(viewsets.ModelViewSet):
    queryset = Influencer.objects.all()
    serializer_class = InfluencerSerializer


class OrtViewSet(viewsets.ModelViewSet):
    queryset = Ort.objects.all()
    serializer_class = OrtSerializer


class KategorieViewSet(viewsets.ModelViewSet):
    queryset = Kategorie.objects.all()
    serializer_class = KategorieSerializer


class IdeeViewSet(viewsets.ModelViewSet):
    queryset = Idee.objects.all()
    serializer_class = IdeeSerializer

    @csrf_exempt
    def idee_detail(request, *pk):
        try:
            snippet = Idee.objects.filter(pk__in=pk)
        except Idee.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            serializer = IdeeSerializer(snippet)
            return JsonResponse(serializer.data)


class ReligionViewSet(viewsets.ModelViewSet):
    queryset = Religion.objects.all()
    serializer_class = ReligionSerializer
