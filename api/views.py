from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
from rest_framework import generics, filters,response
from .models import Category,Expenses
from .serializers import CategorySerializer, ExpensesSerializer,MonthSummarySerializer,YearSummarySerializer
from .filters import ExpensesFilter , ExpensesummaryFilter
import logging
from django.db.models import Sum ,Aggregate
from rest_framework.views import APIView
from django.db.models.functions import ExtractMonth ,ExtractYear
from rest_framework.permissions import IsAuthenticated
#CRUD FUNCTIONS 
logger = logging.getLogger(__name__)





class ExpenseList(generics.ListAPIView):
    
    serializer_class = ExpensesSerializer
    filterset_class = ExpensesFilter
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        
        return Expenses.objects.filter(user=self.request.user)

    
     

    

class ExpenseCreate(generics.CreateAPIView):
    serializer_class = ExpensesSerializer
    permission_classes =[IsAuthenticated]



class ExpenseDetail(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class=ExpensesSerializer
    queryset = Expenses.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        
        return Expenses.objects.filter(user=self.request.user)


    
     




class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        
        return Category.objects.filter(user=self.request.user)



class CreateCategory(generics.CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        
        return Category.objects.filter(user=self.request.user)





##User login sign up and token validation

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerialzer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username = request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail":"wrong username or password"}, status = status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user = user)
    serializer = UserSerialzer(instance=user)
    return Response({"token":token.key, "user":serializer.data})


@api_view(['POST'])
def signup(request):
    if User.objects.filter(username=request.data.get('username')).exists():
        return Response(
            {
                "detail":"Username already exists"
            },
                status=status.HTTP_400_BAD_REQUEST
        )
    if User.objects.filter(username=request.data.get('email')).exists():
        return Response(
            {
                "detail":"Email already exists"
            },
                status=status.HTTP_400_BAD_REQUEST
        )
    serializer = UserSerialzer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username = request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.get_or_create(user=user)
        return Response({"token":token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.email))



##Summary views





class MonthlySummaryExpenses(generics.GenericAPIView):
    serializer_class = MonthSummarySerializer
    queryset = Expenses.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpensesummaryFilter

    def get(self, request, *args, **kwargs):
        
        qs = self.filter_queryset(self.get_queryset())

        
        category_totals = qs.values('category__title').annotate(
            category_total=Sum('amount_spent')
        )
       
       
        total_for_month = {
            item['category__title']: {
                "category__title": item['category__title'],
                "category_total": item['category_total']
            } for item in category_totals
        }

        month = request.query_params.get('month')
        total_spent = qs.aggregate(total=Sum('amount_spent'))['total'] or Decimal('0')
        data_display = {
            'month': month,
            'total_spent':total_spent,
            'total_for_month': total_for_month,
        }

        serializer = self.get_serializer(data_display)
        return Response(serializer.data)

class YearlySummaryExpenses(generics.GenericAPIView):
    serializer_class = YearSummarySerializer  
    queryset = Expenses.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpensesummaryFilter

    def get(self, request, *args, **kwargs):
        
        qs = self.filter_queryset(self.get_queryset())

        
        year_param = request.query_params.get('year')
        if year_param:
            qs = qs.filter(date_added__year=int(year_param))

        
        yearly_category_totals = (
            qs.annotate(year=ExtractYear('date_added'))
              .values('year', 'category__title')
              .annotate(category_total=Sum('amount_spent'))
              .order_by('year', 'category__title')
        )

       
        total_for_year = {}
        for item in yearly_category_totals:
            yr = str(item['year'])
            cat_title = item['category__title']
            cat_total = float(item['category_total'])  
            if yr not in total_for_year:
                total_for_year[yr] = {}

            total_for_year[yr][cat_title] = {
                "category__title": cat_title,
                "category_total": cat_total
            }

        
        yearly_totals = {}
        years = qs.annotate(year=ExtractYear('date_added')).values_list('year', flat=True).distinct()
        for yr in years:
            total = qs.filter(date_added__year=yr).aggregate(total=Sum('amount_spent'))['total'] or Decimal('0')
            yearly_totals[str(yr)] = float(total)

        
        data_display = {
        "year": year_param,
        "yearly_totals": yearly_totals , 
        "total_for_year": total_for_year,
        }

        serializer = self.get_serializer(data_display)
        return Response(serializer.data)










