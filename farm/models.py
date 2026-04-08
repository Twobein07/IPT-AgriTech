from django.db import models

class CropType(models.TextChoices):
    CACAO = 'CACAO', 'Cacao'
    RICE = 'RICE', 'Rice'
    BANANA = 'BANANA', 'Banana'
    VEGETABLES = 'VEGETABLES', 'Vegetables'
    CORN = 'CORN', 'Corn'

class Farm(models.Model):
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    crop_type = models.CharField(max_length=20, choices=CropType.choices)
    area_hectares = models.FloatField(default=1.0)
    installed_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.crop_type}"

class SensorNode(models.Model):
    node_id = models.CharField(max_length=50, unique=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='nodes')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    installed_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.node_id} - {self.farm.name}"

class SensorReading(models.Model):
    node = models.ForeignKey(SensorNode, on_delete=models.CASCADE, related_name='readings')
    timestamp = models.DateTimeField()
    soil_moisture = models.FloatField(help_text="Percentage")
    soil_temperature = models.FloatField(help_text="Celsius")
    soil_pH = models.FloatField()
    air_temperature = models.FloatField(help_text="Celsius")
    humidity = models.FloatField(help_text="Percentage")
    leaf_wetness = models.FloatField(help_text="Percentage")
    
    def __str__(self):
        return f"{self.node.node_id} - {self.timestamp}"

class DiseaseRisk(models.Model):
    RISK_LEVELS = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='disease_risks')
    timestamp = models.DateTimeField()
    disease_type = models.CharField(max_length=100)
    risk_level = models.CharField(max_length=10, choices=RISK_LEVELS)
    probability = models.FloatField()
    recommendation = models.TextField()
    is_resolved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.disease_type} - {self.risk_level} - {self.farm.name}"

class IrrigationRecommendation(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='irrigation_recs')
    timestamp = models.DateTimeField()
    needed = models.BooleanField()
    water_amount_liters = models.FloatField(null=True, blank=True)
    reason = models.TextField()
    days_until_next = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{' irrigate' if self.needed else 'delay'} - {self.farm.name}"

class YieldForecast(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='yield_forecasts')
    timestamp = models.DateTimeField()
    predicted_yield_kg = models.FloatField()
    harvest_date = models.DateField()
    confidence = models.FloatField(help_text="Percentage")
    crop_condition = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.farm.name} - {self.predicted_yield_kg}kg"
