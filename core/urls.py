from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
    path('index', views.index, name='core-index'),
    path('core/', views.core, name='core-core'),
    path('core_detail/<int:pk>/', views.core_detail, name='core-core_detail'),
    path('qr_code/', include('qr_code.urls', namespace="qr_code")),
    path('core_delete/<int:pk>/', views.core_delete, name='core-core_delete'),
    path('core_update/<int:pk>/', views.core_update, name='core-core_update'),
    path('core_history/<int:pk>/', views.core_history, name='core-core_history'),
    path('core_history/<int:pk>/add/', views.core_history_add, name='core-core_history_add'),

]
