import django_filters
from django_filters import rest_framework as filters
from .models import Expenses

class ExpensesFilter(django_filters.FilterSet):
    class Meta:
        model = Expenses
        fields={'name':['contains','exact'],
                'category':['exact'],
                'amount_spent':['range','lt','gt','exact'],
                'date_added':['month','day','year','range'],
                }

class ExpensesummaryFilter(filters.FilterSet):
    month = filters.NumberFilter(field_name='date_added', lookup_expr='month')
    user = filters.NumberFilter(field_name='user_id')
    category = filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    class Meta:
        model = Expenses
        fields = ['month', 'user', 'category']
