from rest_framework import serializers
from .models import Expenses, Category
from django.contrib.auth.models import User
class UserSerialzer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','password','email']
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']

class ExpensesSerializer(serializers.ModelSerializer):
   
    category = CategorySerializer(read_only=True)
    
    category_data = serializers.DictField(write_only=True)

    class Meta:
        model = Expenses
        fields = ('name','note', 'amount_spent', 'category', 'category_data', 'date_added', 'user')

    def create(self, validated_data):
        category_input = validated_data.pop('category_data')
        category, _ = Category.objects.get_or_create(title=category_input['title'])
        expense = Expenses.objects.create(category=category, **validated_data)
        return expense
    
    def validate_amount_spent(self,value):
        if value<0 or value>9999999999:
            raise serializers.ValidationError(
                'Price must be in the range of 1 and 9999999999'
            )
        return value

class MonthSummarySerializer(serializers.Serializer):
    month = serializers.CharField()
    total_for_month = serializers.DictField(child=serializers.DictField())
    total_spent=serializers.DecimalField(max_digits=10,decimal_places=2)

class YearSummarySerializer(serializers.Serializer):
    year = serializers.CharField(max_length=7, required=False)
    total_for_year = serializers.DictField(child=serializers.DictField())
    yearly_totals = serializers.DictField() 


        