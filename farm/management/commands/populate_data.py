from django.core.management.base import BaseCommand
from farm.models import Farm, SensorNode, SensorReading, DiseaseRisk, IrrigationRecommendation, YieldForecast, CropType
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Populate FarmShield AgriTech with simulated sensor data'

    def handle(self, *args, **options):
        self.stdout.write('Creating farms...')
        farms_data = [
            {'name': 'Green Valley Farm', 'owner': 'Juan dela Cruz', 'location': 'Benguet', 'crop_type': 'VEGETABLES', 'area_hectares': 2.5},
            {'name': 'Sunrise Cacao Plantation', 'owner': 'Maria Santos', 'location': 'Davao', 'crop_type': 'CACAO', 'area_hectares': 5.0},
            {'name': 'Riverside Rice Fields', 'owner': 'Pedro Garcia', 'location': 'Nueva Ecija', 'crop_type': 'RICE', 'area_hectares': 10.0},
            {'name': 'Highland Banana Grove', 'owner': 'Ana Lopez', 'location': 'Cebu', 'crop_type': 'BANANA', 'area_hectares': 3.5},
            {'name': 'Golden Corn Farm', 'owner': 'Carlos Reyes', 'location': 'Pampanga', 'crop_type': 'CORN', 'area_hectares': 8.0},
        ]
        
        farms = [Farm.objects.create(**f) for f in farms_data]
        
        self.stdout.write('Creating sensor nodes...')
        nodes = []
        for farm in farms:
            for i in range(2):
                node = SensorNode.objects.create(
                    node_id=f"FS-{farm.name[:3].upper()}-{random.randint(100,999)}",
                    farm=farm,
                    latitude=random.uniform(9.5, 18.5),
                    longitude=random.uniform(116.5, 126.5),
                    is_active=True
                )
                nodes.append(node)
        
        self.stdout.write('Creating sensor readings...')
        base_time = timezone.now() - timedelta(days=30)
        
        for node in nodes:
            for hour in range(100):
                timestamp = base_time + timedelta(hours=hour)
                
                is_day = 6 <= timestamp.hour <= 18
                
                if node.farm.crop_type == 'RICE':
                    soil_moisture = random.uniform(60, 90) if is_day else random.uniform(70, 95)
                elif node.farm.crop_type == 'CACAO':
                    soil_moisture = random.uniform(50, 75)
                else:
                    soil_moisture = random.uniform(30, 60)
                
                if node.farm.crop_type == 'VEGETABLES':
                    air_temp = random.uniform(20, 32)
                    humidity = random.uniform(60, 85)
                elif node.farm.crop_type == 'CACAO':
                    air_temp = random.uniform(22, 30)
                    humidity = random.uniform(70, 90)
                else:
                    air_temp = random.uniform(25, 35)
                    humidity = random.uniform(50, 80)
                
                leaf_wetness = random.uniform(0, 30) if humidity > 70 else random.uniform(0, 15)
                
                SensorReading.objects.create(
                    node=node,
                    timestamp=timestamp,
                    soil_moisture=round(soil_moisture, 2),
                    soil_temperature=round(air_temp - 3 + random.uniform(-2, 2), 2),
                    soil_pH=round(random.uniform(5.5, 7.0), 2),
                    air_temperature=round(air_temp, 2),
                    humidity=round(humidity, 2),
                    leaf_wetness=round(leaf_wetness, 2)
                )
        
        self.stdout.write('Creating disease risks...')
        for farm in farms:
            for _ in range(3):
                DiseaseRisk.objects.create(
                    farm=farm,
                    timestamp=timezone.now() - timedelta(days=random.randint(1, 20)),
                    disease_type=random.choice(['Fungal Blast', 'Leaf Spot', 'Powdery Mildew', 'Bacterial Wilt', 'Rust']),
                    risk_level=random.choice(['LOW', 'MEDIUM', 'HIGH']),
                    probability=round(random.uniform(0.1, 0.9), 2),
                    recommendation=random.choice([
                        'Apply preventive fungicide within 48 hours',
                        'Increase air circulation around plants',
                        'Reduce leaf wetness duration',
                        'Monitor closely for 7 days',
                        'No action needed - conditions favorable'
                    ]),
                    is_resolved=random.choice([True, True, False])
                )
        
        self.stdout.write('Creating irrigation recommendations...')
        for farm in farms:
            for _ in range(4):
                IrrigationRecommendation.objects.create(
                    farm=farm,
                    timestamp=timezone.now() - timedelta(days=random.randint(1, 25)),
                    needed=random.choice([True, False]),
                    water_amount_liters=random.uniform(500, 2000) if random.choice([True, False]) else None,
                    reason=random.choice([
                        'Soil moisture below crop threshold',
                        'High evapotranspiration due to heat',
                        'Rainfall insufficient for 5+ days',
                        'Optimal moisture levels maintained'
                    ]),
                    days_until_next=random.randint(1, 5) if random.choice([True, False]) else None
                )
        
        self.stdout.write('Creating yield forecasts...')
        for farm in farms:
            YieldForecast.objects.create(
                farm=farm,
                timestamp=timezone.now(),
                predicted_yield_kg=farm.area_hectares * random.uniform(1000, 5000),
                harvest_date=timezone.now().date() + timedelta(days=random.randint(60, 120)),
                confidence=round(random.uniform(0.7, 0.95), 2),
                crop_condition=random.choice(['Excellent', 'Good', 'Fair', 'Needs Attention'])
            )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created:'))
        self.stdout.write(f'  - {len(farms)} farms')
        self.stdout.write(f'  - {len(nodes)} sensor nodes')
        self.stdout.write(f'  - {SensorReading.objects.count()} sensor readings')
        self.stdout.write(f'  - {DiseaseRisk.objects.count()} disease risks')
        self.stdout.write(f'  - {IrrigationRecommendation.objects.count()} irrigation recommendations')
        self.stdout.write(f'  - {YieldForecast.objects.count()} yield forecasts')
