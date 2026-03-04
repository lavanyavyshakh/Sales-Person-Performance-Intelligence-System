from django.core.management.base import BaseCommand
from django.db.models import Sum
from datetime import date
from dateutil.relativedelta import relativedelta

from myapp.models import Invoice
from myapp.models import Salesperson
from myapp.models import Target


class Command(BaseCommand):
    help = "Generate last 4 months sales targets from invoice data"

    def handle(self, *args, **kwargs):

        # Base month → January 2026
        base_month = date(2026, 1, 1)

        months = [
            base_month,
            base_month - relativedelta(months=1),
            base_month - relativedelta(months=2),
            base_month - relativedelta(months=3),
        ]

        created, updated = 0, 0

        for salesperson in Salesperson.objects.all():
            for m in months:

                total_sales = (
                    Invoice.objects.filter(
                        salesperson=salesperson,
                        sale_date__year=m.year,
                        sale_date__month=m.month
                    )
                    .aggregate(total=Sum("grand_total"))
                    ["total"] or 0
                )

                obj, is_created = Target.objects.update_or_create(
                    salesperson=salesperson,
                    month=m.month,
                    year=m.year,
                    defaults={
                        "target_type": "value",
                        "target_value": total_sales,
                        "product_category": None
                    }
                )

                if is_created:
                    created += 1
                else:
                    updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Targets completed | Created: {created}, Updated: {updated}"
            )
        )
