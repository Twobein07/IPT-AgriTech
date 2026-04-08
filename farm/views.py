from django.shortcuts import render
from django.db.models import Avg, Max, Count
from .models import Farm, SensorNode, SensorReading, DiseaseRisk, IrrigationRecommendation, YieldForecast
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import FarmSerializer, SensorReadingSerializer, DiseaseRiskSerializer

# Web Views
def dashboard(request):
    farms = Farm.objects.all()
    nodes = SensorNode.objects.all()
    readings = SensorReading.objects.all()
    risks = DiseaseRisk.objects.all()
    irrigations = IrrigationRecommendation.objects.all()
    forecasts = YieldForecast.objects.all()
    
    farm_data = []
    for farm in farms:
        latest = SensorReading.objects.filter(node__farm=farm).order_by('-timestamp').first()
        active_risks = DiseaseRisk.objects.filter(farm=farm, is_resolved=False).count()
        farm_data.append({'farm': farm, 'latest': latest, 'active_risks': active_risks})
    
    risk_counts = {
        'HIGH': risks.filter(risk_level='HIGH', is_resolved=False).count(),
        'MEDIUM': risks.filter(risk_level='MEDIUM', is_resolved=False).count(),
        'LOW': risks.filter(risk_level='LOW', is_resolved=False).count(),
    }
    
    return render(request, 'dashboard.html', {
        'farms': farms, 'nodes': nodes, 'readings_count': readings.count(),
        'risks_count': risks.count(), 'farm_data': farm_data,
        'risk_counts': risk_counts, 'irr_needed': irrigations.filter(needed=True).count(),
        'irr_delayed': irrigations.filter(needed=False).count(), 'forecasts': forecasts,
    })

def farms_view(request):
    return render(request, 'farms.html', {'farms': Farm.objects.all()})

def sensors_view(request):
    return render(request, 'sensors.html', {'nodes': SensorNode.objects.select_related('farm').all()})

def disease_view(request):
    risks = DiseaseRisk.objects.select_related('farm').order_by('-timestamp')
    filter_level = request.GET.get('level')
    if filter_level:
        risks = risks.filter(risk_level=filter_level)
    return render(request, 'disease.html', {'risks': risks, 'filter_level': filter_level})

def irrigation_view(request):
    irrigations = IrrigationRecommendation.objects.select_related('farm').order_by('-timestamp')
    filter_status = request.GET.get('status')
    if filter_status == 'needed':
        irrigations = irrigations.filter(needed=True)
    elif filter_status == 'delayed':
        irrigations = irrigations.filter(needed=False)
    return render(request, 'irrigation.html', {'irrigations': irrigations, 'filter_status': filter_status})

def yield_view(request):
    return render(request, 'yield.html', {'forecasts': YieldForecast.objects.select_related('farm').all()})

# API Views
class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    
    @action(detail=True, methods=['get'])
    def latest_reading(self, request, pk=None):
        farm = self.get_object()
        reading = SensorReading.objects.filter(node__farm=farm).order_by('-timestamp').first()
        return Response(SensorReadingSerializer(reading).data if reading else {})

class SensorReadingViewSet(viewsets.ModelViewSet):
    queryset = SensorReading.objects.all().order_by('-timestamp')[:100]
    serializer_class = SensorReadingSerializer

class DiseaseRiskViewSet(viewsets.ModelViewSet):
    queryset = DiseaseRisk.objects.all()
    serializer_class = DiseaseRiskSerializer
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        return Response(DiseaseRiskSerializer(DiseaseRisk.objects.filter(is_resolved=False), many=True).data)

# API Cheatcode:
# GET    /api/farms/           -> list farms
# POST   /api/farms/           -> create farm
# GET    /api/farms/{id}/      -> get farm
# PUT    /api/farms/{id}/      -> update farm  
# DELETE /api/farms/{id}/      -> delete farm
