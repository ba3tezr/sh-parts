"""
API Integration for Car Data
استخدام VPIC API من NHTSA (مجاني)
"""
import requests
from django.core.cache import cache

class CarAPI:
    """
    API للحصول على بيانات السيارات من NHTSA VPIC
    """
    BASE_URL = "https://vpic.nhtsa.dot.gov/api/vehicles"
    
    @staticmethod
    def get_all_makes():
        """الحصول على جميع ماركات السيارات"""
        cache_key = 'car_makes_all'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            url = f"{CarAPI.BASE_URL}/GetAllMakes?format=json"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                makes = []
                
                if 'Results' in data:
                    for make in data['Results']:
                        makes.append({
                            'id': make['Make_ID'],
                            'name': make['Make_Name']
                        })
                
                # حفظ في الكاش لمدة 30 يوم
                cache.set(cache_key, makes, 60 * 60 * 24 * 30)
                return makes
            
            return []
            
        except Exception as e:
            print(f"Error fetching makes: {e}")
            return []
    
    @staticmethod
    def get_models_for_make(make_name):
        """الحصول على موديلات ماركة معينة"""
        cache_key = f'car_models_{make_name}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            url = f"{CarAPI.BASE_URL}/GetModelsForMake/{make_name}?format=json"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                models = []
                
                if 'Results' in data:
                    for model in data['Results']:
                        models.append({
                            'id': model['Model_ID'],
                            'name': model['Model_Name'],
                            'make_id': model['Make_ID'],
                            'make_name': model['Make_Name']
                        })
                
                # حفظ في الكاش لمدة 30 يوم
                cache.set(cache_key, models, 60 * 60 * 24 * 30)
                return models
            
            return []
            
        except Exception as e:
            print(f"Error fetching models for {make_name}: {e}")
            return []
    
    @staticmethod
    def get_years_for_make_model(make, model):
        """الحصول على السنوات المتاحة لماركة وموديل معين"""
        # في الواقع، NHTSA API لا يوفر نطاق السنوات بشكل مباشر
        # لذا سنستخدم نطاق سنوات افتراضي من 1990 إلى السنة الحالية + 1
        from datetime import datetime
        current_year = datetime.now().year
        
        years = []
        for year in range(1990, current_year + 2):
            years.append({'year': year})
        
        return years
    
    @staticmethod
    def decode_vin(vin):
        """فك تشفير VIN للحصول على معلومات السيارة"""
        cache_key = f'vin_{vin}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            url = f"{CarAPI.BASE_URL}/DecodeVin/{vin}?format=json"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                vehicle_info = {}
                
                if 'Results' in data:
                    for item in data['Results']:
                        variable = item.get('Variable', '')
                        value = item.get('Value', '')
                        
                        if value and value != 'Not Applicable':
                            # جمع المعلومات المهمة فقط
                            if 'Make' in variable:
                                vehicle_info['make'] = value
                            elif 'Model' in variable:
                                vehicle_info['model'] = value
                            elif 'Year' in variable:
                                vehicle_info['year'] = value
                            elif 'Body Class' in variable:
                                vehicle_info['body_class'] = value
                            elif 'Engine' in variable and 'Cylinders' in variable:
                                vehicle_info['engine_cylinders'] = value
                
                # حفظ في الكاش لمدة 365 يوم (VIN لا يتغير)
                cache.set(cache_key, vehicle_info, 60 * 60 * 24 * 365)
                return vehicle_info
            
            return {}
            
        except Exception as e:
            print(f"Error decoding VIN {vin}: {e}")
            return {}


class StandardParts:
    """
    قائمة القطع القياسية لجميع السيارات
    """
    
    # القطع الأساسية مع الأسماء بالعربية والإنجليزية
    PARTS_LIST = [
        # المحرك والأجزاء الميكانيكية
        {'category': 'engine', 'name_en': 'Engine Complete', 'name_ar': 'محرك كامل'},
        {'category': 'engine', 'name_en': 'Engine Block', 'name_ar': 'بلوك المحرك'},
        {'category': 'engine', 'name_en': 'Cylinder Head', 'name_ar': 'رأس المحرك'},
        {'category': 'engine', 'name_en': 'Timing Chain', 'name_ar': 'سلسلة التوقيت'},
        {'category': 'engine', 'name_en': 'Timing Belt', 'name_ar': 'سير التوقيت'},
        {'category': 'engine', 'name_en': 'Oil Pump', 'name_ar': 'طرمبة الزيت'},
        {'category': 'engine', 'name_en': 'Water Pump', 'name_ar': 'طرمبة الماء'},
        {'category': 'engine', 'name_en': 'Alternator', 'name_ar': 'دينامو'},
        {'category': 'engine', 'name_en': 'Starter Motor', 'name_ar': 'سلف'},
        {'category': 'engine', 'name_en': 'Fuel Pump', 'name_ar': 'طرمبة البنزين'},
        {'category': 'engine', 'name_en': 'Radiator', 'name_ar': 'ردياتير'},
        {'category': 'engine', 'name_en': 'Radiator Fan', 'name_ar': 'مروحة الردياتير'},
        {'category': 'engine', 'name_en': 'AC Compressor', 'name_ar': 'كمبروسر المكيف'},
        {'category': 'engine', 'name_en': 'Turbocharger', 'name_ar': 'تيربو'},
        
        # ناقل الحركة
        {'category': 'transmission', 'name_en': 'Transmission Complete', 'name_ar': 'قير كامل'},
        {'category': 'transmission', 'name_en': 'Clutch Kit', 'name_ar': 'دبرياج كامل'},
        {'category': 'transmission', 'name_en': 'Flywheel', 'name_ar': 'فولان'},
        {'category': 'transmission', 'name_en': 'Drive Shaft', 'name_ar': 'عامود الدوران'},
        {'category': 'transmission', 'name_en': 'CV Axle', 'name_ar': 'عامود نصف'},
        
        # نظام التعليق والفرامل
        {'category': 'suspension', 'name_en': 'Front Shock Absorber', 'name_ar': 'مساعد أمامي'},
        {'category': 'suspension', 'name_en': 'Rear Shock Absorber', 'name_ar': 'مساعد خلفي'},
        {'category': 'suspension', 'name_en': 'Front Coil Spring', 'name_ar': 'سوست أمامي'},
        {'category': 'suspension', 'name_en': 'Rear Coil Spring', 'name_ar': 'سوست خلفي'},
        {'category': 'suspension', 'name_en': 'Control Arm', 'name_ar': 'مقص'},
        {'category': 'suspension', 'name_en': 'Ball Joint', 'name_ar': 'بلية'},
        {'category': 'suspension', 'name_en': 'Tie Rod End', 'name_ar': 'طرف عايق'},
        {'category': 'suspension', 'name_en': 'Sway Bar', 'name_ar': 'عامود تثبيت'},
        
        {'category': 'brakes', 'name_en': 'Brake Caliper Front', 'name_ar': 'كاليبر فرامل أمامي'},
        {'category': 'brakes', 'name_en': 'Brake Caliper Rear', 'name_ar': 'كاليبر فرامل خلفي'},
        {'category': 'brakes', 'name_en': 'Brake Disc Front', 'name_ar': 'ديسك فرامل أمامي'},
        {'category': 'brakes', 'name_en': 'Brake Disc Rear', 'name_ar': 'ديسك فرامل خلفي'},
        {'category': 'brakes', 'name_en': 'Brake Master Cylinder', 'name_ar': 'اسطوانة فرامل رئيسية'},
        {'category': 'brakes', 'name_en': 'ABS Pump', 'name_ar': 'طرمبة ABS'},
        
        # الإطارات والجنوط
        {'category': 'wheels', 'name_en': 'Alloy Wheel', 'name_ar': 'جنط ألمنيوم'},
        {'category': 'wheels', 'name_en': 'Steel Wheel', 'name_ar': 'جنط حديد'},
        {'category': 'wheels', 'name_en': 'Tire', 'name_ar': 'إطار'},
        {'category': 'wheels', 'name_en': 'Spare Tire', 'name_ar': 'إطار احتياطي'},
        
        # الهيكل والأبواب
        {'category': 'body', 'name_en': 'Front Bumper', 'name_ar': 'صدام أمامي'},
        {'category': 'body', 'name_en': 'Rear Bumper', 'name_ar': 'صدام خلفي'},
        {'category': 'body', 'name_en': 'Hood', 'name_ar': 'كبوت'},
        {'category': 'body', 'name_en': 'Front Door Right', 'name_ar': 'باب أمامي يمين'},
        {'category': 'body', 'name_en': 'Front Door Left', 'name_ar': 'باب أمامي يسار'},
        {'category': 'body', 'name_en': 'Rear Door Right', 'name_ar': 'باب خلفي يمين'},
        {'category': 'body', 'name_en': 'Rear Door Left', 'name_ar': 'باب خلفي يسار'},
        {'category': 'body', 'name_en': 'Trunk Lid', 'name_ar': 'شنطة'},
        {'category': 'body', 'name_en': 'Tailgate', 'name_ar': 'باب خلفي علوي'},
        {'category': 'body', 'name_en': 'Front Fender Right', 'name_ar': 'رفرف أمامي يمين'},
        {'category': 'body', 'name_en': 'Front Fender Left', 'name_ar': 'رفرف أمامي يسار'},
        {'category': 'body', 'name_en': 'Quarter Panel', 'name_ar': 'ربع سيارة'},
        {'category': 'body', 'name_en': 'Rocker Panel', 'name_ar': 'عتبة'},
        {'category': 'body', 'name_en': 'Roof', 'name_ar': 'سقف'},
        
        # الزجاج والمرايا
        {'category': 'glass', 'name_en': 'Windshield', 'name_ar': 'زجاج أمامي'},
        {'category': 'glass', 'name_en': 'Rear Windshield', 'name_ar': 'زجاج خلفي'},
        {'category': 'glass', 'name_en': 'Door Glass', 'name_ar': 'زجاج باب'},
        {'category': 'glass', 'name_en': 'Quarter Glass', 'name_ar': 'زجاج صغير'},
        {'category': 'glass', 'name_en': 'Side Mirror Right', 'name_ar': 'مرآة يمين'},
        {'category': 'glass', 'name_en': 'Side Mirror Left', 'name_ar': 'مرآة يسار'},
        {'category': 'glass', 'name_en': 'Sunroof', 'name_ar': 'فتحة سقف'},
        
        # الإضاءة
        {'category': 'lighting', 'name_en': 'Headlight Right', 'name_ar': 'فانوس أمامي يمين'},
        {'category': 'lighting', 'name_en': 'Headlight Left', 'name_ar': 'فانوس أمامي يسار'},
        {'category': 'lighting', 'name_en': 'Tail Light Right', 'name_ar': 'فانوس خلفي يمين'},
        {'category': 'lighting', 'name_en': 'Tail Light Left', 'name_ar': 'فانوس خلفي يسار'},
        {'category': 'lighting', 'name_en': 'Fog Light', 'name_ar': 'كشاف ضباب'},
        {'category': 'lighting', 'name_en': 'Turn Signal Light', 'name_ar': 'إشارة انعطاف'},
        
        # الداخلية
        {'category': 'interior', 'name_en': 'Dashboard', 'name_ar': 'تابلوه'},
        {'category': 'interior', 'name_en': 'Steering Wheel', 'name_ar': 'عجلة القيادة'},
        {'category': 'interior', 'name_en': 'Front Seat Right', 'name_ar': 'كرسي أمامي يمين'},
        {'category': 'interior', 'name_en': 'Front Seat Left', 'name_ar': 'كرسي أمامي يسار'},
        {'category': 'interior', 'name_en': 'Rear Seat', 'name_ar': 'كرسي خلفي'},
        {'category': 'interior', 'name_en': 'Seat Belt', 'name_ar': 'حزام أمان'},
        {'category': 'interior', 'name_en': 'Door Panel', 'name_ar': 'تابلوه باب'},
        {'category': 'interior', 'name_en': 'Carpet', 'name_ar': 'موكيت'},
        {'category': 'interior', 'name_en': 'Glove Box', 'name_ar': 'صندوق التابلوه'},
        {'category': 'interior', 'name_en': 'Console', 'name_ar': 'كونسول'},
        {'category': 'interior', 'name_en': 'Sun Visor', 'name_ar': 'حاجب شمس'},
        {'category': 'interior', 'name_en': 'Gear Shift', 'name_ar': 'ذراع الجير'},
        
        # الإلكترونيات
        {'category': 'electronics', 'name_en': 'ECU (Engine Control Unit)', 'name_ar': 'كمبيوتر المحرك'},
        {'category': 'electronics', 'name_en': 'ABS Module', 'name_ar': 'كمبيوتر ABS'},
        {'category': 'electronics', 'name_en': 'Airbag Module', 'name_ar': 'كمبيوتر الوسائد'},
        {'category': 'electronics', 'name_en': 'Instrument Cluster', 'name_ar': 'عداد'},
        {'category': 'electronics', 'name_en': 'Radio/Stereo', 'name_ar': 'راديو'},
        {'category': 'electronics', 'name_en': 'Navigation System', 'name_ar': 'شاشة ملاحة'},
        {'category': 'electronics', 'name_en': 'Climate Control', 'name_ar': 'كنترول مكيف'},
        {'category': 'electronics', 'name_en': 'Power Window Switch', 'name_ar': 'مفتاح الزجاج'},
        {'category': 'electronics', 'name_en': 'Central Lock Module', 'name_ar': 'كنترول الأقفال'},
        {'category': 'electronics', 'name_en': 'Wiper Motor', 'name_ar': 'موتور المساحات'},
        
        # البطارية والكهرباء
        {'category': 'electrical', 'name_en': 'Battery', 'name_ar': 'بطارية'},
        {'category': 'electrical', 'name_en': 'Fuse Box', 'name_ar': 'علبة الفيوزات'},
        {'category': 'electrical', 'name_en': 'Wiring Harness', 'name_ar': 'أسلاك كهربائية'},
        
        # متفرقات
        {'category': 'misc', 'name_en': 'Catalytic Converter', 'name_ar': 'شكمان حفاز'},
        {'category': 'misc', 'name_en': 'Exhaust Manifold', 'name_ar': 'منفولد'},
        {'category': 'misc', 'name_en': 'Muffler', 'name_ar': 'كاتم صوت'},
        {'category': 'misc', 'name_en': 'Fuel Tank', 'name_ar': 'تنك البنزين'},
        {'category': 'misc', 'name_en': 'Jack', 'name_ar': 'جاك'},
        {'category': 'misc', 'name_en': 'Tool Kit', 'name_ar': 'عدة'},
    ]
    
    @staticmethod
    def get_all_parts():
        """الحصول على جميع القطع القياسية"""
        return StandardParts.PARTS_LIST
    
    @staticmethod
    def get_parts_by_category(category):
        """الحصول على القطع حسب الفئة"""
        return [part for part in StandardParts.PARTS_LIST if part['category'] == category]
    
    @staticmethod
    def get_categories():
        """الحصول على جميع الفئات"""
        categories = set(part['category'] for part in StandardParts.PARTS_LIST)
        
        category_names = {
            'engine': 'المحرك',
            'transmission': 'ناقل الحركة',
            'suspension': 'نظام التعليق',
            'brakes': 'الفرامل',
            'wheels': 'الإطارات والجنوط',
            'body': 'الهيكل',
            'glass': 'الزجاج',
            'lighting': 'الإضاءة',
            'interior': 'الداخلية',
            'electronics': 'الإلكترونيات',
            'electrical': 'الكهرباء',
            'misc': 'متفرقات'
        }
        
        return [
            {'id': cat, 'name': category_names.get(cat, cat)}
            for cat in categories
        ]
