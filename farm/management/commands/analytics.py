from django.core.management.base import BaseCommand
from django.db.models import Avg, Max, Min, Count, Q
from farm.models import Farm, SensorNode, SensorReading, DiseaseRisk, IrrigationRecommendation, YieldForecast

class Command(BaseCommand):
    help = 'Run FarmShield Analytics Report'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('FARMSHIELD AGRITECH ANALYTICS'))
        self.stdout.write(self.style.SUCCESS('=' * 60))

        # 1. Soil moisture by crop type
        self.stdout.write(self.style.WARNING('\n1. AVERAGE SOIL MOISTURE BY CROP'))
        self.stdout.write(self.style.WARNING('-' * 40))
        for crop in Farm.CropType.choices:
            avg_moisture = SensorReading.objects.filter(
                node__farm__crop_type=crop[0]
            ).aggregate(Avg('soil_moisture'))
            self.stdout.write(f'{crop[1]}: {avg_moisture["soil_moisture__avg"] or 0:.1f}%')

        # 2. Disease risk distribution
        self.stdout.write(self.style.WARNING('\n2. DISEASE RISK BY FARM'))
        self.stdout.write(self.style.WARNING('-' * 40))
        for farm in Farm.objects.all():
            risks = DiseaseRisk.objects.filter(farm=farm)
            high = risks.filter(risk_level='HIGH').count()
            medium = risks.filter(risk_level='MEDIUM').count()
            self.stdout.write(f'{farm.name}: HIGH={high}, MEDIUM={medium}, LOW={risks.filter(risk_level="LOW").count()}')

        # 3. Irrigation needs
        self.stdout.write(self.style.WARNING('\n3. IRRIGATION RECOMMENDATIONS'))
        self.stdout.write(self.style.WARNING('-' * 40))
        needed = IrrigationRecommendation.objects.filter(needed=True).count()
        delayed = IrrigationRecommendation.objects.filter(needed=False).count()
        self.stdout.write(f'Irrigation Needed: {needed}')
        self.stdout.write(f'Delay Irrigation: {delayed}')

        # 4. Temperature & Humidity extremes
        self.stdout.write(self.style.WARNING('\n4. ENVIRONMENTAL EXTREMES'))
        self.stdout.write(self.style.WARNING('-' * 40))
        ext = SensorReading.objects.aggregate(
            max_temp=Max('air_temperature'),
            min_temp=Min('air_temperature'),
            max_humidity=Max('humidity'),
            min_humidity=Min('humidity')
        )
        self.stdout.write(f'Max Air Temp: {ext["max_temp"]}C')
        self.stdout.write(f'Min Air Temp: {ext["min_temp"]}C')
        self.stdout.write(f'Max Humidity: {ext["max_humidity"]}%')
        self.stdout.write(f'Min Humidity: {ext["min_humidity"]}%')

        # 5. Yield forecasts
        self.stdout.write(self.style.WARNING('\n5. YIELD FORECASTS'))
        self.stdout.write(self.style.WARNING('-' * 40))
        for forecast in YieldForecast.objects.all():
            self.stdout.write(f'{forecast.farm.name}: {forecast.predicted_yield_kg:.0f}kg ({forecast.crop_condition})')

        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
