from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField()

    def __str__(self):
        return self.title
    
class Expenses(models.Model):
    title = models.CharField(max_length=200)
    date_added = models.DateField(auto_now_add=True)
    note = models.CharField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.title}  {self.note}'