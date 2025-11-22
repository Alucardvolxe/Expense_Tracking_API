import django_filters
from .models import Expenses

class ExpensesFilter(django_filters.FilterSet):
    class Meta:
        model = Expenses
        fields={'name':['contains','exact'],
                'category':['exact'],
                'amount_spent':['range','lt','gt','exact'],
                'date_added':['month','day','year','range'],
                }


class Expense_summary(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name="date_added", lookup_expr="gte")
    to_date = django_filters.DateFilter(field_name="date_added", lookup_expr="lte")
    

    class Meta:
        model = Expenses
        fields = ['from_date', 'to_date']
