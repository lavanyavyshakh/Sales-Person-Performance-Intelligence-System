import csv
import random

# ================= TARGET MISS =================
with open("target_miss.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "target_amount", "achieved_amount",
        "invoice_count", "avg_invoice_value",
        "active_days", "target_missed"
    ])

    for _ in range(2000):
        target = random.randint(200000, 800000)
        achieved = random.randint(150000, 850000)
        missed = 1 if achieved < target else 0

        writer.writerow([
            target,
            achieved,
            random.randint(15, 60),
            random.randint(8000, 20000),
            random.randint(18, 26),
            missed
        ])

# ================= PERFORMANCE CONSISTENCY =================
with open("performance_consistency.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "salesperson_id", "month",
        "target_amount", "achieved_amount"
    ])

    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    for i in range(2000):
        writer.writerow([
            random.randint(1, 30),
            random.choice(months),
            random.randint(200000, 700000),
            random.randint(150000, 750000),
        ])

# ================= FOCUS ACCOUNTS =================
with open("focus_accounts.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "customer_id", "total_revenue",
        "invoice_count", "avg_invoice_value"
    ])

    for _ in range(2000):
        invoice_count = random.randint(1, 30)
        avg_invoice = random.randint(2000, 10000)

        writer.writerow([
            random.randint(1, 500),
            invoice_count * avg_invoice,
            invoice_count,
            avg_invoice
        ])

print("✅ ALL CSV FILES GENERATED (2000 ROWS EACH)")
