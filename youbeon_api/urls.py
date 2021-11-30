from django.urls import include, path

from rest_framework import routers

from youbeon_api import views
from youbeon_api.views import IdeeViewSet, KategorieViewSet, ReligionViewSet, InfluencerViewSet, OrtViewSet

router = routers.DefaultRouter()
router.register(r'idee', IdeeViewSet)
router.register(r'kategorie', KategorieViewSet)
router.register(r'religion', ReligionViewSet)
router.register(r'influencer', InfluencerViewSet)
router.register(r'ort', OrtViewSet)

urlpatterns = [
   path('idee/filter/', views.idee_detail),
   path('kategorie/filter/', views.kategorie_detail),
   path('idee/menge/', views.idee_menge),
   path('', include(router.urls)),
   path('upload/', views.import_data),
   path('accounts/', include('django.contrib.auth.urls'))
]