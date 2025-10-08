"""
API Views for Car Data
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .car_api import CarAPI, StandardParts

@require_http_methods(["GET"])
def get_makes(request):
    """الحصول على جميع ماركات السيارات"""
    makes = CarAPI.get_all_makes()
    return JsonResponse({'results': makes})

@require_http_methods(["GET"])
def get_models(request, make_name):
    """الحصول على موديلات ماركة معينة"""
    models = CarAPI.get_models_for_make(make_name)
    return JsonResponse({'results': models})

@require_http_methods(["GET"])
def get_years(request, make, model):
    """الحصول على السنوات المتاحة"""
    years = CarAPI.get_years_for_make_model(make, model)
    return JsonResponse({'results': years})

@require_http_methods(["GET"])
def decode_vin_view(request, vin):
    """فك تشفير VIN"""
    vehicle_info = CarAPI.decode_vin(vin)
    return JsonResponse(vehicle_info)

@require_http_methods(["GET"])
def get_standard_parts(request):
    """الحصول على جميع القطع القياسية"""
    parts = StandardParts.get_all_parts()
    return JsonResponse({'results': parts})

@require_http_methods(["GET"])
def get_part_categories(request):
    """الحصول على فئات القطع"""
    categories = StandardParts.get_categories()
    return JsonResponse({'results': categories})

@require_http_methods(["GET"])
def get_parts_by_category(request, category):
    """الحصول على القطع حسب الفئة"""
    parts = StandardParts.get_parts_by_category(category)
    return JsonResponse({'results': parts})
