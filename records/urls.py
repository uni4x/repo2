# records/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('record/new/', views.record_create, name='record_create'),
    path('record/<int:pk>/', views.record_detail, name='record_detail'),
    path('record/<int:pk>/edit/', views.record_edit, name='record_edit'),
    path('record/<int:pk>/delete/', views.record_delete, name='record_delete'),
    path('monthly/<int:year>/<int:month>/', views.monthly_view, name='monthly_view'),
    path('weight-trend/', views.weight_trend_view, name='weight_trend'),
    path('graph/', views.graph_view, name='graph'),
    path('calculate_bmi/', views.calculate_bmi, name='calculate_bmi'),
]
