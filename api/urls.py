from django.urls import path, re_path
from .views import CategoryList,CategoryDetail,ExpenseDetail,ExpenseList,ExpenseCreate,CreateCategory,MonthlySummaryExpenses,YearlySummaryExpenses
from rest_framework import routers
from .views import login,signup,test_token

urlpatterns = [
    path('expenses/', ExpenseList.as_view()),
    path('expense/create',ExpenseCreate.as_view()),
    path('expense/detail/<int:pk>/', ExpenseDetail.as_view()),
    path('expense/delete/<int:pk>/', ExpenseDetail.as_view()),
    
    path('categories/', CategoryList.as_view()),
    path('category/create', CreateCategory.as_view()),
    path('category/<int:pk>/', CategoryDetail.as_view()),
    path('category/delete/<int:pk>/', CategoryDetail.as_view()),
    path('category/detail/<int:pk>/', CategoryDetail.as_view()),
    path('expense/summary/month', MonthlySummaryExpenses.as_view()),
    path('expense/summary/year', YearlySummaryExpenses.as_view()),
    re_path('login', login),
    re_path('signup' ,signup),
    re_path('test_token', test_token),
    

    
] 








