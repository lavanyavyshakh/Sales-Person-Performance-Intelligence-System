import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from myapp.models import Product


class Command(BaseCommand):
    help = "Generate 1000 products (without touching invoices, customers, salespersons)"

    def handle(self, *args, **kwargs):
        TARGET_COUNT = 1000

        existing_count = Product.objects.count()
        to_create = TARGET_COUNT - existing_count

        if to_create <= 0:
            self.stdout.write(
                self.style.WARNING(
                    f"⚠ Already {existing_count} products exist. No new products created."
                )
            )
            return

        materials = list(Product.MATERIAL_UNIT_MAP.keys())

        created = 0

        for i in range(existing_count + 1, TARGET_COUNT + 1):
            material = random.choice(materials)
            unit_type = random.choice(
                Product.MATERIAL_UNIT_MAP[material]
            )

            name = f"{material.capitalize()} Product {i}"

            Product.objects.create(
                name=name,
                material_type=material,
                category="fabric",
                unit_type=unit_type,
                price_per_unit=Decimal(
                    random.randint(50, 500)
                ),
                status=True,
            )

            created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ {created} products created successfully"
            )
        )
