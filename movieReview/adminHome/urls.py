from django.urls import path
from adminHome import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('index',views.index),
    path('dataMG',views.dataMG),
    path('reportCM',views.reportCM),
    path('dashBD',views.dashBD),
    path('',views.login),
    path('calender',views.calender),
    
]