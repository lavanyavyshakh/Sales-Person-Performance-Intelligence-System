import csv
import random
from faker import Faker
from datetime import date, timedelta

fake = Faker("en_IN")  # Indian-style names

OUTPUT_FILE = "analysis/datasets/invoices.csv"
TOTAL_INVOICES = 5000

# ===============================
# REALISTIC SALESPERSON NAMES (30)
# ===============================
SALESPERSONS = list({fake.name() for _ in range(50)})[:30]

# ===============================
# REALISTIC CUSTOMER BUSINESS NAMES (1000)
# ===============================
BUSINESS_SUFFIXES = [
    "Traders", "Enterprises", "Distributors",
    "Retailers", "Stores", "Mart", "Fabrics", "Textiles"
]

CUSTOMERS = list({
    f"{fake.company()} {random.choice(BUSINESS_SUFFIXES)}"
    for _ in range(1200)
})[:1000]

# ===============================
# PRODUCTS (MATCH YOUR MODEL)
# ===============================
PRODUCTS = [
    ("Cotton Fabric", "cotton", 120),
    ("Yarn Roll", "yarn", 90),
    ("Wool Fabric", "wool", 200),
    ("Silk Fabric", "silk", 350),
    ("Polyester Sheet", "polyester", 150),
    ("Nylon Fabric", "nylon", 180),
]

SALE_TYPES = ["cash", "credit"]

# ===============================
# RANDOM DATE RANGE
# ===============================
start_date = date(2024, 1, 1)
end_date = date(2026, 12, 31)
days_range = (end_date - start_date).days

# ===============================
# CSV GENERATION
# ===============================
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "invoice_number",
        "sale_date",
        "sale_type",
        "salesperson",
        "customer",
        "product",
        "material_type",
        "quantity",
        "price",
    ])

    invoice_no = 1

    for _ in range(TOTAL_INVOICES):
        inv = f"INV-{invoice_no:05d}"
        invoice_no += 1

        sale_date = start_date + timedelta(
            days=random.randint(0, days_range)
        )

        sale_type = random.choice(SALE_TYPES)
        salesperson = random.choice(SALESPERSONS)
        customer = random.choice(CUSTOMERS)

        for _ in range(random.randint(2, 4)):
            product, material, price = random.choice(PRODUCTS)
            quantity = random.randint(1, 25)

            writer.writerow([
                inv,
                sale_date.strftime("%Y-%m-%d"),
                sale_type,
                salesperson,
                customer,
                product,
                material,
                quantity,
                price,
            ])

print("✅ invoices.csv generated with REALISTIC names")
