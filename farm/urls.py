from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'farms', views.FarmViewSet)
router.register(r'readings', views.SensorReadingViewSet)
router.register(r'disease-risks', views.DiseaseRiskViewSet)

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('farms/', views.farms_view, name='farms'),
    path('sensors/', views.sensors_view, name='sensors'),
    path('disease/', views.disease_view, name='disease'),
    path('irrigation/', views.irrigation_view, name='irrigation'),
    path('yield/', views.yield_view, name='yield'),
    path('api/', include(router.urls)),
]
