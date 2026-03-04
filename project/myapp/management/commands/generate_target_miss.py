from django.core.management.base import BaseCommand
from django.db.models import Sum, Avg, Count
from myapp.models import Invoice
from analysis.models import TargetMissPrediction
from analysis.services.predictor import predict_target_miss
import random


class Command(BaseCommand):
    help = "Generate Target Miss Prediction from invoices"

    def handle(self, *args, **kwargs):
        TargetMissPrediction.objects.all().delete()

        sales_data = (
            Invoice.objects
            .values("salesperson__name")
            .annotate(
                achieved=Sum("grand_total"),
                invoice_count=Count("id"),
                avg_invoice=Avg("grand_total"),
            )
        )

        for row in sales_data:
            target = random.randint(400000, 800000)
            active_days = random.randint(18, 26)

            result = predict_target_miss([
                target,
                row["invoice_count"],
                row["avg_invoice"],
                active_days
            ])

            TargetMissPrediction.objects.create(
                salesperson_name=row["salesperson__name"],
                target_amount=target,
                risk_percent=result["risk_percent"],
                prediction=result["prediction"]
            )

        self.stdout.write(
            self.style.SUCCESS("✅ Target Miss data generated")
        )
