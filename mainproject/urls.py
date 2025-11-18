
from django.contrib import admin
from django.urls import path, include,re_path
import debug_toolbar
from .views import login,signup,test_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
   
    path('api/', include('api.urls')),
    re_path('login', login),
    re_path('signup' ,signup),
    re_path('test_token', test_token),
    
] 
