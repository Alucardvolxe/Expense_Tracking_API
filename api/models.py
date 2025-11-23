from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    title = models.CharField()

    def __str__(self):
        return self.title
    
class Expenses(models.Model):
    name = models.CharField(max_length=200)
    amount_spent= models.DecimalField(max_digits=10,decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    note = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null= True)
    def __str__(self):
        return f'{self.title}  {self.note}'