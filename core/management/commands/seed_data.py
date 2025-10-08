from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from cars.models import CarMake, CarModel, PartCategory, Part
from inventory.models import WarehouseLocation

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        
        # Create users if they don't exist
        if not User.objects.filter(email='admin@shparts.com').exists():
            User.objects.create_superuser(
                email='admin@shparts.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                role='ADMIN'
            )
            self.stdout.write(self.style.SUCCESS('Created admin user'))
        
        # Create car makes
        toyota = CarMake.objects.get_or_create(
            name='Toyota',
            defaults={'name_ar': 'تويوتا', 'is_active': True}
        )[0]
        
        honda = CarMake.objects.get_or_create(
            name='Honda',
            defaults={'name_ar': 'هوندا', 'is_active': True}
        )[0]
        
        nissan = CarMake.objects.get_or_create(
            name='Nissan',
            defaults={'name_ar': 'نيسان', 'is_active': True}
        )[0]
        
        self.stdout.write(self.style.SUCCESS('Created car makes'))
        
        # Create car models
        CarModel.objects.get_or_create(
            make=toyota,
            name='Camry',
            year_start=2015,
            defaults={'name_ar': 'كامري', 'body_type': 'Sedan'}
        )
        
        CarModel.objects.get_or_create(
            make=toyota,
            name='Corolla',
            year_start=2010,
            defaults={'name_ar': 'كورولا', 'body_type': 'Sedan'}
        )
        
        CarModel.objects.get_or_create(
            make=honda,
            name='Accord',
            year_start=2013,
            defaults={'name_ar': 'أكورد', 'body_type': 'Sedan'}
        )
        
        CarModel.objects.get_or_create(
            make=nissan,
            name='Altima',
            year_start=2012,
            defaults={'name_ar': 'التيما', 'body_type': 'Sedan'}
        )
        
        self.stdout.write(self.style.SUCCESS('Created car models'))
        
        # Create part categories
        engine_cat = PartCategory.objects.get_or_create(
            name='Engine',
            defaults={'name_ar': 'المحرك', 'sort_order': 1}
        )[0]
        
        transmission_cat = PartCategory.objects.get_or_create(
            name='Transmission',
            defaults={'name_ar': 'ناقل الحركة', 'sort_order': 2}
        )[0]
        
        body_cat = PartCategory.objects.get_or_create(
            name='Body Parts',
            defaults={'name_ar': 'قطع الهيكل', 'sort_order': 3}
        )[0]
        
        electrical_cat = PartCategory.objects.get_or_create(
            name='Electrical',
            defaults={'name_ar': 'الكهرباء', 'sort_order': 4}
        )[0]
        
        self.stdout.write(self.style.SUCCESS('Created part categories'))
        
        # Create subcategories
        engine_cooling = PartCategory.objects.get_or_create(
            name='Cooling System',
            defaults={'name_ar': 'نظام التبريد', 'parent': engine_cat, 'sort_order': 1}
        )[0]
        
        body_exterior = PartCategory.objects.get_or_create(
            name='Exterior',
            defaults={'name_ar': 'الخارجي', 'parent': body_cat, 'sort_order': 1}
        )[0]
        
        # Create sample parts
        Part.objects.get_or_create(
            name='Radiator',
            category=engine_cooling,
            defaults={
                'name_ar': 'الردياتير',
                'part_number': 'RAD-001',
                'description': 'Engine cooling radiator',
                'is_universal': False
            }
        )
        
        Part.objects.get_or_create(
            name='Front Bumper',
            category=body_exterior,
            defaults={
                'name_ar': 'الصدام الأمامي',
                'part_number': 'BUM-001',
                'description': 'Front bumper assembly',
                'is_universal': False
            }
        )
        
        Part.objects.get_or_create(
            name='Headlight',
            category=electrical_cat,
            defaults={
                'name_ar': 'المصباح الأمامي',
                'part_number': 'HL-001',
                'description': 'Front headlight assembly',
                'is_universal': False
            }
        )
        
        self.stdout.write(self.style.SUCCESS('Created sample parts'))
        
        # Create warehouse locations
        WarehouseLocation.objects.get_or_create(
            warehouse='Main Warehouse',
            aisle='A',
            shelf='1',
            bin='1',
            defaults={'description': 'Main warehouse location A-1-1'}
        )
        
        WarehouseLocation.objects.get_or_create(
            warehouse='Main Warehouse',
            aisle='A',
            shelf='1',
            bin='2',
            defaults={'description': 'Main warehouse location A-1-2'}
        )
        
        WarehouseLocation.objects.get_or_create(
            warehouse='Main Warehouse',
            aisle='B',
            shelf='1',
            bin='1',
            defaults={'description': 'Main warehouse location B-1-1'}
        )
        
        self.stdout.write(self.style.SUCCESS('Created warehouse locations'))
        
        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
        self.stdout.write(self.style.WARNING('Default admin credentials: admin@shparts.com / admin123'))
