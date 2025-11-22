from django.urls import path, re_path
from .views import CategoryList,CategoryDetail,ExpenseDetail,ExpenseList,ExpenseCreate,CreateCategory,ExpensesSummaryview

from .views import login,signup,test_token
urlpatterns = [
    path('', ExpenseList.as_view()),
    path('expense/create',ExpenseCreate.as_view()),
    path('expenses/<int:pk>/', ExpenseDetail.as_view()),
    path('categories/', CategoryList.as_view()),
    path('category/create', CreateCategory.as_view()),
    path('categories/<int:pk>/', CategoryDetail.as_view()),
    path('expense/summary', ExpensesSummaryview.as_view()),
    re_path('login', login),
    re_path('signup' ,signup),
    re_path('test_token', test_token),
    

    
] 








