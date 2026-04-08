from rest_framework import serializers
from .models import Farm, SensorNode, SensorReading, DiseaseRisk, IrrigationRecommendation, YieldForecast

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = '__all__'

class SensorNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorNode
        fields = '__all__'

class SensorReadingSerializer(serializers.ModelSerializer):
    node_id = serializers.CharField(source='node.node_id', read_only=True)
    
    class Meta:
        model = SensorReading
        fields = '__all__'

class DiseaseRiskSerializer(serializers.ModelSerializer):
    farm_name = serializers.CharField(source='farm.name', read_only=True)
    
    class Meta:
        model = DiseaseRisk
        fields = '__all__'

class IrrigationRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IrrigationRecommendation
        fields = '__all__'

class YieldForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = YieldForecast
        fields = '__all__'
