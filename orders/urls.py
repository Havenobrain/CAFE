from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from .views import OrderViewSet


router = DefaultRouter()
router.register(r'api/orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', views.order_list, name='order_list'),  
    path('add/', views.add_order, name='add_order'),  
    path('update/<int:order_id>/', views.update_status, name='update_status'),  
    path('delete/<int:order_id>/', views.delete_order, name='delete_order'),  
    path('revenue/', views.revenue_report, name='revenue_report'),  
    path('edit/<int:order_id>/', views.edit_order, name='edit_order'),  
]

urlpatterns += router.urls
