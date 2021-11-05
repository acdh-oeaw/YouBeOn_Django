from django.db import models
from rest_framework import serializers

from youbeon_api.models import Idee, Influencer, Kategorie, Ort, Religion




class InfluencerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Influencer
        fields = ('id', 'name', 'bemerkung', 'location', 'osm_id', 'gnd', 'kategorie', 'idee', 'religion', 'interview', 'link')

class OrtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ort
        fields = ('id', 'bezeichnung', 'bemerkung', 'koordinate_l', 'koordinate_b', 'osm_id', 'kategorie', 'idee', 'religion', 'interview')

class IdeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idee
        fields = ('id', 'name', 'cooccurence', 'cluster')

class ReligionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Religion
        fields = ('id', 'name')

class KategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategorie
        fields = ('id', 'name')
