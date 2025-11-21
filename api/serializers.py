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
    



class UserSerialzer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','password','email']