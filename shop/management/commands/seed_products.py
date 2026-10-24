from decimal import Decimal

import requests
from django.core.management.base import BaseCommand

from shop.models import Category, Product

CATEGORY_SLUGS = ["smartphones", "laptops", "tablets", "mobile-accessories"]


class Command(BaseCommand):
    help = "Import tech products from DummyJSON"

    def handle(self, *args, **options):
        for slug in CATEGORY_SLUGS:
            url = f"https://dummyjson.com/products/category/{slug}"
            data = requests.get(url, timeout=20).json()

            category, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={"name": slug.replace("-", " ").title()},
            )

            for item in data["products"]:
                Product.objects.update_or_create(
                    category=category,
                    title=item["title"],
                    defaults={
                        "description": item.get("description", ""),
                        "brand": item.get("brand", ""),
                        "price": Decimal(str(item["price"])),
                        "discount_percentage": Decimal(str(item.get("discountPercentage", 0))),
                        "rating": Decimal(str(item.get("rating", 0))),
                        "stock": item.get("stock", 0),
                        "thumbnail": item.get("thumbnail", ""),
                    },
                )

            self.stdout.write(f"Imported {slug}")
