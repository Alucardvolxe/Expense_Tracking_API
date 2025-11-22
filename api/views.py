from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
from rest_framework import generics, filters,response
from .models import Category,Expenses
from .serializers import CategorySerializer, ExpensesSerializer
from .filters import ExpensesFilter , Expense_summary
import logging
from django.db.models import Sum
from rest_framework.views import APIView
from django.db.models.functions import ExtractMonth ,ExtractYear

#CRUD FUNCTIONS 
logger = logging.getLogger(__name__)





class ExpenseList(generics.ListAPIView):
    queryset=Expenses.objects.all()
    serializer_class = ExpensesSerializer
    filterset_class = ExpensesFilter
   
    # def get_queryset(self):
    #     queryset = Expenses.objects.all()
    #     category = self.request.query_params.get('category')

    #     if category is not None:
    #         queryset= queryset.filter(Category=category)

        
    #     return queryset
    
     

    

class ExpenseCreate(generics.CreateAPIView):
    serializer_class = ExpensesSerializer




class ExpenseDetail(generics.RetrieveUpdateDestroyAPIView):
    logger.info('Expense detail log')
    serializer_class=ExpensesSerializer
    queryset = Expenses.objects.all()



class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CreateCategory(generics.CreateAPIView):
    serializer_class = CategorySerializer
   



class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()



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
        return Response({"detail":"Not found."}, status = status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user = user)
    serializer = UserSerialzer(instance=user)
    return Response({"token":token.key, "user":serializer.data})


@api_view(['POST'])
def signup(request):
    serializer = UserSerialzer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username = request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token":token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.email))



##Summary views


class ExpensesSummaryview(generics.ListAPIView):
    queryset = Expenses.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = Expense_summary

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        period = request.query_params.get("period", "").lower()

        if period == "month":
            data = (
                qs.annotate(month=ExtractMonth("date_added"))
                  .values("month")
                  .annotate(total=Sum("amount_spent"))
                  .order_by("month")
            )
        elif period == "year":
            data = (
                qs.annotate(year=ExtractYear("date_added"))
                  .values("year")
                  .annotate(total=Sum("amount_spent"))
                  .order_by("year")
            )
        else:
            data = {'Summary':"all time",
                "total": qs.aggregate(total=Sum("amount_spent"))["total"]}

        return Response(data)












