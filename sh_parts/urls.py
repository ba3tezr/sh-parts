"""
URL configuration for sh_parts project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import (
    dashboard, login_view, logout_view,
    vehicles_list, inventory_list, inventory_enhanced, inventory_item_details,
    profitability_report, inventory_count, inventory_dashboard,
    sales_list, customers_list, reports_view, price_management_view,
    vehicle_dismantle_view, save_dismantling
)
from core.views_api import get_system_settings
from core.views_car_api import (
    get_makes, get_models, get_years, decode_vin_view,
    get_standard_parts, get_part_categories, get_parts_by_category
)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # Django i18n (language switching)
    path('i18n/', include('django.conf.urls.i18n')),

    # صفحات النظام
    path('vehicles/', vehicles_list, name='vehicles'),
    path('vehicles/dismantle/<int:vehicle_id>/', vehicle_dismantle_view, name='vehicle_dismantle'),
    path('inventory/', inventory_enhanced, name='inventory'),  # الصفحة المحسّنة كصفحة أساسية
    path('inventory/item/', inventory_item_details, name='inventory_item_details'),
    path('inventory/profitability/', profitability_report, name='profitability_report'),
    path('inventory/count/', inventory_count, name='inventory_count'),
    path('inventory/dashboard/', inventory_dashboard, name='inventory_dashboard'),
    path('sales/', sales_list, name='sales'),
    path('customers/', customers_list, name='customers'),
    path('reports/', reports_view, name='reports'),
    path('price-management/', price_management_view, name='price_management'),
    
    path('admin/', admin.site.urls),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # System Settings API
    path('api/settings/', get_system_settings, name='system_settings'),
    
    # Dismantling API
    path('api/save-dismantling/', save_dismantling, name='save_dismantling'),
    
    # Car API Endpoints
    path('api/cars-data/makes/', get_makes, name='api_car_makes'),
    path('api/cars-data/models/<str:make_name>/', get_models, name='api_car_models'),
    path('api/cars-data/years/<str:make>/<str:model>/', get_years, name='api_car_years'),
    path('api/cars-data/decode-vin/<str:vin>/', decode_vin_view, name='api_decode_vin'),
    path('api/cars-data/standard-parts/', get_standard_parts, name='api_standard_parts'),
    path('api/cars-data/part-categories/', get_part_categories, name='api_part_categories'),
    path('api/cars-data/parts-by-category/<str:category>/', get_parts_by_category, name='api_parts_by_category'),
    
    # API endpoints
    path('api/auth/', include('authentication.urls')),
    path('api/cars/', include('cars.urls')),
    path('api/inventory/', include('inventory.urls')),
    path('api/customers/', include('customers.urls')),
    path('api/sales/', include('sales.urls')),
    path('api/reports/', include('reports.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
