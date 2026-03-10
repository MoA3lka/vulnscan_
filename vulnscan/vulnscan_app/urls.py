from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/',views.login_view, name="login"),   

    path('dashboard/',views.dashboard, name="dashboard"),    

    path('start_scan/',views.start_scan, name="start_scan"),   
    path('Scan_Result/',views.results, name="Scan_Result"),    
    path('alerts/',views.alerts, name="alerts"),
    
]

