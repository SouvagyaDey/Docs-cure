"""Populate image_url for all ProductStore items."""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from products.models import ProductStore

IMAGES = {
    'first aid': 'https://images.unsplash.com/photo-1603398938378-e54eab446dde?w=600&h=600&fit=crop&q=80',
    'nebulizer': 'https://images.unsplash.com/photo-1583947215259-38e31be8751f?w=600&h=600&fit=crop&q=80',
    'yoga mat': 'https://images.unsplash.com/photo-1592432678016-e910b452f9a2?w=600&h=600&fit=crop&q=80',
    'thermometer': 'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=600&h=600&fit=crop&q=80',
    'multivitamin': 'https://images.unsplash.com/photo-1550572017-edd951aa8f72?w=600&h=600&fit=crop&q=80',
    'bp monitor': 'https://images.unsplash.com/photo-1631549916768-4119b2e5f926?w=600&h=600&fit=crop&q=80',
    'blood pressure': 'https://images.unsplash.com/photo-1631549916768-4119b2e5f926?w=600&h=600&fit=crop&q=80',
    'resistance band': 'https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=600&h=600&fit=crop&q=80',
    'whey': 'https://images.unsplash.com/photo-1593095948071-474c5cc2c129?w=600&h=600&fit=crop&q=80',
    'protein': 'https://images.unsplash.com/photo-1593095948071-474c5cc2c129?w=600&h=600&fit=crop&q=80',
    'paracetamol': 'https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=600&h=600&fit=crop&q=80',
    'sanitizer': 'https://images.unsplash.com/photo-1584483766114-2cea6facdf57?w=600&h=600&fit=crop&q=80',
    'oximeter': 'https://images.unsplash.com/photo-1585435557343-3b092031a831?w=600&h=600&fit=crop&q=80',
    'pulse': 'https://images.unsplash.com/photo-1585435557343-3b092031a831?w=600&h=600&fit=crop&q=80',
    'stethoscope': 'https://images.unsplash.com/photo-1581093458791-9d42e3c2fd45?w=600&h=600&fit=crop&q=80',
    'wheelchair': 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=600&h=600&fit=crop&q=80',
    'knee brace': 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=600&h=600&fit=crop&q=80',
    'vitamin c': 'https://images.unsplash.com/photo-1550572017-edd951aa8f72?w=600&h=600&fit=crop&q=80',
    'mask': 'https://images.unsplash.com/photo-1584634731339-252c581abfc5?w=600&h=600&fit=crop&q=80',
    'surgical': 'https://images.unsplash.com/photo-1584634731339-252c581abfc5?w=600&h=600&fit=crop&q=80',
    'dumbbell': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&h=600&fit=crop&q=80',
    'glucometer': 'https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=600&h=600&fit=crop&q=80',
    'glucose': 'https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=600&h=600&fit=crop&q=80',
    'essential oil': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=600&h=600&fit=crop&q=80',
    'aromatherapy': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=600&h=600&fit=crop&q=80',
    'band': 'https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=600&h=600&fit=crop&q=80',
    'treadmill': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&h=600&fit=crop&q=80',
    'omega': 'https://images.unsplash.com/photo-1550572017-edd951aa8f72?w=600&h=600&fit=crop&q=80',
    'fish oil': 'https://images.unsplash.com/photo-1550572017-edd951aa8f72?w=600&h=600&fit=crop&q=80',
    'heating pad': 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=600&h=600&fit=crop&q=80',
    'cough': 'https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=600&h=600&fit=crop&q=80',
    'syrup': 'https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=600&h=600&fit=crop&q=80',
}

CAT_FALLBACKS = {
    'medicine': 'https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=600&h=600&fit=crop&q=80',
    'equipment': 'https://images.unsplash.com/photo-1581093458791-9d42e3c2fd45?w=600&h=600&fit=crop&q=80',
    'wellness': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=600&h=600&fit=crop&q=80',
    'fitness': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&h=600&fit=crop&q=80',
}

products = ProductStore.objects.all()
for p in products:
    name_lower = p.name.lower()
    img = None
    for keyword, url in IMAGES.items():
        if keyword in name_lower:
            img = url
            break
    if not img:
        img = CAT_FALLBACKS.get(p.category, CAT_FALLBACKS['medicine'])
    p.image_url = img
    p.save(update_fields=['image_url'])
    print(f'  {p.name} -> set')

print(f'\nDone: {products.count()} products updated with images')
