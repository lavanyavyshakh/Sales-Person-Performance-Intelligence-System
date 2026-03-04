import csv
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.dateparse import parse_date

from myapp.models import (
    Invoice,
    InvoiceItem,
    Product,
    Customer,
    Salesperson
)


def map_product_category(material):
    """
    Map product material to valid Salesperson.product_category choice
    """
    if material in ["cotton", "silk", "wool"]:
        return material
    return "synthetic"  # yarn, polyester, nylon


class Command(BaseCommand):
    help = "Generate 5000 invoices, 30 salespersons, 1000 products"

    def handle(self, *args, **kwargs):
        file_path = "analysis/datasets/invoices.csv"
        invoice_cache = {}

        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            with transaction.atomic():
                for row in reader:

                    material = row["material_type"]

                    # ---------------- SALESPERSON ----------------
                    salesperson, _ = Salesperson.objects.get_or_create(
                        name=row["salesperson"],
                        defaults={
                            "region": random.choice(
                                ["North", "South", "East", "West"]
                            ),
                            "product_category": map_product_category(material),
                            "phone": "9000000000",
                            "email": f"{row['salesperson'].replace(' ', '').lower()}@company.com",
                            "status": True,
                        }
                    )

                    # ---------------- CUSTOMER ----------------
                    customer, _ = Customer.objects.get_or_create(
                        business_name=row["customer"],
                        defaults={
                            "contact_person": "Manager",
                            "customer_type": random.choice(
                                ["retail", "wholesale", "distributor"]
                            ),
                            "phone": "8000000000",
                            "email": f"{row['customer'].replace(' ', '').lower()}@mail.com",
                            "location": random.choice(
                                ["Bangalore", "Chennai", "Hyderabad", "Mumbai"]
                            ),
                            "credit_limit": Decimal("1000000.00"),
                            "status": True,
                        }
                    )

                    # ---------------- INVOICE ----------------
                    inv_no = row["invoice_number"]

                    if inv_no not in invoice_cache:
                        invoice = Invoice.objects.create(
                            invoice_number=inv_no,
                            sale_date=parse_date(row["sale_date"]),
                            sale_type=row["sale_type"],
                            salesperson=salesperson,
                            customer=customer,
                            grand_total=Decimal("0.00")
                        )
                        invoice_cache[inv_no] = invoice
                    else:
                        invoice = invoice_cache[inv_no]

                    # ---------------- PRODUCT ----------------
                    unit_type = Product.MATERIAL_UNIT_MAP[material][0]

                    product, _ = Product.objects.get_or_create(
                        name=row["product"],
                        defaults={
                            "material_type": material,
                            "category": "Fabric",
                            "unit_type": unit_type,
                            "price_per_unit": Decimal(row["price"]),
                            "status": True,
                        }
                    )

                    # ---------------- INVOICE ITEM ----------------
                    qty = int(row["quantity"])
                    price = Decimal(row["price"])

                    InvoiceItem.objects.create(
                        invoice=invoice,
                        product=product,
                        quantity=qty,
                        price=price
                    )

                    invoice.grand_total += qty * price
                    invoice.save(update_fields=["grand_total"])

        self.stdout.write(
            self.style.SUCCESS("✅ 5000 invoices generated successfully")
        )
