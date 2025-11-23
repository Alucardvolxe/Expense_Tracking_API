from rest_framework import serializers
from .models import Expenses, Category
from django.contrib.auth.models import User
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']

class ExpensesSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Expenses
        fields = ('name','amount_spent','category','date_added')
    
    def validate_amount_spent():
        if 'amount_spent'<0 or 'amount_spent>999999':
            raise serializers.ValidationError(
                'Price must be in the range of 1 and 999999'
            )

class CategorySummarySerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(max_length=255)
    category_total_spent=serializers.DecimalField(max_digits=10,decimal_places=2)

class MonthSummarySerializer(serializers.Serializer):
    month = serializers.CharField()
    total_for_month = serializers.DictField(child=serializers.DictField())
    total_spent=serializers.DecimalField(max_digits=10,decimal_places=2)

class YearSummarySerializer(serializers.Serializer):
    year = serializers.CharField(max_length=7, required=False)
    total_for_year = serializers.DictField(child=serializers.DictField())
    yearly_totals = serializers.DictField() 

class UserSerialzer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','password','email']

        