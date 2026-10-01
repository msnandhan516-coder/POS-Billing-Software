import os
import sys
import urllib.request
import django
from io import BytesIO
from PIL import Image

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product

image_mappings = {
    'RM12-PRO-256': 'photo-1511707171634-5f897ff02aa9',
    'RN13-128-BLK': 'photo-1580910051074-3eb694886505',
    'SAM-S24-256': 'photo-1610945265064-0e34e5519bbf',
    'IP15P-128-BLU': 'photo-1592750475338-74b7b21085ab',
    'OP12-256-GRN': 'photo-1565849904461-04a58ad377e0',
    'PIX8-128-OBS': 'photo-1598327105666-5b89351aff97',

    'DELL-INSP-15': 'photo-1588872657578-7efd1f1555ed',
    'HP-PAV-14-SIL': 'photo-1496181133206-80ce9b88a853',
    'LEN-IP3-SLIM': 'photo-1603302576837-37561b2e2302',
    'MBA-M2-256': 'photo-1517336714731-489689fd1ca8',
    'ASUS-VIVO-16': 'photo-1525547719571-a2d4ac8945e2',

    'SONY-XM5-BLK': 'photo-1505740420928-5e560c06d30e',
    'JBL-FLIP6-BLU': 'photo-1608043152269-423dbba4e7e1',
    'APP-GEN2-USBC': 'photo-1590658268037-6bf12165a8df',
    'BOAT-RCK-450': 'photo-1546435770-a3e426bf472b',
    'BOSE-QC45-BLK': 'photo-1572536147248-ac59a8abfa4b',

    'ANK-PB-20K': 'photo-1609592426815-5853f6630f53',
    'CAB-USBC-60W': 'photo-1541689592655-f5f52825a3b8',
    'CHG-65W-GAN': 'photo-1583863788434-e58a36330cf0',
    'SPG-ARMOR-GEN': 'photo-1601784551446-20c9e07cdbdb',

    'LOGI-MX3S-GRY': 'photo-1615663245857-ac93bb7c39e7',
    'KEY-K2-RGB': 'photo-1587829741301-dc798b83add3',
    'DELL-MON-24': 'photo-1527443224154-c4a3942d3acf',
    'LOGI-C920-PRO': 'photo-1587826080692-f439cd0b70da',

    'TPL-AX73-W6': 'photo-1544197150-b99a580bb7a8',
    'NET-NIGHT-XR5': 'photo-1606904825846-647eb07f5be2',
}

media_dir = os.path.join(os.path.dirname(__file__), 'media', 'products')
os.makedirs(media_dir, exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for sku, photo_id in image_mappings.items():
    try:
        product = Product.objects.filter(sku=sku).first()
        if not product:
            continue

        filename = f"{sku.lower().replace('-', '_')}.jpg"
        target_path = os.path.join(media_dir, filename)

        if not os.path.exists(target_path) or os.path.getsize(target_path) < 1000:
            url = f"https://images.unsplash.com/{photo_id}?w=500&h=500&fit=crop&crop=entropy&auto=format&q=85"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as response:
                img_data = response.read()

            # Process with Pillow to ensure standard 500x500 RGB
            img = Image.open(BytesIO(img_data)).convert('RGB')
            img.thumbnail((500, 500), Image.Resampling.LANCZOS)
            img.save(target_path, 'JPEG', quality=85)
            print(f"[OK] Downloaded and saved: {filename}")
        else:
            print(f"[EXISTS] Cached: {filename}")

        product.image = f"products/{filename}"
        product.save(update_fields=['image'])

    except Exception as e:
        print(f"[ERR] Failed {sku}: {e}")

print("Image processing complete. Active products with images:")
print(Product.objects.exclude(image='').count())
