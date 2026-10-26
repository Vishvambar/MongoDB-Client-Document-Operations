"""
Sample Data Seeder for MongoDB Collection Operations.
Populates realistic product documents with nested structures and arrays.
"""

from typing import List, Dict, Any
from mongodb_client import MongoOperationsService


def get_sample_products() -> List[Dict[str, Any]]:
    """Returns a list of rich product documents."""
    return [
        {
            "product_id": 101,
            "name": "UltraBook Pro 15",
            "category": "Computing",
            "price": 89999.00,
            "stock": 25,
            "rating": 4.8,
            "tags": ["laptop", "ultrabook", "intel-i7", "ssd"],
            "specs": {"brand": "TechCorp", "ram_gb": 16, "storage_gb": 512, "color": "Space Gray"},
            "is_featured": True
        },
        {
            "product_id": 102,
            "name": "Noise-Cancelling Headphones 700",
            "category": "Audio",
            "price": 19999.00,
            "stock": 50,
            "rating": 4.7,
            "tags": ["audio", "wireless", "bluetooth", "anc"],
            "specs": {"brand": "SoundWave", "battery_hours": 30, "color": "Midnight Black"},
            "is_featured": True
        },
        {
            "product_id": 103,
            "name": "Ergonomic Mechanical Keyboard",
            "category": "Accessories",
            "price": 4499.00,
            "stock": 120,
            "rating": 4.5,
            "tags": ["keyboard", "mechanical", "rgb", "usb-c"],
            "specs": {"brand": "KeyMaster", "switch_type": "Brown", "color": "White"},
            "is_featured": False
        },
        {
            "product_id": 104,
            "name": "Wireless Precision Gaming Mouse",
            "category": "Accessories",
            "price": 2999.00,
            "stock": 85,
            "rating": 4.3,
            "tags": ["mouse", "gaming", "wireless", "rgb"],
            "specs": {"brand": "KeyMaster", "dpi": 16000, "color": "Black"},
            "is_featured": False
        },
        {
            "product_id": 105,
            "name": "4K Ultra HD Smart Monitor 27-inch",
            "category": "Computing",
            "price": 32999.00,
            "stock": 40,
            "rating": 4.6,
            "tags": ["monitor", "4k", "hdr", "ips"],
            "specs": {"brand": "VisionPlus", "refresh_hz": 144, "color": "Silver"},
            "is_featured": True
        },
        {
            "product_id": 106,
            "name": "True Wireless Sport Earbuds",
            "category": "Audio",
            "price": 5999.00,
            "stock": 150,
            "rating": 4.2,
            "tags": ["audio", "wireless", "ipx7", "waterproof"],
            "specs": {"brand": "SoundWave", "battery_hours": 24, "color": "Blue"},
            "is_featured": False
        },
        {
            "product_id": 107,
            "name": "Smart Home Hub & Speaker",
            "category": "Smart Home",
            "price": 7999.00,
            "stock": 60,
            "rating": 4.4,
            "tags": ["smart-home", "voice-assistant", "wifi", "bluetooth"],
            "specs": {"brand": "HomeSense", "connectivity": "Zigbee", "color": "Charcoal"},
            "is_featured": False
        },
        {
            "product_id": 108,
            "name": "Smart Security Camera 2K",
            "category": "Smart Home",
            "price": 4999.00,
            "stock": 75,
            "rating": 4.1,
            "tags": ["smart-home", "security", "night-vision", "cloud"],
            "specs": {"brand": "HomeSense", "resolution": "2K QHD", "color": "White"},
            "is_featured": False
        },
        {
            "product_id": 109,
            "name": "Creator Studio Laptop 16",
            "category": "Computing",
            "price": 145000.00,
            "stock": 15,
            "rating": 4.9,
            "tags": ["laptop", "creator", "rtx-4070", "oled"],
            "specs": {"brand": "TechCorp", "ram_gb": 32, "storage_gb": 1000, "color": "Dark Ash"},
            "is_featured": True
        },
        {
            "product_id": 110,
            "name": "Studio Monitor Speakers (Pair)",
            "category": "Audio",
            "price": 24999.00,
            "stock": 30,
            "rating": 4.8,
            "tags": ["audio", "studio", "speakers", "pro"],
            "specs": {"brand": "SoundWave", "power_watts": 120, "color": "Matte Black"},
            "is_featured": True
        }
    ]


def seed_collection(reset: bool = True) -> int:
    """Seeds the collection with sample documents."""
    service = MongoOperationsService()
    if reset:
        print("[*] Resetting collection 'products'...")
        service.drop_collection()

    products = get_sample_products()
    ids = service.insert_batch(products)
    print(f"[✓] Successfully seeded {len(ids)} product documents into MongoDB collection!")
    return len(ids)


if __name__ == "__main__":
    seed_collection()
