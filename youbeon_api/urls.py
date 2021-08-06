from django.urls import include, path

from rest_framework import routers

from youbeon_api.views import IdeeViewSet, KategorieViewSet, ReligionViewSet, InfluencerViewSet, OrtViewSet, IdeeDetail

router = routers.DefaultRouter()
router.register(r'idee', IdeeViewSet)
router.register(r'kategorie', KategorieViewSet)
router.register(r'religion', ReligionViewSet)
router.register(r'influencer', InfluencerViewSet)
router.register(r'ort', OrtViewSet)

urlpatterns = [
   path('', include(router.urls)),
   path('idee/(?P<pk>[0-9]+)/$', IdeeViewSet.idee_detail)
]