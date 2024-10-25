# filters.py
import django_filters
from moves.models import Move


class MoveFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    branch_id = django_filters.NumberFilter(field_name='branch_id')

    class Meta:
        model = Move
        fields = ['start_date', 'end_date', 'branch_id']
