from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Avg, Max, Count
from .models import Farm, SensorNode, SensorReading, DiseaseRisk, IrrigationRecommendation, YieldForecast, CropType
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
        'irr_delayed': irrigations.filter(needed=False).count(), 'forecasts': YieldForecast.objects.all(),
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

# CRUD: Farm Create
def farm_create(request):
    if request.method == 'POST':
        Farm.objects.create(
            name=request.POST.get('name'),
            owner=request.POST.get('owner'),
            location=request.POST.get('location'),
            crop_type=request.POST.get('crop_type'),
            area_hectares=float(request.POST.get('area_hectares', 1))
        )
        return redirect('farms')
    crops = CropType.choices
    return render(request, 'farm_form.html', {'action': 'Create', 'crops': crops})

# CRUD: Farm Edit
def farm_edit(request, farm_id):
    farm = Farm.objects.get(id=farm_id)
    if request.method == 'POST':
        farm.name = request.POST.get('name')
        farm.owner = request.POST.get('owner')
        farm.location = request.POST.get('location')
        farm.crop_type = request.POST.get('crop_type')
        farm.area_hectares = float(request.POST.get('area_hectares', 1))
        farm.save()
        return redirect('farms')
    crops = CropType.choices
    return render(request, 'farm_form.html', {'action': 'Edit', 'farm': farm, 'crops': crops})

# CRUD: Farm Delete
def farm_delete(request, farm_id):
    farm = Farm.objects.get(id=farm_id)
    if request.method == 'POST':
        farm.delete()
        return redirect('farms')
    return render(request, 'confirm_delete.html', {'item': farm, 'type': 'Farm'})

# CRUD: Sensor Node Create
def node_create(request):
    if request.method == 'POST':
        SensorNode.objects.create(
            node_id=request.POST.get('node_id'),
            farm_id=request.POST.get('farm'),
            latitude=float(request.POST.get('latitude', 0)),
            longitude=float(request.POST.get('longitude', 0)),
            is_active=True
        )
        return redirect('sensors')
    farms = Farm.objects.all()
    return render(request, 'node_form.html', {'action': 'Create', 'farms': farms})

# CRUD: Sensor Node Delete
def node_delete(request, node_id):
    node = SensorNode.objects.get(id=node_id)
    if request.method == 'POST':
        node.delete()
        return redirect('sensors')
    return render(request, 'confirm_delete.html', {'item': node, 'type': 'Sensor Node'})

# CRUD: Disease Risk Resolve
def risk_resolve(request, risk_id):
    risk = DiseaseRisk.objects.get(id=risk_id)
    if request.method == 'POST':
        risk.is_resolved = True
        risk.save()
        return redirect('disease')
    return render(request, 'confirm_delete.html', {'item': risk, 'type': 'Disease Risk', 'action': 'Resolve'})

# CRUD: Irrigation Delete
def irrigation_delete(request, irr_id):
    irr = IrrigationRecommendation.objects.get(id=irr_id)
    if request.method == 'POST':
        irr.delete()
        return redirect('irrigation')
    return render(request, 'confirm_delete.html', {'item': irr, 'type': 'Irrigation Rec'})

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
# GET    /api/farms/           -> list farms (GET)
# POST   /api/farms/           -> create farm (POST)
# GET    /api/farms/{id}/      -> get farm (GET)
# PUT    /api/farms/{id}/      -> update farm (PUT)
# DELETE /api/farms/{id}/      -> delete farm (DELETE)