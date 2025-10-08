"""
أمر إداري لاستيراد بيانات السيارات والقطع الشائعة في السوق السعودي
Data Import Command for Common Vehicles and Parts in Saudi Market
"""

from django.core.management.base import BaseCommand
from cars.models import CarMake, CarModel, PartCategory, Part
from django.db import transaction


class Command(BaseCommand):
    help = 'استيراد بيانات السيارات والقطع الشائعة / Import common vehicles and parts data'

    def handle(self, *args, **kwargs):
        self.stdout.write('بدء استيراد بيانات السيارات والقطع...')
        self.stdout.write('Starting vehicles and parts data import...\n')
        
        with transaction.atomic():
            # استيراد ماركات السيارات الرئيسية
            self.import_car_makes()
            
            # استيراد موديلات السيارات
            self.import_car_models()
            
            # استيراد فئات القطع
            self.import_part_categories()
            
            # استيراد القطع
            self.import_parts()
            
        self.stdout.write(self.style.SUCCESS('\n✓ تم الاستيراد بنجاح!'))
        self.stdout.write(self.style.SUCCESS('✓ Import completed successfully!'))

    def import_car_makes(self):
        """استيراد ماركات السيارات الشائعة"""
        self.stdout.write('استيراد ماركات السيارات...')
        
        makes_data = [
            {'name': 'Toyota', 'name_ar': 'تويوتا'},
            {'name': 'Honda', 'name_ar': 'هوندا'},
            {'name': 'Nissan', 'name_ar': 'نيسان'},
            {'name': 'Hyundai', 'name_ar': 'هيونداي'},
            {'name': 'Kia', 'name_ar': 'كيا'},
            {'name': 'Chevrolet', 'name_ar': 'شيفروليه'},
            {'name': 'Ford', 'name_ar': 'فورد'},
            {'name': 'GMC', 'name_ar': 'جي إم سي'},
        ]
        
        for make_data in makes_data:
            make, created = CarMake.objects.get_or_create(
                name=make_data['name'],
                defaults={'name_ar': make_data['name_ar'], 'is_active': True}
            )
            if created:
                self.stdout.write(f'  ✓ تم إضافة: {make.name} - {make.name_ar}')

    def import_car_models(self):
        """استيراد موديلات السيارات الشائعة"""
        self.stdout.write('\nاستيراد موديلات السيارات...')
        
        # Toyota Models
        toyota = CarMake.objects.get(name='Toyota')
        toyota_models = [
            {'name': 'Camry', 'name_ar': 'كامري', 'year_start': 2012, 'body_type': 'Sedan'},
            {'name': 'Corolla', 'name_ar': 'كورولا', 'year_start': 2010, 'body_type': 'Sedan'},
            {'name': 'Land Cruiser', 'name_ar': 'لاند كروزر', 'year_start': 2008, 'body_type': 'SUV'},
            {'name': 'RAV4', 'name_ar': 'راف فور', 'year_start': 2013, 'body_type': 'SUV'},
            {'name': 'Hilux', 'name_ar': 'هايلكس', 'year_start': 2015, 'body_type': 'Pickup'},
        ]
        
        for model_data in toyota_models:
            model, created = CarModel.objects.get_or_create(
                make=toyota,
                name=model_data['name'],
                year_start=model_data['year_start'],
                defaults={
                    'name_ar': model_data['name_ar'],
                    'body_type': model_data['body_type'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'  ✓ {toyota.name} {model.name} {model.year_start}+')
        
        # Honda Models
        honda = CarMake.objects.get(name='Honda')
        honda_models = [
            {'name': 'Accord', 'name_ar': 'أكورد', 'year_start': 2013, 'body_type': 'Sedan'},
            {'name': 'Civic', 'name_ar': 'سيفيك', 'year_start': 2012, 'body_type': 'Sedan'},
            {'name': 'CR-V', 'name_ar': 'سي آر في', 'year_start': 2014, 'body_type': 'SUV'},
            {'name': 'Pilot', 'name_ar': 'بايلوت', 'year_start': 2016, 'body_type': 'SUV'},
        ]
        
        for model_data in honda_models:
            model, created = CarModel.objects.get_or_create(
                make=honda,
                name=model_data['name'],
                year_start=model_data['year_start'],
                defaults={
                    'name_ar': model_data['name_ar'],
                    'body_type': model_data['body_type'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'  ✓ {honda.name} {model.name} {model.year_start}+')
        
        # Nissan Models
        nissan = CarMake.objects.get(name='Nissan')
        nissan_models = [
            {'name': 'Altima', 'name_ar': 'التيما', 'year_start': 2012, 'body_type': 'Sedan'},
            {'name': 'Maxima', 'name_ar': 'ماكسيما', 'year_start': 2016, 'body_type': 'Sedan'},
            {'name': 'Patrol', 'name_ar': 'باترول', 'year_start': 2010, 'body_type': 'SUV'},
            {'name': 'X-Trail', 'name_ar': 'اكس تريل', 'year_start': 2014, 'body_type': 'SUV'},
        ]
        
        for model_data in nissan_models:
            model, created = CarModel.objects.get_or_create(
                make=nissan,
                name=model_data['name'],
                year_start=model_data['year_start'],
                defaults={
                    'name_ar': model_data['name_ar'],
                    'body_type': model_data['body_type'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'  ✓ {nissan.name} {model.name} {model.year_start}+')

    def import_part_categories(self):
        """استيراد فئات القطع الرئيسية والفرعية"""
        self.stdout.write('\nاستيراد فئات القطع...')
        
        categories = [
            # المحرك والأنظمة الميكانيكية
            {
                'name': 'Engine System',
                'name_ar': 'نظام المحرك',
                'icon': 'bi-gear-fill',
                'sort_order': 1,
                'subcategories': [
                    {'name': 'Engine Block', 'name_ar': 'بلوك المحرك'},
                    {'name': 'Cylinder Head', 'name_ar': 'رأس المحرك'},
                    {'name': 'Pistons & Rings', 'name_ar': 'المكابس والشنابر'},
                    {'name': 'Crankshaft', 'name_ar': 'عمود الكرنك'},
                    {'name': 'Camshaft', 'name_ar': 'عمود الكامات'},
                    {'name': 'Timing Belt/Chain', 'name_ar': 'سير/سلسلة التوقيت'},
                    {'name': 'Engine Mounts', 'name_ar': 'قواعد المحرك'},
                ]
            },
            # نظام التبريد
            {
                'name': 'Cooling System',
                'name_ar': 'نظام التبريد',
                'icon': 'bi-thermometer-snow',
                'sort_order': 2,
                'subcategories': [
                    {'name': 'Radiator', 'name_ar': 'الرادياتير'},
                    {'name': 'Water Pump', 'name_ar': 'مضخة الماء'},
                    {'name': 'Thermostat', 'name_ar': 'الثرموستات'},
                    {'name': 'Cooling Fan', 'name_ar': 'مروحة التبريد'},
                    {'name': 'Radiator Hoses', 'name_ar': 'خراطيم الرادياتير'},
                    {'name': 'Expansion Tank', 'name_ar': 'خزان التمدد'},
                ]
            },
            # ناقل الحركة
            {
                'name': 'Transmission',
                'name_ar': 'ناقل الحركة',
                'icon': 'bi-gear-wide-connected',
                'sort_order': 3,
                'subcategories': [
                    {'name': 'Automatic Transmission', 'name_ar': 'قير أوتوماتيك'},
                    {'name': 'Manual Transmission', 'name_ar': 'قير عادي'},
                    {'name': 'CVT Transmission', 'name_ar': 'قير CVT'},
                    {'name': 'Clutch Kit', 'name_ar': 'طقم الكلتش'},
                    {'name': 'Transmission Mounts', 'name_ar': 'قواعد القير'},
                    {'name': 'Drive Shaft', 'name_ar': 'عمود الكردان'},
                ]
            },
            # نظام الوقود
            {
                'name': 'Fuel System',
                'name_ar': 'نظام الوقود',
                'icon': 'bi-droplet-fill',
                'sort_order': 4,
                'subcategories': [
                    {'name': 'Fuel Tank', 'name_ar': 'خزان الوقود'},
                    {'name': 'Fuel Pump', 'name_ar': 'مضخة الوقود'},
                    {'name': 'Fuel Injectors', 'name_ar': 'البخاخات'},
                    {'name': 'Fuel Filter', 'name_ar': 'فلتر الوقود'},
                    {'name': 'Fuel Lines', 'name_ar': 'خطوط الوقود'},
                ]
            },
            # النظام الكهربائي
            {
                'name': 'Electrical System',
                'name_ar': 'النظام الكهربائي',
                'icon': 'bi-lightning-charge-fill',
                'sort_order': 5,
                'subcategories': [
                    {'name': 'Battery', 'name_ar': 'البطارية'},
                    {'name': 'Alternator', 'name_ar': 'الدينامو'},
                    {'name': 'Starter Motor', 'name_ar': 'السلف'},
                    {'name': 'Ignition Coils', 'name_ar': 'كويلات الإشعال'},
                    {'name': 'Spark Plugs', 'name_ar': 'البواجي'},
                    {'name': 'Wiring Harness', 'name_ar': 'حزمة الأسلاك'},
                    {'name': 'Fuse Box', 'name_ar': 'علبة الفيوزات'},
                ]
            },
            # الإضاءة
            {
                'name': 'Lighting',
                'name_ar': 'الإضاءة',
                'icon': 'bi-lightbulb-fill',
                'sort_order': 6,
                'subcategories': [
                    {'name': 'Headlights', 'name_ar': 'الأنوار الأمامية'},
                    {'name': 'Tail Lights', 'name_ar': 'الأنوار الخلفية'},
                    {'name': 'Fog Lights', 'name_ar': 'أنوار الضباب'},
                    {'name': 'Turn Signal Lights', 'name_ar': 'الغمازات'},
                    {'name': 'Interior Lights', 'name_ar': 'الأنوار الداخلية'},
                ]
            },
            # قطع الهيكل الخارجي
            {
                'name': 'Body Exterior',
                'name_ar': 'الهيكل الخارجي',
                'icon': 'bi-car-front-fill',
                'sort_order': 7,
                'subcategories': [
                    {'name': 'Front Bumper', 'name_ar': 'الصدام الأمامي'},
                    {'name': 'Rear Bumper', 'name_ar': 'الصدام الخلفي'},
                    {'name': 'Hood', 'name_ar': 'الكبوت'},
                    {'name': 'Front Fenders', 'name_ar': 'الرفارف الأمامية'},
                    {'name': 'Rear Fenders', 'name_ar': 'الرفارف الخلفية'},
                    {'name': 'Doors', 'name_ar': 'الأبواب'},
                    {'name': 'Trunk Lid', 'name_ar': 'غطاء الصندوق'},
                    {'name': 'Roof', 'name_ar': 'السقف'},
                    {'name': 'Side Mirrors', 'name_ar': 'المرايا الجانبية'},
                    {'name': 'Grille', 'name_ar': 'الشبك الأمامي'},
                ]
            },
            # الزجاج
            {
                'name': 'Glass',
                'name_ar': 'الزجاج',
                'icon': 'bi-square',
                'sort_order': 8,
                'subcategories': [
                    {'name': 'Windshield', 'name_ar': 'الزجاج الأمامي'},
                    {'name': 'Rear Window', 'name_ar': 'الزجاج الخلفي'},
                    {'name': 'Door Windows', 'name_ar': 'زجاج الأبواب'},
                    {'name': 'Quarter Windows', 'name_ar': 'زجاج الربع'},
                ]
            },
            # المقصورة الداخلية
            {
                'name': 'Interior',
                'name_ar': 'المقصورة الداخلية',
                'icon': 'bi-house-door-fill',
                'sort_order': 9,
                'subcategories': [
                    {'name': 'Dashboard', 'name_ar': 'التابلوه'},
                    {'name': 'Steering Wheel', 'name_ar': 'المقود'},
                    {'name': 'Front Seats', 'name_ar': 'المقاعد الأمامية'},
                    {'name': 'Rear Seats', 'name_ar': 'المقاعد الخلفية'},
                    {'name': 'Door Panels', 'name_ar': 'تجليد الأبواب'},
                    {'name': 'Center Console', 'name_ar': 'الكونسول الوسطي'},
                    {'name': 'Carpets', 'name_ar': 'الفرش'},
                    {'name': 'Headliner', 'name_ar': 'سقف المقصورة'},
                    {'name': 'Sun Visors', 'name_ar': 'حاجبات الشمس'},
                ]
            },
            # نظام التعليق
            {
                'name': 'Suspension',
                'name_ar': 'نظام التعليق',
                'icon': 'bi-arrows-vertical',
                'sort_order': 10,
                'subcategories': [
                    {'name': 'Shock Absorbers', 'name_ar': 'المساعدات'},
                    {'name': 'Coil Springs', 'name_ar': 'السوست'},
                    {'name': 'Control Arms', 'name_ar': 'أذرع التعليق'},
                    {'name': 'Ball Joints', 'name_ar': 'البلي المقصات'},
                    {'name': 'Stabilizer Bar', 'name_ar': 'المطارة'},
                    {'name': 'Steering Rack', 'name_ar': 'علبة الدركسون'},
                ]
            },
            # نظام الفرامل
            {
                'name': 'Brakes',
                'name_ar': 'نظام الفرامل',
                'icon': 'bi-disc-fill',
                'sort_order': 11,
                'subcategories': [
                    {'name': 'Brake Pads', 'name_ar': 'تيل الفرامل'},
                    {'name': 'Brake Discs', 'name_ar': 'أقراص الفرامل'},
                    {'name': 'Brake Drums', 'name_ar': 'طبول الفرامل'},
                    {'name': 'Brake Calipers', 'name_ar': 'سلندرات الفرامل'},
                    {'name': 'Master Cylinder', 'name_ar': 'سلندر الفرامل الرئيسي'},
                    {'name': 'ABS Module', 'name_ar': 'وحدة ABS'},
                ]
            },
            # الإطارات والجنوط
            {
                'name': 'Wheels & Tires',
                'name_ar': 'الإطارات والجنوط',
                'icon': 'bi-circle',
                'sort_order': 12,
                'subcategories': [
                    {'name': 'Alloy Wheels', 'name_ar': 'جنوط ألمنيوم'},
                    {'name': 'Steel Wheels', 'name_ar': 'جنوط حديد'},
                    {'name': 'Tires', 'name_ar': 'الإطارات'},
                    {'name': 'Hub Caps', 'name_ar': 'أغطية الجنوط'},
                ]
            },
            # نظام التكييف
            {
                'name': 'AC System',
                'name_ar': 'نظام التكييف',
                'icon': 'bi-wind',
                'sort_order': 13,
                'subcategories': [
                    {'name': 'AC Compressor', 'name_ar': 'كمبروسر التكييف'},
                    {'name': 'Condenser', 'name_ar': 'المكثف'},
                    {'name': 'Evaporator', 'name_ar': 'المبخر'},
                    {'name': 'Blower Motor', 'name_ar': 'مروحة التكييف'},
                    {'name': 'AC Controls', 'name_ar': 'أزرار التحكم'},
                ]
            },
            # نظام العادم
            {
                'name': 'Exhaust System',
                'name_ar': 'نظام العادم',
                'icon': 'bi-cloud-fill',
                'sort_order': 14,
                'subcategories': [
                    {'name': 'Exhaust Manifold', 'name_ar': 'مانيفولد العادم'},
                    {'name': 'Catalytic Converter', 'name_ar': 'الكتلايزر'},
                    {'name': 'Muffler', 'name_ar': 'الجنزير'},
                    {'name': 'Exhaust Pipes', 'name_ar': 'مواسير العادم'},
                ]
            },
            # الوسائط المتعددة
            {
                'name': 'Multimedia',
                'name_ar': 'الوسائط المتعددة',
                'icon': 'bi-music-note-beamed',
                'sort_order': 15,
                'subcategories': [
                    {'name': 'Infotainment System', 'name_ar': 'شاشة المعلومات'},
                    {'name': 'Radio/CD Player', 'name_ar': 'الراديو/المشغل'},
                    {'name': 'Speakers', 'name_ar': 'السماعات'},
                    {'name': 'Amplifier', 'name_ar': 'مكبر الصوت'},
                    {'name': 'GPS Navigation', 'name_ar': 'نظام الملاحة'},
                ]
            },
        ]
        
        for category_data in categories:
            # إنشاء الفئة الرئيسية
            category, created = PartCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'name_ar': category_data['name_ar'],
                    'icon': category_data.get('icon', ''),
                    'sort_order': category_data['sort_order'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f'  ✓ {category.name} - {category.name_ar}')
            
            # إنشاء الفئات الفرعية
            if 'subcategories' in category_data:
                for sub_data in category_data['subcategories']:
                    sub_category, sub_created = PartCategory.objects.get_or_create(
                        name=sub_data['name'],
                        parent=category,
                        defaults={
                            'name_ar': sub_data['name_ar'],
                            'is_active': True
                        }
                    )
                    if sub_created:
                        self.stdout.write(f'    • {sub_category.name} - {sub_category.name_ar}')

    def import_parts(self):
        """استيراد القطع الشائعة"""
        self.stdout.write('\nاستيراد القطع الشائعة...')
        
        # الحصول على الموديلات الثلاثة الرئيسية
        toyota_camry = CarModel.objects.filter(make__name='Toyota', name='Camry').first()
        honda_accord = CarModel.objects.filter(make__name='Honda', name='Accord').first()
        nissan_altima = CarModel.objects.filter(make__name='Nissan', name='Altima').first()
        
        if not all([toyota_camry, honda_accord, nissan_altima]):
            self.stdout.write(self.style.WARNING('لم يتم العثور على جميع الموديلات الرئيسية'))
            return
        
        # قائمة القطع حسب الفئة
        parts_by_category = {
            'Engine Block': [
                {'name': 'Complete Engine Block 2.5L', 'name_ar': 'بلوك محرك كامل 2.5 لتر', 'part_number': 'ENG-2.5L-001'},
                {'name': 'Complete Engine Block 3.5L', 'name_ar': 'بلوك محرك كامل 3.5 لتر', 'part_number': 'ENG-3.5L-001'},
            ],
            'Radiator': [
                {'name': 'Engine Radiator', 'name_ar': 'رادياتير المحرك', 'part_number': 'RAD-001'},
                {'name': 'AC Condenser', 'name_ar': 'رادياتير التكييف', 'part_number': 'RAD-002'},
            ],
            'Water Pump': [
                {'name': 'Engine Water Pump', 'name_ar': 'مضخة ماء المحرك', 'part_number': 'WP-001'},
            ],
            'Automatic Transmission': [
                {'name': 'Automatic Transmission Complete', 'name_ar': 'قير أوتوماتيك كامل', 'part_number': 'ATX-001'},
            ],
            'Headlights': [
                {'name': 'Front Right Headlight', 'name_ar': 'كشاف أمامي يمين', 'part_number': 'HL-R-001'},
                {'name': 'Front Left Headlight', 'name_ar': 'كشاف أمامي يسار', 'part_number': 'HL-L-001'},
            ],
            'Tail Lights': [
                {'name': 'Rear Right Tail Light', 'name_ar': 'ستوب خلفي يمين', 'part_number': 'TL-R-001'},
                {'name': 'Rear Left Tail Light', 'name_ar': 'ستوب خلفي يسار', 'part_number': 'TL-L-001'},
            ],
            'Front Bumper': [
                {'name': 'Front Bumper Complete', 'name_ar': 'صدام أمامي كامل', 'part_number': 'FBP-001'},
            ],
            'Rear Bumper': [
                {'name': 'Rear Bumper Complete', 'name_ar': 'صدام خلفي كامل', 'part_number': 'RBP-001'},
            ],
            'Hood': [
                {'name': 'Engine Hood', 'name_ar': 'كبوت المحرك', 'part_number': 'HOOD-001'},
            ],
            'Doors': [
                {'name': 'Front Right Door', 'name_ar': 'باب أمامي يمين', 'part_number': 'DOOR-FR-001'},
                {'name': 'Front Left Door', 'name_ar': 'باب أمامي يسار', 'part_number': 'DOOR-FL-001'},
                {'name': 'Rear Right Door', 'name_ar': 'باب خلفي يمين', 'part_number': 'DOOR-RR-001'},
                {'name': 'Rear Left Door', 'name_ar': 'باب خلفي يسار', 'part_number': 'DOOR-RL-001'},
            ],
            'Side Mirrors': [
                {'name': 'Right Side Mirror', 'name_ar': 'مرآة جانبية يمين', 'part_number': 'MIR-R-001'},
                {'name': 'Left Side Mirror', 'name_ar': 'مرآة جانبية يسار', 'part_number': 'MIR-L-001'},
            ],
            'Windshield': [
                {'name': 'Front Windshield Glass', 'name_ar': 'زجاج أمامي', 'part_number': 'WS-001'},
            ],
            'Dashboard': [
                {'name': 'Complete Dashboard', 'name_ar': 'تابلوه كامل', 'part_number': 'DASH-001'},
            ],
            'Front Seats': [
                {'name': 'Driver Seat', 'name_ar': 'مقعد السائق', 'part_number': 'SEAT-DR-001'},
                {'name': 'Passenger Seat', 'name_ar': 'مقعد الراكب', 'part_number': 'SEAT-PA-001'},
            ],
            'Shock Absorbers': [
                {'name': 'Front Right Shock Absorber', 'name_ar': 'مساعد أمامي يمين', 'part_number': 'SHOCK-FR-001'},
                {'name': 'Front Left Shock Absorber', 'name_ar': 'مساعد أمامي يسار', 'part_number': 'SHOCK-FL-001'},
                {'name': 'Rear Right Shock Absorber', 'name_ar': 'مساعد خلفي يمين', 'part_number': 'SHOCK-RR-001'},
                {'name': 'Rear Left Shock Absorber', 'name_ar': 'مساعد خلفي يسار', 'part_number': 'SHOCK-RL-001'},
            ],
            'Brake Discs': [
                {'name': 'Front Brake Disc Pair', 'name_ar': 'أقراص فرامل أمامية (زوج)', 'part_number': 'DISC-F-001'},
                {'name': 'Rear Brake Disc Pair', 'name_ar': 'أقراص فرامل خلفية (زوج)', 'part_number': 'DISC-R-001'},
            ],
            'Alloy Wheels': [
                {'name': '17" Alloy Wheel', 'name_ar': 'جنط ألمنيوم 17 إنش', 'part_number': 'WHEEL-17-001'},
                {'name': '18" Alloy Wheel', 'name_ar': 'جنط ألمنيوم 18 إنش', 'part_number': 'WHEEL-18-001'},
            ],
            'AC Compressor': [
                {'name': 'AC Compressor', 'name_ar': 'كمبروسر التكييف', 'part_number': 'AC-COMP-001'},
            ],
        }
        
        compatible_models = [toyota_camry, honda_accord, nissan_altima]
        
        for category_name, parts_list in parts_by_category.items():
            category = PartCategory.objects.filter(name=category_name).first()
            if not category:
                continue
            
            for part_data in parts_list:
                part, created = Part.objects.get_or_create(
                    name=part_data['name'],
                    category=category,
                    defaults={
                        'name_ar': part_data['name_ar'],
                        'part_number': part_data['part_number'],
                        'description': f"Original quality part for {', '.join([m.make.name + ' ' + m.name for m in compatible_models])}",
                        'description_ar': f"قطعة أصلية لـ {', '.join([m.make.name_ar + ' ' + m.name_ar for m in compatible_models])}",
                        'is_universal': False,
                        'is_active': True
                    }
                )
                
                if created:
                    # ربط القطعة بالموديلات المتوافقة
                    part.compatible_models.set(compatible_models)
                    self.stdout.write(f'  ✓ {part.name} - {part.name_ar}')
        
        self.stdout.write(f'\nإجمالي القطع المضافة: {Part.objects.count()}')
