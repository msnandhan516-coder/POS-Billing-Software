from decimal import Decimal
import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User
from billing.models import Sale, SaleItem
from ledger.models import LedgerEntry
from products.models import Category, Product
from suppliers.models import Supplier


class Command(BaseCommand):
    help = 'Seeds realistic commercial demo data for the POS application.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding commercial POS demo data...')

        # 1. Staff and Admin accounts
        admin_user, _ = User.objects.get_or_create(
            username='Nandhan',
            defaults={
                'email': 'nandhan@retailpos.com',
                'first_name': 'Nandhan',
                'last_name': 'K',
                'role': User.Role.ADMIN,
                'phone_number': '+91 98765 00001',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            }
        )
        admin_user.role = User.Role.ADMIN
        admin_user.set_password('admin123')
        admin_user.save()

        staff_list_data = [
            ('bins_7', 'Bins', 'Mathew', 'bins@retailpos.com', '+91 98765 00002'),
            ('Akhil', 'Akhil', 'Raj', 'akhil@retailpos.com', '+91 98765 00003'),
            ('Syamjith', 'Syamjith', 'S', 'syamjith@retailpos.com', '+91 98765 00004'),
            ('Susmitha', 'Susmitha', 'P', 'susmitha@retailpos.com', '+91 98765 00005'),
        ]

        created_staff = []
        for uname, fname, lname, email, phone in staff_list_data:
            st, _ = User.objects.get_or_create(
                username=uname,
                defaults={
                    'email': email,
                    'first_name': fname,
                    'last_name': lname,
                    'role': User.Role.STAFF,
                    'phone_number': phone,
                    'is_staff': False,
                    'is_active': True,
                }
            )
            st.role = User.Role.STAFF
            st.set_password('staff123')
            st.save()
            created_staff.append(st)

        # 2. Suppliers
        suppliers_data = [
            ('Apex Tech Distributors', 'Vikram Patel', 'vikram@apextech.com', '+91 98450 11223', 'Electronic City, Bengaluru', 'Karnataka', '29AABCA1234F1Z5'),
            ('Prime Logistics & Hardware', 'Deepa Nair', 'deepa@primelogistics.com', '+91 97420 55667', 'Kakkanad, Kochi', 'Kerala', '32AACCP9988G1ZQ'),
            ('Global Gadgets Wholesale', 'Amitabh Sen', 'amitabh@globalgadgets.com', '+91 98110 33445', 'Nehru Place, New Delhi', 'Delhi', '07AABCG5544H1ZS'),
        ]
        created_suppliers = []
        for cname, contact, email, phone, addr, state, gst in suppliers_data:
            sup, _ = Supplier.objects.get_or_create(
                company_name=cname,
                defaults={
                    'contact_person': contact,
                    'email': email,
                    'phone': phone,
                    'address': addr,
                    'city': addr.split(',')[0].strip(),
                    'state': state,
                    'gst_number': gst,
                    'is_active': True,
                }
            )
            created_suppliers.append(sup)

        # 3. Categories
        categories_data = [
            ('Smartphones', 'Latest premium 5G and mid-range mobile devices'),
            ('Laptops', 'Ultrabooks, business notebooks and workstation laptops'),
            ('Audio', 'Noise-cancelling headphones, wireless earphones and Bluetooth speakers'),
            ('Accessories', 'Power banks, fast chargers, cables and protective cases'),
            ('Peripherals', 'Keyboards, wireless mice, webcams and external monitors'),
            ('Networking', 'Wi-Fi 6 mesh routers, network switches and adapters'),
        ]
        cat_map = {}
        for cname, cdesc in categories_data:
            cat, _ = Category.objects.get_or_create(
                name=cname,
                defaults={'description': cdesc, 'is_active': True}
            )
            cat_map[cname] = cat

        # 4. Products Catalog
        products_data = [
            # Smartphones
            ('Realme 12 Pro', 'RM12-PRO-256', '8901234567891', 'Smartphones', 0, 16999.00, 19999.00, 18.0, 18, 5),
            ('Redmi Note 13', 'RN13-128-BLK', '8901234567892', 'Smartphones', 0, 12499.00, 14499.00, 18.0, 2, 5),  # Low stock
            ('Samsung Galaxy S24', 'SAM-S24-256', '8901234567893', 'Smartphones', 0, 64999.00, 74999.00, 18.0, 8, 4),
            ('iPhone 15 Pro', 'IP15P-128-BLU', '8901234567894', 'Smartphones', 0, 108000.00, 124900.00, 18.0, 12, 3),
            ('OnePlus 12', 'OP12-256-GRN', '8901234567895', 'Smartphones', 0, 56999.00, 64999.00, 18.0, 15, 4),
            ('Google Pixel 8', 'PIX8-128-OBS', '8901234567896', 'Smartphones', 0, 59999.00, 69999.00, 18.0, 3, 5),   # Low stock

            # Laptops
            ('Dell Inspiron 15', 'DELL-INSP-15', '8901234567897', 'Laptops', 1, 46990.00, 54990.00, 18.0, 7, 3),
            ('HP Pavilion 14', 'HP-PAV-14-SIL', '8901234567898', 'Laptops', 1, 50499.00, 58499.00, 18.0, 10, 4),
            ('Lenovo IdeaPad Slim 3', 'LEN-IP3-SLIM', '8901234567899', 'Laptops', 1, 36990.00, 42990.00, 18.0, 2, 5), # Low stock
            ('Apple MacBook Air M2', 'MBA-M2-256', '8901234567900', 'Laptops', 1, 82900.00, 94900.00, 18.0, 9, 3),
            ('ASUS Vivobook 16', 'ASUS-VIVO-16', '8901234567901', 'Laptops', 1, 54990.00, 62990.00, 18.0, 6, 3),

            # Audio
            ('Sony WH-1000XM5', 'SONY-XM5-BLK', '8901234567902', 'Audio', 2, 23990.00, 28990.00, 18.0, 14, 4),
            ('JBL Flip 6 Speaker', 'JBL-FLIP6-BLU', '8901234567903', 'Audio', 2, 7999.00, 9999.00, 18.0, 22, 5),
            ('Apple AirPods Pro 2', 'APP-GEN2-USBC', '8901234567904', 'Audio', 2, 19499.00, 22900.00, 18.0, 16, 4),
            ('Boat Rockerz 450', 'BOAT-RCK-450', '8901234567905', 'Audio', 2, 999.00, 1499.00, 18.0, 35, 10),
            ('Bose QuietComfort 45', 'BOSE-QC45-BLK', '8901234567906', 'Audio', 2, 19900.00, 24900.00, 18.0, 4, 5), # Low stock

            # Accessories
            ('Anker PowerBank 20000mAh', 'ANK-PB-20K', '8901234567907', 'Accessories', 2, 2499.00, 3499.00, 18.0, 28, 6),
            ('Braided USB-C Fast Cable', 'CAB-USBC-60W', '8901234567908', 'Accessories', 2, 249.00, 499.00, 18.0, 45, 10),
            ('65W GaN Fast Charger', 'CHG-65W-GAN', '8901234567909', 'Accessories', 2, 1399.00, 1999.00, 18.0, 20, 5),
            ('Spigen Tough Armor Case', 'SPG-ARMOR-GEN', '8901234567910', 'Accessories', 2, 499.00, 899.00, 18.0, 40, 8),

            # Peripherals
            ('Logitech MX Master 3S', 'LOGI-MX3S-GRY', '8901234567911', 'Peripherals', 1, 6995.00, 8495.00, 18.0, 11, 4),
            ('Keychron K2 RGB Keyboard', 'KEY-K2-RGB', '8901234567912', 'Peripherals', 1, 6499.00, 7999.00, 18.0, 8, 3),
            ('Dell 24-inch IPS Monitor', 'DELL-MON-24', '8901234567913', 'Peripherals', 1, 9490.00, 11490.00, 18.0, 12, 4),
            ('Logitech C920 Pro Webcam', 'LOGI-C920-PRO', '8901234567914', 'Peripherals', 1, 4995.00, 6495.00, 18.0, 18, 5),

            # Networking
            ('TP-Link AX73 Wi-Fi 6', 'TPL-AX73-W6', '8901234567915', 'Networking', 0, 5499.00, 6999.00, 18.0, 15, 4),
            ('Netgear Nighthawk Router', 'NET-NIGHT-XR5', '8901234567916', 'Networking', 0, 11999.00, 14999.00, 18.0, 3, 5), # Low stock
        ]

        created_products = []
        for name, sku, barcode, cat_name, sup_idx, p_price, s_price, tax, stock, min_stock in products_data:
            prod, _ = Product.objects.get_or_create(
                sku=sku,
                defaults={
                    'name': name,
                    'barcode': barcode,
                    'category': cat_map[cat_name],
                    'supplier': created_suppliers[sup_idx],
                    'description': f'Premium enterprise grade {name} with manufacturer warranty.',
                    'purchase_price': Decimal(str(p_price)),
                    'selling_price': Decimal(str(s_price)),
                    'tax_percentage': Decimal(str(tax)),
                    'stock_quantity': stock,
                    'minimum_stock': min_stock,
                    'is_active': True,
                }
            )
            # Update stock in case it already existed
            prod.stock_quantity = stock
            prod.minimum_stock = min_stock
            prod.selling_price = Decimal(str(s_price))
            prod.save()
            created_products.append(prod)

        # 5. Historical Sales Transactions
        now = timezone.now()
        customer_names = [
            ('Rohit Sharma', '+91 98200 12345'),
            ('Priya Nair', '+91 98470 23456'),
            ('Aditya Verma', '+91 98100 34567'),
            ('Ananya Iyer', '+91 98840 45678'),
            ('Rahul Das', '+91 98310 56789'),
            ('Kavita Patel', '+91 98790 67890'),
            ('Vikram Joshi', '+91 98220 78901'),
            ('Sneha Menon', '+91 98450 89012'),
            ('', ''),  # Walk-in
            ('', ''),  # Walk-in
        ]

        # Check existing sales count
        existing_sales_count = Sale.objects.count()
        if existing_sales_count < 20:
            self.stdout.write('Generating realistic sales transactions across past 14 days...')
            payment_methods = [Sale.PaymentMethod.CASH, Sale.PaymentMethod.CARD, Sale.PaymentMethod.UPI]

            for days_ago in range(13, -1, -1):
                # 2 to 4 sales per day
                sales_count_for_day = random.randint(2, 4)
                if days_ago == 0:
                    sales_count_for_day = 4  # today

                for _ in range(sales_count_for_day):
                    sale_time = now - timedelta(days=days_ago, hours=random.randint(1, 8), minutes=random.randint(0, 59))
                    cust_name, cust_phone = random.choice(customer_names)
                    staff = random.choice(created_staff)
                    payment_method = random.choice(payment_methods)

                    # Select 1 to 3 items
                    selected_items = random.sample(created_products, k=random.randint(1, 3))
                    subtotal = Decimal('0.00')
                    total_tax = Decimal('0.00')
                    items_payload = []

                    for prod in selected_items:
                        qty = random.randint(1, 2)
                        item_sub = prod.selling_price * qty
                        item_tax = (item_sub * prod.tax_percentage) / Decimal('100')
                        subtotal += item_sub
                        total_tax += item_tax
                        items_payload.append({
                            'product': prod,
                            'quantity': qty,
                            'unit_price': prod.selling_price,
                            'tax_percentage': prod.tax_percentage,
                            'subtotal': item_sub,
                            'tax': item_tax,
                            'total': item_sub + item_tax,
                        })

                    discount = Decimal('0.00')
                    if random.random() < 0.25 and subtotal > Decimal('2000.00'):
                        discount = Decimal(str(random.choice([100, 200, 500])))

                    total_amount = subtotal + total_tax - discount

                    sale = Sale.objects.create(
                        staff=staff,
                        customer_name=cust_name,
                        customer_phone=cust_phone,
                        subtotal=subtotal,
                        tax_amount=total_tax,
                        discount_amount=discount,
                        total_amount=total_amount,
                        payment_method=payment_method,
                        payment_status=Sale.PaymentStatus.PAID,
                        notes='Demo order' if cust_name else '',
                    )
                    # Manually update created_at to simulate history
                    Sale.objects.filter(id=sale.id).update(created_at=sale_time)

                    for ip in items_payload:
                        SaleItem.objects.create(
                            sale=sale,
                            product=ip['product'],
                            quantity=ip['quantity'],
                            unit_price=ip['unit_price'],
                            tax_percentage=ip['tax_percentage'],
                            discount_amount=Decimal('0.00'),
                            subtotal=ip['subtotal'],
                            total=ip['total'],
                        )

                    LedgerEntry.objects.create(
                        entry_type=LedgerEntry.EntryType.SALE,
                        reference=sale.invoice_number,
                        description=f'POS Sale {sale.invoice_number}',
                        debit=Decimal('0.00'),
                        credit=total_amount,
                        created_by=staff,
                    )
                    LedgerEntry.objects.filter(reference=sale.invoice_number).update(created_at=sale_time)

        self.stdout.write(self.style.SUCCESS(
            f'Demo data successfully seeded!\n'
            f'• Products: {Product.objects.count()}\n'
            f'• Categories: {Category.objects.count()}\n'
            f'• Suppliers: {Supplier.objects.count()}\n'
            f'• Staff Accounts: {User.objects.filter(role=User.Role.STAFF).count()}\n'
            f'• Total Sales: {Sale.objects.count()}'
        ))
