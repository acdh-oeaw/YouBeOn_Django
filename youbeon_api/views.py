from rest_framework import viewsets

from youbeon_api.serializers import KategorieSerializer, IdeeSerializer, ReligionSerializer, InfluencerSerializer, OrtSerializer
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

class ReligionViewSet(viewsets.ModelViewSet):
   queryset = Religion.objects.all()
   serializer_class = ReligionSerializer