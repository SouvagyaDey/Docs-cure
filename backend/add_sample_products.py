import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from products.models import Product, ProductStore, ProductCategory
from decimal import Decimal

def add_sample_products():
    """Add sample medical products to the database"""
    
    products_data = [
        # Medicines
        {
            'name': 'Aspirin 100mg (Box of 30)',
            'category': ProductCategory.MEDICINE,
            'price': Decimal('12.99'),
            'manufacturer': 'Bayer Healthcare',
            'description': 'Low-dose aspirin for heart health and pain relief. Used for preventing heart attacks and strokes in at-risk patients.',
            'stock': 150,
            'features': {
                'dosage': '100mg',
                'quantity': '30 tablets',
                'form': 'Tablet',
                'prescription_required': False
            }
        },
        {
            'name': 'Amoxicillin 500mg (Box of 21)',
            'category': ProductCategory.MEDICINE,
            'price': Decimal('24.99'),
            'manufacturer': 'GSK Pharmaceuticals',
            'description': 'Broad-spectrum antibiotic used to treat bacterial infections including respiratory, ear, throat, and urinary tract infections.',
            'stock': 80,
            'features': {
                'dosage': '500mg',
                'quantity': '21 capsules',
                'form': 'Capsule',
                'prescription_required': True
            }
        },
        {
            'name': 'Lisinopril 10mg (Box of 30)',
            'category': ProductCategory.MEDICINE,
            'price': Decimal('18.50'),
            'manufacturer': 'Merck & Co.',
            'description': 'ACE inhibitor used to treat high blood pressure and heart failure. Helps prevent strokes and kidney problems.',
            'stock': 120,
            'features': {
                'dosage': '10mg',
                'quantity': '30 tablets',
                'form': 'Tablet',
                'prescription_required': True
            }
        },
        {
            'name': 'Paracetamol 500mg (Box of 50)',
            'category': ProductCategory.MEDICINE,
            'price': Decimal('8.99'),
            'manufacturer': 'Johnson & Johnson',
            'description': 'Effective pain reliever and fever reducer. Suitable for headaches, muscle aches, arthritis, and cold symptoms.',
            'stock': 200,
            'features': {
                'dosage': '500mg',
                'quantity': '50 tablets',
                'form': 'Tablet',
                'prescription_required': False
            }
        },
        {
            'name': 'Omeprazole 20mg (Box of 28)',
            'category': ProductCategory.MEDICINE,
            'price': Decimal('15.99'),
            'manufacturer': 'AstraZeneca',
            'description': 'Proton pump inhibitor for treating acid reflux, heartburn, and stomach ulcers.',
            'stock': 95,
            'features': {
                'dosage': '20mg',
                'quantity': '28 capsules',
                'form': 'Capsule',
                'prescription_required': False
            }
        },
        
        # Medical Equipment
        {
            'name': 'Digital Blood Pressure Monitor',
            'category': ProductCategory.EQUIPMENT,
            'price': Decimal('45.99'),
            'manufacturer': 'Omron Healthcare',
            'description': 'Automatic upper arm blood pressure monitor with large LCD display. Detects irregular heartbeat and stores up to 60 readings.',
            'stock': 50,
            'features': {
                'type': 'Automatic',
                'display': 'LCD',
                'memory': '60 readings',
                'warranty': '2 years',
                'cuff_size': 'Universal (22-42cm)'
            }
        },
        {
            'name': 'Infrared Thermometer (Non-Contact)',
            'category': ProductCategory.EQUIPMENT,
            'price': Decimal('29.99'),
            'manufacturer': 'Braun',
            'description': 'Fast and accurate non-contact infrared thermometer. Ideal for checking body temperature without physical contact.',
            'stock': 75,
            'features': {
                'measurement_time': '1 second',
                'measurement_range': '32-42.9°C',
                'accuracy': '±0.2°C',
                'battery': 'AAA x 2',
                'color_coded_fever': True
            }
        },
        {
            'name': 'Pulse Oximeter',
            'category': ProductCategory.EQUIPMENT,
            'price': Decimal('34.99'),
            'manufacturer': 'Masimo Corporation',
            'description': 'Finger pulse oximeter for measuring blood oxygen saturation (SpO2) and pulse rate. Essential for monitoring respiratory conditions.',
            'stock': 65,
            'features': {
                'spo2_range': '70-100%',
                'pulse_rate_range': '30-235 bpm',
                'display': 'OLED',
                'battery_life': '30 hours',
                'auto_off': True
            }
        },
        {
            'name': 'Glucometer Blood Sugar Monitor Kit',
            'category': ProductCategory.EQUIPMENT,
            'price': Decimal('39.99'),
            'manufacturer': 'Accu-Chek by Roche',
            'description': 'Complete glucose monitoring system with meter, 50 test strips, and lancets. Essential for diabetes management.',
            'stock': 45,
            'features': {
                'test_time': '5 seconds',
                'sample_size': '0.6 microliters',
                'memory': '500 readings',
                'includes': 'Meter, 50 strips, 50 lancets, carrying case'
            }
        },
        {
            'name': 'Nebulizer Machine',
            'category': ProductCategory.EQUIPMENT,
            'price': Decimal('65.00'),
            'manufacturer': 'Philips Respironics',
            'description': 'Compressor nebulizer for efficient delivery of medication for respiratory conditions like asthma and COPD.',
            'stock': 30,
            'features': {
                'type': 'Compressor',
                'particle_size': '0.5-10 microns',
                'medication_capacity': '10ml',
                'noise_level': '<65 dB',
                'weight': '1.8 kg'
            }
        },
        {
            'name': 'First Aid Kit (Family Size)',
            'category': ProductCategory.EQUIPMENT,
            'price': Decimal('49.99'),
            'manufacturer': 'MediPro',
            'description': 'Comprehensive 200-piece first aid kit for home, office, or travel. Includes bandages, antiseptics, and emergency supplies.',
            'stock': 85,
            'features': {
                'pieces': '200+',
                'case': 'Portable hard case',
                'contents': 'Bandages, gauze, antiseptic, scissors, tweezers, gloves, thermometer',
                'size': '25x20x8 cm'
            }
        },
        
        # Wellness Products
        {
            'name': 'Vitamin D3 5000 IU (120 Softgels)',
            'category': ProductCategory.WELLNESS,
            'price': Decimal('19.99'),
            'manufacturer': 'Nature Made',
            'description': 'High-potency Vitamin D3 supplement for bone health, immune support, and mood regulation.',
            'stock': 150,
            'features': {
                'dosage': '5000 IU',
                'quantity': '120 softgels',
                'supply': '4 months',
                'gluten_free': True,
                'non_gmo': True
            }
        },
        {
            'name': 'Omega-3 Fish Oil 1400mg (90 Softgels)',
            'category': ProductCategory.WELLNESS,
            'price': Decimal('27.99'),
            'manufacturer': 'Nordic Naturals',
            'description': 'Premium omega-3 fish oil for heart, brain, and joint health. Molecularly distilled for purity.',
            'stock': 110,
            'features': {
                'epa': '700mg',
                'dha': '500mg',
                'quantity': '90 softgels',
                'purity': 'Third-party tested',
                'sustainable': 'MSC certified'
            }
        },
        {
            'name': 'Multivitamin for Adults (60 Tablets)',
            'category': ProductCategory.WELLNESS,
            'price': Decimal('22.99'),
            'manufacturer': 'Centrum',
            'description': 'Complete daily multivitamin with essential vitamins and minerals for immune support and energy.',
            'stock': 175,
            'features': {
                'vitamins': '23 essential nutrients',
                'quantity': '60 tablets',
                'supply': '2 months',
                'iron_free': False,
                'age_group': 'Adults 18+'
            }
        },
        {
            'name': 'Probiotic Complex 50 Billion CFU (30 Capsules)',
            'category': ProductCategory.WELLNESS,
            'price': Decimal('34.99'),
            'manufacturer': 'Garden of Life',
            'description': 'High-potency probiotic with 15 diverse strains for digestive and immune health. Shelf-stable formula.',
            'stock': 90,
            'features': {
                'cfu': '50 billion',
                'strains': '15',
                'quantity': '30 capsules',
                'refrigeration': 'Not required',
                'vegan': True
            }
        },
        {
            'name': 'Melatonin 10mg (60 Tablets)',
            'category': ProductCategory.WELLNESS,
            'price': Decimal('14.99'),
            'manufacturer': 'Natrol',
            'description': 'Natural sleep aid supplement to help you fall asleep faster and improve sleep quality.',
            'stock': 140,
            'features': {
                'dosage': '10mg',
                'quantity': '60 tablets',
                'form': 'Fast-dissolve',
                'drug_free': True,
                'non_habit_forming': True
            }
        },
        
        # Fitness Products
        {
            'name': 'Resistance Bands Set (5 Levels)',
            'category': ProductCategory.FITNESS,
            'price': Decimal('24.99'),
            'manufacturer': 'TheraBand',
            'description': 'Professional resistance bands set with 5 different resistance levels for strength training and physical therapy.',
            'stock': 60,
            'features': {
                'levels': '5 (Extra Light to Extra Heavy)',
                'material': 'Natural latex',
                'includes': 'Carrying bag, door anchor, ankle straps',
                'colors': 'Color-coded by resistance'
            }
        },
        {
            'name': 'Yoga Mat (6mm Premium)',
            'category': ProductCategory.FITNESS,
            'price': Decimal('32.99'),
            'manufacturer': 'Manduka',
            'description': 'High-density cushioned yoga mat with superior grip and joint protection. Eco-friendly materials.',
            'stock': 55,
            'features': {
                'thickness': '6mm',
                'size': '183cm x 61cm',
                'material': 'TPE (non-toxic)',
                'texture': 'Non-slip',
                'weight': '1.2 kg'
            }
        },
        {
            'name': 'Foam Roller (High Density)',
            'category': ProductCategory.FITNESS,
            'price': Decimal('28.99'),
            'manufacturer': 'TriggerPoint',
            'description': 'High-density foam roller for muscle recovery, myofascial release, and improved flexibility.',
            'stock': 70,
            'features': {
                'length': '33cm',
                'diameter': '14cm',
                'density': 'High',
                'surface': 'Textured',
                'weight_capacity': '250 kg'
            }
        },
        {
            'name': 'Adjustable Dumbbells (2-12kg per hand)',
            'category': ProductCategory.FITNESS,
            'price': Decimal('89.99'),
            'manufacturer': 'Bowflex',
            'description': 'Space-saving adjustable dumbbells that replace 15 sets of weights. Quick-change mechanism.',
            'stock': 25,
            'features': {
                'weight_range': '2-12kg per hand',
                'increments': '2kg',
                'material': 'Steel and plastic',
                'space_saving': True,
                'includes': 'Storage tray'
            }
        },
        {
            'name': 'Jump Rope (Adjustable)',
            'category': ProductCategory.FITNESS,
            'price': Decimal('15.99'),
            'manufacturer': 'RENPHO',
            'description': 'Adjustable speed jump rope with ball bearings for smooth rotation. Digital counter tracks jumps and calories.',
            'stock': 100,
            'features': {
                'length': 'Adjustable 2.5-3m',
                'bearings': 'Ball bearings',
                'handles': 'Ergonomic foam',
                'counter': 'Digital LCD',
                'weight': '180g'
            }
        },
    ]
    
    print(f"Adding {len(products_data)} sample products to the database...")
    
    created_count = 0
    for product_data in products_data:
        # Extract features
        features = product_data.pop('features', {})
        
        # Create Product first (for features)
        product = Product.objects.create(features=features)
        
        # Create ProductStore with reference to Product
        ProductStore.objects.create(
            product_id=product.id,
            **product_data
        )
        
        created_count += 1
        print(f"✓ Added: {product_data['name']}")
    
    print(f"\n✅ Successfully added {created_count} products to the database!")
    
    # Print summary
    print("\n📊 Summary by category:")
    for category in ProductCategory:
        count = ProductStore.objects.filter(category=category.value).count()
        print(f"  - {category.label}: {count} products")
    
    total_stock = sum(p.stock for p in ProductStore.objects.all())
    print(f"\n📦 Total stock items: {total_stock}")
    print(f"💰 Price range: ${ProductStore.objects.order_by('price').first().price} - ${ProductStore.objects.order_by('-price').first().price}")

if __name__ == '__main__':
    add_sample_products()
