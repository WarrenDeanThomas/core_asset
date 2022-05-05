from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.apiGetCoreData),
    path('apiGetCore/<str:pk>/', views.apiGetCore),
    path('apiAddCore/', views.apiAddCore),
    path('apiUpdateCore/<str:pk>/', views.apiUpdateCore, name="apiUpdateCore"),
    path('apiDeleteCore/<str:pk>/', views.apiDeleteCore, name="apiDeleteCore"),
]
