from django.db.models import Avg
from django.utils.timezone import now
from django.views.generic import TemplateView

from municipalities.models import Province
from observations.models import Observation, Sensor


class IndexView(TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        provinces = Province.objects.filter(active=True).prefetch_related('municipality_set').all()

        observations = Observation.objects.filter(
            sensor__municipality__province__in=provinces,
            type__in=['pm10', 'pm25', 'temp', 'rh']
        ).values(
            'sensor__municipality__province',
            'sensor__municipality',
            'type'
        ).annotate(
            avg_value=Avg('value')
        )

        averages_dict = {}
        for obs in observations:
            province_id = obs['sensor__municipality__province']
            municipality_id = obs['sensor__municipality']
            obs_type = obs['type']
            avg_value = obs['avg_value']

            if province_id not in averages_dict:
                averages_dict[province_id] = {}

            if municipality_id not in averages_dict[province_id]:
                averages_dict[province_id][municipality_id] = {}

            averages_dict[province_id][municipality_id][obs_type] = avg_value

        for province in provinces:
            for municipality in province.municipality_set.all():
                municipality.averages = {
                    'pm10': averages_dict.get(province.id, {}).get(municipality.id, {}).get('pm10', None),
                    'pm25': averages_dict.get(province.id, {}).get(municipality.id, {}).get('pm25', None),
                    'temp': averages_dict.get(province.id, {}).get(municipality.id, {}).get('temp', None),
                    'rh': averages_dict.get(province.id, {}).get(municipality.id, {}).get('rh', None),
                    'sensor_count': Sensor.objects.filter(municipality=municipality, observation__isnull=False).distinct().count()
                }

        context['provinces'] = provinces
        context['now'] = now()

        latest_observation = Observation.objects.order_by('-timestamp').values('timestamp').first()
        context['latest_data_timestamp'] = latest_observation['timestamp'] if latest_observation else None
        return context


def trigger_error(request):
    division_by_zero = 1/0
