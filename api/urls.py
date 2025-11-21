from django.urls import path, re_path
from .views import CategoryList,CategoryDetail,ExpenseDetail,ExpenseList,ExpenseCreate,CreateCategory

from .views import login,signup,test_token
urlpatterns = [
    path('expenses/', ExpenseList.as_view()),
    path('create_expense/',ExpenseCreate.as_view()),
    path('expenses/<int:pk>/', ExpenseDetail.as_view()),
    path('categories/', CategoryList.as_view()),
    path('create_category/', CreateCategory.as_view()),
    path('categories/<int:pk>/', CategoryDetail.as_view()),
    re_path('login', login),
    re_path('signup' ,signup),
    re_path('test_token', test_token),
    

    
] 








