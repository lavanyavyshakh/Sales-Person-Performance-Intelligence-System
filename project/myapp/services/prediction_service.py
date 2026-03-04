from django.db.models import Sum
from datetime import date
import math
from decimal import Decimal
from myapp.models import Invoice, Salesperson


def get_last_n_month_sales(salesperson, n=3):
    today = date.today()
    sales = []

    for i in range(n):
        month = today.month - i
        year = today.year

        if month <= 0:
            month += 12
            year -= 1

        total = Invoice.objects.filter(
            salesperson=salesperson,
            sale_date__year=year,
            sale_date__month=month
        ).aggregate(total=Sum("grand_total"))["total"] or 0

        sales.append(total)

    return sales


def predict_next_month_sales(monthly_sales):
    weights = [
        Decimal("0.6"),
        Decimal("0.25"),
        Decimal("0.15")
    ]

    prediction = sum(
        s * w for s, w in zip(monthly_sales, weights)
    )

    return round(float(prediction), 2)



def calculate_confidence(monthly_sales, predicted_amount):
    """
    Confidence based on:
    1. Sales stability
    2. Strength of predicted amount
    """

    values = [float(s) for s in monthly_sales if float(s) > 0]

    # Case 1: No usable history
    if not values:
        # Confidence based only on predicted strength
        if predicted_amount > 0:
            return 0.55
        return 0.4

    # Case 2: One month data
    if len(values) == 1:
        base_confidence = 0.55
    else:
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = math.sqrt(variance)

        stability_ratio = std_dev / mean if mean else 1
        base_confidence = max(0.5, 1 - stability_ratio)

    # Strength factor (scale confidence based on predicted amount)
    strength_factor = min(1.0, predicted_amount / max(values))

    confidence = 0.6 * base_confidence + 0.4 * strength_factor

    return round(min(0.95, max(0.4, confidence)), 2)




def generate_next_month_prediction(salesperson):
    monthly_sales = get_last_n_month_sales(salesperson)
    predicted_amount = predict_next_month_sales(monthly_sales)
    confidence = calculate_confidence(monthly_sales, predicted_amount)
    return predicted_amount, confidence
