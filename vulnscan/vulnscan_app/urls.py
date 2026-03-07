from django.urls import path
from . import views


urlpatterns = [
    path('',views.dashboard, name="dashboard"),    
    path('',views.start_scan, name="scan"),   
    path('',views.results, name="results"),    
    path('',views.alerts, name="alerts"),
    
]

