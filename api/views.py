
# Create your views here.
from rest_framework import generics
from .models import Category,Expenses
from .serializers import CategorySerializer, ExpensesSerializer

class ExpenseList(generics.ListCreateAPIView):
    serializer_class = ExpensesSerializer


    def get_queryset(self):
        queryset = Expenses.objects.all()
        category = self.request.query_params.get('category')

        if category is not None:
            queryset= queryset.filter(Category=category)

        return queryset


class ExpenseDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=ExpensesSerializer
    queryset = Expenses.objects.all()



class CategoryList(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()



class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()





















