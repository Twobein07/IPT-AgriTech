from django.urls import path, include
from rest_framework.routers import DefaultRouter
from farm import views
from farm.views import FarmViewSet, SensorReadingViewSet, DiseaseRiskViewSet

# API Router
router = DefaultRouter()
router.register(r'farms', FarmViewSet)
router.register(r'readings', SensorReadingViewSet)
router.register(r'disease-risks', DiseaseRiskViewSet)

urlpatterns = [
    # API endpoints - MUST BE FIRST
    path('api/', include(router.urls)),
    
    # Web Pages
    path('', views.dashboard, name='dashboard'),
    path('farms/', views.farms_view, name='farms'),
    path('farms/create/', views.farm_create, name='farm_create'),
    path('farms/edit/<int:farm_id>/', views.farm_edit, name='farm_edit'),
    path('farms/delete/<int:farm_id>/', views.farm_delete, name='farm_delete'),
    path('sensors/', views.sensors_view, name='sensors'),
    path('sensors/create/', views.node_create, name='node_create'),
    path('sensors/delete/<int:node_id>/', views.node_delete, name='node_delete'),
    path('disease/', views.disease_view, name='disease'),
    path('disease/resolve/<int:risk_id>/', views.risk_resolve, name='risk_resolve'),
    path('irrigation/', views.irrigation_view, name='irrigation'),
    path('irrigation/delete/<int:irr_id>/', views.irrigation_delete, name='irrigation_delete'),
    path('yield/', views.yield_view, name='yield'),
]

# API CRUD Cheatcode:
# GET    /api/farms/           -> list (Read)
# POST   /api/farms/           -> create (Create)
# GET    /api/farms/{id}/      -> retrieve (Read)
# PUT    /api/farms/{id}/      -> update (Update)
# DELETE /api/farms/{id}/      -> delete (Delete)