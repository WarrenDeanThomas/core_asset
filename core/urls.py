from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
    path('index', views.index, name='core-index'),
    path('core/', views.core, name='core-core'),
    path('core_data/', views.core_data, name='core-core_data'),
    path('core_detail/<int:pk>/', views.core_detail, name='core-core_detail'),
    path('core_detail_card/<int:pk>/', views.core_detail_card, name='core-core_detail_card'),
    path('qr_code/', include('qr_code.urls', namespace="qr_code")),
    path('core_delete/<int:pk>/', views.core_delete, name='core-core_delete'),
    path('core_update/<int:pk>/', views.core_update, name='core-core_update'),

    path('core_history/', views.core_history_all, name='core-core_history_all'),
    path('core_history/<int:pk>/', views.core_history, name='core-core_history'),
    path('core_history_detail/<int:pk>/', views.core_history_detail, name='core-core_history_detail'),
    path('core_history_update/<int:pk>/', views.core_history_update, name='core-core_history_update'),
    path('core_history_delete/<int:pk>/', views.core_history_delete, name='core-core_history_delete'),
    path('core_history/<int:pk>/add/', views.core_history_add, name='core-core_history_add'),

    path('core_history_dashboard/', views.core_history_dashboard, name='core-core_history_dashboard'),

    path('core_reminder/', views.core_reminder_all, name='core-core_reminder_all'),
    path('core_reminder_upcoming/', views.core_reminder_week, name='core-core_reminder_week'),
    path('core_reminder/<int:pk>/', views.core_reminder, name='core-core_reminder'),
    path('core_reminder_detail/<int:pk>/', views.core_reminder_detail, name='core-core_reminder_detail'),
    path('core_reminder/<int:pk>/add/', views.core_reminder_add, name='core-core_reminder_add'),
    path('core_reminder_update/<int:pk>/', views.core_reminder_update, name='core-core_reminder_update'),
    path('core_reminder_delete/<int:pk>/', views.core_reminder_delete, name='core-core_reminder_delete'),

    path('core_users/', views.core_users, name='core-core_users'),

    path('send_emails/', views.send_email, name='core-core_send_email'),

]
