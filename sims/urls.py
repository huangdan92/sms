from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('edit/', views.edit, name='edit'),
    path('delete/', views.delete, name='delete'),
    path('parse_targets/', views.parse_targets, name='parse_targets'),  # 新增
    path('parse_custom_config/', views.parse_custom_config, name='parse_custom_config'),  # 新增
]