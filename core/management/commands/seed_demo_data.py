"""
Command to seed comprehensive demo data for testing the entire system
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
import random

from cars.models import CarMake, CarModel, Part, Vehicle, VehiclePhoto
from inventory.models import WarehouseLocation, InventoryItem, StockMovement
from customers.models import Customer, CustomerCredit, CustomerNote
from sales.models import Sale, SaleItem, Payment

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed comprehensive demo data for system testing'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🌱 Starting demo data seeding...'))
        
        # Get or create admin user
        admin, created = User.objects.get_or_create(
            email='admin@shparts.com',
            defaults={
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
                'role': 'admin'
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'✅ Created admin user'))
        else:
            admin = User.objects.get(email='admin@shparts.com')
        
        # Create additional users
        sales_user, created_sales = User.objects.get_or_create(
            email='sales@shparts.com',
            defaults={
                'first_name': 'أحمد',
                'last_name': 'محمد',
                'role': 'sales',
                'phone': '01012345678',
                'is_staff': True
            }
        )
        if created_sales:
            sales_user.set_password('sales123')
            sales_user.save()
            self.stdout.write(self.style.SUCCESS(f'✅ Created sales user'))
        else:
            sales_user = User.objects.get(email='sales@shparts.com')
        
        warehouse_user, created_warehouse = User.objects.get_or_create(
            email='warehouse@shparts.com',
            defaults={
                'first_name': 'محمود',
                'last_name': 'علي',
                'role': 'warehouse',
                'phone': '01098765432',
                'is_staff': True
            }
        )
        if created_warehouse:
            warehouse_user.set_password('warehouse123')
            warehouse_user.save()
            self.stdout.write(self.style.SUCCESS(f'✅ Created warehouse user'))
        else:
            warehouse_user = User.objects.get(email='warehouse@shparts.com')
        
        # Get existing car data
        makes = CarMake.objects.all()
        models = CarModel.objects.all()
        parts = Part.objects.all()
        locations = WarehouseLocation.objects.all()
        
        if not makes.exists():
            self.stdout.write(self.style.ERROR('❌ No car makes found. Run import_cars_data first.'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'📊 Found: {makes.count()} makes, {models.count()} models, {parts.count()} parts'))
        
        # Create Vehicles (سيارات للتفكيك)
        vehicles_data = [
            {
                'vin': 'JT2BF18K9X0123456',
                'make': makes.filter(name='Toyota').first(),
                'model': models.filter(name='Camry').first(),
                'year': 2018,
                'color': 'أبيض',
                'mileage': 125000,
                'condition': 'fair',
                'purchase_price': Decimal('45000.00'),
                'purchase_date': timezone.now().date() - timedelta(days=45),
                'intake_date': timezone.now().date() - timedelta(days=45),
                'notes': 'سيارة حادث - محرك جيد، هيكل يحتاج عمل'
            },
            {
                'vin': 'JHMCF56H0XC456789',
                'make': makes.filter(name='Honda').first(),
                'model': models.filter(name='Accord').first(),
                'year': 2017,
                'color': 'أسود',
                'mileage': 98000,
                'condition': 'good',
                'purchase_price': Decimal('52000.00'),
                'purchase_date': timezone.now().date() - timedelta(days=30),
                'intake_date': timezone.now().date() - timedelta(days=30),
                'notes': 'حالة ممتازة - للتفكيك الكامل'
            },
            {
                'vin': '1N4AL11D5XC789012',
                'make': makes.filter(name='Nissan').first(),
                'model': models.filter(name='Altima').first(),
                'year': 2019,
                'color': 'فضي',
                'mileage': 75000,
                'condition': 'excellent',
                'purchase_price': Decimal('58000.00'),
                'purchase_date': timezone.now().date() - timedelta(days=15),
                'intake_date': timezone.now().date() - timedelta(days=15),
                'notes': 'سيارة نظيفة - قطع ممتازة'
            },
            {
                'vin': '5XXGN4A78FG123456',
                'make': makes.filter(name='Hyundai').first(),
                'model': models.filter(name='Elantra').first(),
                'year': 2016,
                'color': 'أحمر',
                'mileage': 145000,
                'condition': 'fair',
                'purchase_price': Decimal('38000.00'),
                'purchase_date': timezone.now().date() - timedelta(days=60),
                'intake_date': timezone.now().date() - timedelta(days=60),
                'notes': 'استخدام عالي - قطع ميكانيكا جيدة'
            },
            {
                'vin': 'KNAGM4A74B5234567',
                'make': makes.filter(name='Kia').first(),
                'model': models.filter(name='Cerato').first(),
                'year': 2020,
                'color': 'أزرق',
                'mileage': 45000,
                'condition': 'excellent',
                'purchase_price': Decimal('68000.00'),
                'purchase_date': timezone.now().date() - timedelta(days=10),
                'intake_date': timezone.now().date() - timedelta(days=10),
                'notes': 'سيارة حديثة - قطع أصلية'
            }
        ]
        
        created_vehicles = []
        for veh_data in vehicles_data:
            if veh_data['make'] and veh_data['model']:
                vehicle, created = Vehicle.objects.get_or_create(
                    vin=veh_data['vin'],
                    defaults={
                        'make': veh_data['make'],
                        'model': veh_data['model'],
                        'year': veh_data['year'],
                        'color': veh_data.get('color', ''),
                        'mileage': veh_data.get('mileage', 0),
                        'condition': veh_data.get('condition', 'FAIR').upper(),
                        'purchase_price': veh_data.get('purchase_price', Decimal('0')),
                        'received_by': admin,
                    }
                )
                if created:
                    created_vehicles.append(vehicle)
                    self.stdout.write(self.style.SUCCESS(f'✅ Created vehicle: {vehicle.make.name} {vehicle.model.name} {vehicle.year}'))
        
        # Create Inventory Items (قطع في المخزون)
        if not locations.exists():
            self.stdout.write(self.style.WARNING('⚠️ No warehouse locations found'))
        else:
            inventory_count = 0
            for vehicle in created_vehicles:
                # Select 5-8 random parts for each vehicle
                vehicle_parts = random.sample(list(parts), min(random.randint(5, 8), parts.count()))
                
                for part in vehicle_parts:
                    condition = random.choice(['new', 'excellent', 'good', 'fair'])
                    quantity = random.randint(1, 3)
                    
                    purchase_price = Decimal(random.randint(100, 5000))
                    selling_price = purchase_price * Decimal('1.4')  # 40% markup
                    
                    item, created = InventoryItem.objects.get_or_create(
                        part=part,
                        vehicle_source=vehicle,
                        condition=condition.upper(),
                        defaults={
                            'location': random.choice(locations),
                            'quantity': quantity,
                            'price': selling_price,
                        }
                    )
                    
                    if created:
                        inventory_count += 1
                        
                        # Create stock movement
                        StockMovement.objects.create(
                            inventory_item=item,
                            movement_type='in',
                            quantity=quantity,
                            reference_number=f'IN-{vehicle.vin[:8]}',
                            performed_by=warehouse_user
                        )
            
            self.stdout.write(self.style.SUCCESS(f'✅ Created {inventory_count} inventory items'))
        
        # Create Customers (عملاء)
        customers_data = [
            {
                'customer_type': 'individual',
                'first_name': 'محمد',
                'last_name': 'أحمد',
                'phone': '01012345678',
                'email': 'mohamed.ahmed@example.com',
                'address': 'شارع النيل، المعادي، القاهرة',
                'city': 'القاهرة',
                'id_number': '28901234567890'
            },
            {
                'customer_type': 'individual',
                'first_name': 'أحمد',
                'last_name': 'علي',
                'phone': '01098765432',
                'email': 'ahmed.ali@example.com',
                'address': 'شارع الهرم، الجيزة',
                'city': 'الجيزة',
                'id_number': '29012345678901'
            },
            {
                'customer_type': 'company',
                'company_name': 'ورشة النور للسيارات',
                'first_name': 'خالد',
                'last_name': 'حسن',
                'phone': '01123456789',
                'email': 'alnoor.workshop@example.com',
                'address': 'شارع الجيش، الإسكندرية',
                'city': 'الإسكندرية',
                'tax_number': 'TAX-123-456-789'
            },
            {
                'customer_type': 'company',
                'company_name': 'مركز الصفوة للصيانة',
                'first_name': 'عمر',
                'last_name': 'سالم',
                'phone': '01234567890',
                'email': 'alsafwa@example.com',
                'address': 'شارع المعمورة، الإسكندرية',
                'city': 'الإسكندرية',
                'tax_number': 'TAX-987-654-321'
            },
            {
                'customer_type': 'individual',
                'first_name': 'حسام',
                'last_name': 'فتحي',
                'phone': '01156789012',
                'email': 'hossam.fathy@example.com',
                'address': 'شارع الثورة، طنطا',
                'city': 'الغربية',
                'id_number': '28512345678902'
            },
            {
                'customer_type': 'company',
                'company_name': 'توكيل السلام للقطع',
                'first_name': 'ياسر',
                'last_name': 'محمود',
                'phone': '01187654321',
                'email': 'alsalam.parts@example.com',
                'address': 'شارع بورسعيد، المنصورة',
                'city': 'الدقهلية',
                'tax_number': 'TAX-555-666-777'
            }
        ]
        
        created_customers = []
        for cust_data in customers_data:
            customer, created = Customer.objects.get_or_create(
                phone=cust_data['phone'],
                defaults={
                    **cust_data,
                    'created_by': sales_user
                }
            )
            if created:
                created_customers.append(customer)
                self.stdout.write(self.style.SUCCESS(f'✅ Created customer: {customer.get_full_name()}'))
        
        # Create Sales (مبيعات)
        available_items = InventoryItem.objects.filter(quantity__gt=0)
        
        if available_items.exists() and created_customers:
            sales_count = 0
            
            for i in range(8):  # Create 8 sales
                customer = random.choice(created_customers)
                sale_items_count = random.randint(1, 4)
                
                # Create sale
                sale = Sale.objects.create(
                    customer=customer,
                    sales_person=sales_user,
                    status='completed' if i < 6 else 'pending',  # 6 completed, 2 pending
                    payment_status='paid' if i < 5 else ('partial' if i < 7 else 'unpaid'),
                )
                
                # Add items to sale
                sale_total = Decimal('0.00')
                for _ in range(sale_items_count):
                    item = random.choice(available_items)
                    quantity = 1
                    unit_price = item.selling_price
                    
                    SaleItem.objects.create(
                        sale=sale,
                        inventory_item=item,
                        quantity=quantity,
                        unit_price=unit_price,
                        discount_percentage=Decimal('0.00') if random.random() > 0.3 else Decimal('5.00')
                    )
                    
                    sale_total += unit_price * quantity
                
                # Recalculate sale totals
                sale.save()  # This triggers the auto-calculation
                
                # Create payment if paid or partial
                if sale.payment_status in ['paid', 'partial']:
                    payment_amount = sale.total_amount if sale.payment_status == 'paid' else sale.total_amount * Decimal('0.6')
                    
                    Payment.objects.create(
                        sale=sale,
                        amount=payment_amount,
                        payment_method='cash' if random.random() > 0.5 else 'bank_transfer',
                        reference_number=f'PAY-{sale.invoice_number}',
                        received_by=sales_user
                    )
                
                sales_count += 1
                self.stdout.write(self.style.SUCCESS(f'✅ Created sale: {sale.invoice_number} - {sale.total_amount} EGP'))
            
            self.stdout.write(self.style.SUCCESS(f'✅ Created {sales_count} sales'))
        
        # Create Customer Credits and Notes
        for customer in created_customers[:3]:  # First 3 customers
            # Add credit
            CustomerCredit.objects.get_or_create(
                customer=customer,
                defaults={
                    'amount': Decimal(random.randint(500, 5000)),
                    'credit_type': 'given',
                    'created_by': sales_user
                }
            )
            
            # Add note
            CustomerNote.objects.get_or_create(
                customer=customer,
                defaults={
                    'note': f'عميل ممتاز - يفضل التعامل النقدي',
                    'note_type': 'general',
                    'created_by': sales_user
                }
            )
        
        self.stdout.write(self.style.SUCCESS('✅ Created customer credits and notes'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('🎉 Demo Data Seeding Complete!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS(f'👥 Users: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'🚗 Vehicles: {Vehicle.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'📦 Inventory Items: {InventoryItem.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'👨‍💼 Customers: {Customer.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'💰 Sales: {Sale.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'💳 Payments: {Payment.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS('\n📝 Login Credentials:'))
        self.stdout.write(self.style.SUCCESS('   Admin: admin@shparts.com / admin123'))
        self.stdout.write(self.style.SUCCESS('   Sales: sales@shparts.com / sales123'))
        self.stdout.write(self.style.SUCCESS('   Warehouse: warehouse@shparts.com / warehouse123'))
        self.stdout.write(self.style.SUCCESS('='*60))
