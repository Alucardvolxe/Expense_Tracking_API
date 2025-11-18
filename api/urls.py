from django.urls import path, re_path
from .views import CategoryList,CategoryDetail,ExpenseDetail,ExpenseList
urlpatterns = [
    path('expenses/', ExpenseList.as_view()),
    path('expenses/<int:pk>/', ExpenseDetail.as_view()),
    path('categories/', CategoryList.as_view()),
    path('categories/<int:pk>/', CategoryDetail.as_view()),
    

    
] 