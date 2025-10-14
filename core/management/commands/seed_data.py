from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decimal import Decimal
from cars.models import CarMake, CarModel, PartCategory, Part, Vehicle
from customers.models import Customer
from inventory.models import WarehouseLocation, InventoryItem
from sales.models import Sale, SaleItem
from uuid import uuid4

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with demo data (idempotent)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # 0) Ensure superuser by username
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'is_superuser': True,
                'is_staff': True,
                'first_name': 'Admin',
                'last_name': 'User'
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Created superuser admin/admin123'))

        # 1) Makes/Models
        toyota, _ = CarMake.objects.get_or_create(name='Toyota', defaults={'name_ar': 'تويوتا', 'is_active': True})
        honda, _ = CarMake.objects.get_or_create(name='Honda', defaults={'name_ar': 'هوندا', 'is_active': True})
        nissan, _ = CarMake.objects.get_or_create(name='Nissan', defaults={'name_ar': 'نيسان', 'is_active': True})

        camry, _ = CarModel.objects.get_or_create(make=toyota, name='Camry', year_start=2015, defaults={'name_ar': 'كامري', 'body_type': 'Sedan'})
        corolla, _ = CarModel.objects.get_or_create(make=toyota, name='Corolla', year_start=2010, defaults={'name_ar': 'كورولا', 'body_type': 'Sedan'})
        accord, _ = CarModel.objects.get_or_create(make=honda, name='Accord', year_start=2013, defaults={'name_ar': 'أكورد', 'body_type': 'Sedan'})
        altima, _ = CarModel.objects.get_or_create(make=nissan, name='Altima', year_start=2012, defaults={'name_ar': 'التيما', 'body_type': 'Sedan'})

        # 2) Categories/Parts
        engine, _ = PartCategory.objects.get_or_create(name='Engine', defaults={'name_ar': 'المحرك', 'sort_order': 1})
        transmission, _ = PartCategory.objects.get_or_create(name='Transmission', defaults={'name_ar': 'ناقل الحركة', 'sort_order': 2})
        body, _ = PartCategory.objects.get_or_create(name='Body Parts', defaults={'name_ar': 'قطع الهيكل', 'sort_order': 3})
        electrical, _ = PartCategory.objects.get_or_create(name='Electrical', defaults={'name_ar': 'الكهرباء', 'sort_order': 4})
        cooling, _ = PartCategory.objects.get_or_create(name='Cooling System', defaults={'name_ar': 'نظام التبريد', 'parent': engine, 'sort_order': 1})
        exterior, _ = PartCategory.objects.get_or_create(name='Exterior', defaults={'name_ar': 'الخارجي', 'parent': body, 'sort_order': 1})

        radiator, _ = Part.objects.get_or_create(name='Radiator', category=cooling, defaults={'name_ar': 'الردياتير', 'part_number': 'RAD-001', 'description': 'Engine cooling radiator'})
        bumper, _ = Part.objects.get_or_create(name='Front Bumper', category=exterior, defaults={'name_ar': 'الصدام الأمامي', 'part_number': 'BUM-001', 'description': 'Front bumper assembly'})
        headlight, _ = Part.objects.get_or_create(name='Headlight', category=electrical, defaults={'name_ar': 'المصباح الأمامي', 'part_number': 'HL-001', 'description': 'Front headlight assembly'})
        alternator, _ = Part.objects.get_or_create(name='Alternator', category=electrical, defaults={'name_ar': 'الدينمو', 'part_number': 'ALT-001'})
        gearbox, _ = Part.objects.get_or_create(name='Gearbox', category=transmission, defaults={'name_ar': 'قير', 'part_number': 'GBX-001'})
        hood, _ = Part.objects.get_or_create(name='Hood', category=exterior, defaults={'name_ar': 'غطاء المحرك', 'part_number': 'HD-001'})

        # 3) Warehouse locations
        loc_a11, _ = WarehouseLocation.objects.get_or_create(warehouse='Main Warehouse', aisle='A', shelf='1', bin='1', defaults={'description': 'Main A-1-1'})
        loc_a12, _ = WarehouseLocation.objects.get_or_create(warehouse='Main Warehouse', aisle='A', shelf='1', bin='2', defaults={'description': 'Main A-1-2'})
        loc_b11, _ = WarehouseLocation.objects.get_or_create(warehouse='Main Warehouse', aisle='B', shelf='1', bin='1', defaults={'description': 'Main B-1-1'})

        # 4) Vehicles (6)
        def mk_vehicle(vin, make, model, year, color, condition):
            Vehicle.objects.get_or_create(
                vin=vin,
                defaults={
                    'make': make,
                    'model': model,
                    'year': year,
                    'color': color,
                    'mileage': 120000,
                    'condition': condition,
                    'received_by': admin,
                    'purchase_price': Decimal('12000.00'),
                    'intake_notes': 'Seeded vehicle'
                }
            )
        mk_vehicle('JTDBE30K123456789', toyota, camry, 2016, 'White', 'GOOD')
        mk_vehicle('2HGFB2F50CH123456', honda, accord, 2015, 'Black', 'FAIR')
        mk_vehicle('3N1AB7AP2GY123456', nissan, altima, 2017, 'Silver', 'GOOD')
        mk_vehicle('JTDBR32E330123456', toyota, corolla, 2014, 'Blue', 'FAIR')
        mk_vehicle('2HGCR2F59EA123456', honda, accord, 2014, 'Red', 'GOOD')
        mk_vehicle('1N4AL3AP0DN123456', nissan, altima, 2013, 'Gray', 'SALVAGE')

        # 5) Customers (6)
        def mk_customer(code_suffix, first, last, phone):
            return Customer.objects.get_or_create(
                phone=phone,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'email': f'{first.lower()}.{last.lower()}@example.com',
                    'address_line1': 'Riyadh',
                    'city': 'Riyadh',
                    'country': 'Saudi Arabia',
                    'created_by': admin,
                }
            )[0]
        c1 = mk_customer('01', 'Ahmed', 'Ali', '0500000001')
        c2 = mk_customer('02', 'Sara', 'Yousef', '0500000002')
        c3 = mk_customer('03', 'Omar', 'Hassan', '0500000003')
        c4 = mk_customer('04', 'Laila', 'Saleh', '0500000004')
        c5 = mk_customer('05', 'Noura', 'Khalid', '0500000005')
        c6 = mk_customer('06', 'Fahad', 'Abbas', '0500000006')

        # 6) Inventory Items (20+)
        parts = [radiator, bumper, headlight, alternator, gearbox, hood]
        locs = [loc_a11, loc_a12, loc_b11]
        vehicles = list(Vehicle.objects.all()[:3])
        created_items = 0
        for idx in range(1, 26):
            p = parts[idx % len(parts)]
            loc = locs[idx % len(locs)]
            veh = vehicles[idx % len(vehicles)]
            item, created_flag = InventoryItem.objects.get_or_create(
                part=p,
                vehicle_source=veh,
                selling_price=Decimal(str(200 + (idx * 10))),
                defaults={
                    'condition': 'USED_GOOD',
                    'status': 'AVAILABLE',
                    'quantity': 1 + (idx % 3),
                    'min_quantity': 1,
                    'location': loc,
                    'cost_price': Decimal('100.00'),
                    'notes': 'Seeded item',
                    'added_by': admin,
                }
            )
            if created_flag:
                created_items += 1
        self.stdout.write(self.style.SUCCESS(f'Inventory items ensured, new created: {created_items}'))

        # 7) Sales (4 invoices with items)
        customers = [c1, c2, c3, c4]
        items = list(InventoryItem.objects.all()[:10])
        def mk_sale(customer, items_slice):
            sale = Sale(customer=customer, sales_person=admin, status='DRAFT', payment_status='UNPAID', discount_amount=Decimal('0.00'), tax_amount=Decimal('0.00'))
            sale.invoice_number = f"INV-SEED-{uuid4().hex[:10]}"
            sale.save()  # assign PK before adding items
            for it in items_slice:
                SaleItem.objects.create(sale=sale, inventory_item=it, quantity=1, unit_price=it.selling_price)
            # finalize totals and mark as completed/paid
            sale.status = 'COMPLETED'
            sale.paid_amount = sale.total_amount
            sale.save()
            return sale
        if not Sale.objects.exists():
            mk_sale(customers[0], items[0:2])
            mk_sale(customers[1], items[2:5])
            mk_sale(customers[2], items[5:7])
            mk_sale(customers[3], items[7:10])
            self.stdout.write(self.style.SUCCESS('Created sample sales'))

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
        self.stdout.write(self.style.WARNING('Default superuser: admin / admin123'))
