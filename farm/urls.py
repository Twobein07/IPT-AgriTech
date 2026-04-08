from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'farms', views.FarmViewSet)
router.register(r'readings', views.SensorReadingViewSet)
router.register(r'disease-risks', views.DiseaseRiskViewSet)

urlpatterns = [
    # API FIRST (so it doesn't get caught by web views)
    path('api/', include(router.urls)),
    
    # Web Pages
    path('', views.dashboard, name='dashboard'),
    path('farms/', views.farms_view, name='farms'),
    path('sensors/', views.sensors_view, name='sensors'),
    path('disease/', views.disease_view, name='disease'),
    path('irrigation/', views.irrigation_view, name='irrigation'),
    path('yield/', views.yield_view, name='yield'),
    
    # CRUD: Farm
    path('farms/create/', views.farm_create, name='farm_create'),
    path('farms/edit/<int:farm_id>/', views.farm_edit, name='farm_edit'),
    path('farms/delete/<int:farm_id>/', views.farm_delete, name='farm_delete'),
    
    # CRUD: Sensor Node
    path('sensors/create/', views.node_create, name='node_create'),
    path('sensors/delete/<int:node_id>/', views.node_delete, name='node_delete'),
    
    # CRUD: Disease Risk
    path('disease/resolve/<int:risk_id>/', views.risk_resolve, name='risk_resolve'),
    
    # CRUD: Irrigation
    path('irrigation/delete/<int:irr_id>/', views.irrigation_delete, name='irrigation_delete'),
]

# API CRUD Cheatcode:
# GET    /api/farms/           -> list (Read)
# POST   /api/farms/           -> create (Create)
# GET    /api/farms/{id}/      -> retrieve (Read)
# PUT    /api/farms/{id}/      -> update (Update)
# DELETE /api/farms/{id}/      -> delete (Delete)