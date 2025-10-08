"""
Simple demo data seeder with correct model fields only
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
import random

from cars.models import CarMake, CarModel, Part, Vehicle
from inventory.models import WarehouseLocation, InventoryItem
from customers.models import Customer
from sales.models import Sale, SaleItem, Payment

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed simple demo data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🌱 Starting simple demo data seeding...'))
        
        # Get admin user
        admin = User.objects.filter(email='admin@shparts.com').first()
        if not admin:
            self.stdout.write(self.style.ERROR('❌ Admin user not found. Run init_settings first.'))
            return
        
        # Get existing data
        makes = list(CarMake.objects.all())
        models = list(CarModel.objects.all())
        parts = list(Part.objects.all())
        locations = list(WarehouseLocation.objects.all())
        
        if not makes or not models or not parts:
            self.stdout.write(self.style.ERROR('❌ No car data found. Run import_cars_data first.'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'📊 Found: {len(makes)} makes, {len(models)} models, {len(parts)} parts'))
        
        # Create 5 Vehicles
        vehicles_created = 0
        for i in range(5):
            model_choice = random.choice(models)
            make = model_choice.make
            
            vin = f"VIN{random.randint(100000, 999999):06d}{i}"
            
            vehicle, created = Vehicle.objects.get_or_create(
                vin=vin,
                defaults={
                    'make': make,
                    'model': model_choice,
                    'year': random.randint(2015, 2023),
                    'color': random.choice(['أبيض', 'أسود', 'فضي', 'أحمر', 'أزرق']),
                    'mileage': random.randint(50000, 200000),
                    'condition': random.choice(['EXCELLENT', 'GOOD', 'FAIR']),
                    'purchase_price': Decimal(random.randint(30000, 80000)),
                    'received_by': admin,
                }
            )
            
            if created:
                vehicles_created += 1
                self.stdout.write(self.style.SUCCESS(f'✅ Vehicle: {vehicle.year} {vehicle.make.name} {vehicle.model.name}'))
        
        # Create inventory items
        vehicles = Vehicle.objects.all()[:5]
        inventory_created = 0
        
        if locations and vehicles:
            for vehicle in vehicles:
                # 3-5 parts per vehicle
                for _ in range(random.randint(3, 5)):
                    part = random.choice(parts)
                    
                    item, created = InventoryItem.objects.get_or_create(
                        part=part,
                        vehicle_source=vehicle,
                        condition=random.choice(['NEW', 'USED_EXCELLENT', 'USED_GOOD']),
                        defaults={
                            'location': random.choice(locations),
                            'quantity': random.randint(1, 3),
                            'selling_price': Decimal(random.randint(500, 8000)),
                            'cost_price': Decimal(random.randint(200, 5000)),
                            'added_by': admin,
                        }
                    )
                    
                    if created:
                        inventory_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'✅ Created {inventory_created} inventory items'))
        
        # Create 6 customers
        customers_created = 0
        for i in range(6):
            phone = f"010{random.randint(10000000, 99999999)}"
            
            customer, created = Customer.objects.get_or_create(
                phone=phone,
                defaults={
                    'customer_type': random.choice(['individual', 'company']),
                    'first_name': random.choice(['محمد', 'أحمد', 'علي', 'حسن', 'خالد']),
                    'last_name': random.choice(['أحمد', 'محمد', 'علي', 'حسن', 'إبراهيم']),
                    'email': f'customer{i}@example.com',
                    'city': random.choice(['القاهرة', 'الجيزة', 'الإسكندرية', 'طنطا']),
                    'created_by': admin,
                }
            )
            
            if created:
                customers_created += 1
                self.stdout.write(self.style.SUCCESS(f'✅ Customer: {customer.get_full_name()}'))
        
        # Create 5 sales
        customers = list(Customer.objects.all())
        inventory = list(InventoryItem.objects.filter(quantity__gt=0, status='AVAILABLE'))
        sales_created = 0
        
        if customers and inventory:
            for i in range(5):
                customer = random.choice(customers)
                
                try:
                    sale = Sale(
                        customer=customer,
                        sales_person=admin,
                        status=random.choice(['pending', 'completed', 'completed', 'completed']),
                        payment_status=random.choice(['unpaid', 'partial', 'paid', 'paid']),
                    )
                    # Save without calculating totals first
                    sale.subtotal = Decimal('0')
                    sale.tax_amount = Decimal('0')
                    sale.discount_amount = Decimal('0')
                    sale.total_amount = Decimal('0')
                    sale.save()
                    
                    # Add 1-3 items
                    for _ in range(random.randint(1, 3)):
                        if inventory:
                            item = random.choice(inventory)
                            
                            SaleItem.objects.create(
                                sale=sale,
                                inventory_item=item,
                                quantity=1,
                                unit_price=item.selling_price,
                                discount_percentage=Decimal('0')
                            )
                    
                    # Now recalculate
                    sale.save()
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'⚠️ Skipped sale creation: {e}'))
                    continue
                
                # Add payment if paid
                if sale.payment_status in ['paid', 'partial']:
                    payment_amount = sale.total_amount if sale.payment_status == 'paid' else sale.total_amount * Decimal('0.5')
                    
                    Payment.objects.create(
                        sale=sale,
                        amount=payment_amount,
                        payment_method=random.choice(['cash', 'bank_transfer', 'card']),
                        reference_number=f'PAY-{sale.invoice_number}',
                        received_by=admin
                    )
                
                sales_created += 1
                self.stdout.write(self.style.SUCCESS(f'✅ Sale: {sale.invoice_number} - {sale.total_amount} EGP'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('🎉 Demo Data Seeding Complete!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS(f'🚗 Vehicles: {Vehicle.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'📦 Inventory Items: {InventoryItem.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'👨‍💼 Customers: {Customer.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'💰 Sales: {Sale.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('='*60))
