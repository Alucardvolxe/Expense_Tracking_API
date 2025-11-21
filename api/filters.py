import django_filters
from .models import Expenses

class ExpensesFilter(django_filters.FilterSet):
    class Meta:
        model = Expenses
        fields={'name':['contains','exact'],
                'category':['exact'],
                'amount_spent':['range','lt','gt','exact'],
                'date_added':['month','day','year'],
                }


