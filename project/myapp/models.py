from django.db import models
from django.utils.timezone import now
from decimal import Decimal
from datetime import date
from django.core.exceptions import ValidationError

# Create your models here.

class Customer(models.Model):

    CUSTOMER_TYPE_CHOICES = [
        ('retail', 'Retail'),
        ('wholesale', 'Wholesale'),
        ('distributor', 'Distributor'),
    ]

    business_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)

    customer_type = models.CharField(
        max_length=20,
        choices=CUSTOMER_TYPE_CHOICES,
        default='retail'
    )

    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=100)

    credit_limit = models.DecimalField(
        max_digits=12, decimal_places=2
    )

    status = models.BooleanField(default=True)

    def __str__(self):
        return self.business_name

    @property
    def status_label(self):
        return "Active" if self.status else "Inactive"
    
class Salesperson(models.Model):

    PRODUCT_CATEGORY_CHOICES = [
        ('cotton', 'Cotton'),
        ('silk', 'Silk'),
        ('synthetic', 'Synthetic'),
        ('wool', 'Wool'),
    ]

    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

    product_category = models.CharField(
        max_length=20,
        choices=PRODUCT_CATEGORY_CHOICES
    )

    phone = models.CharField(max_length=15)
    email = models.EmailField()

    join_date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


    
# models.py
class Product(models.Model):

    MATERIAL_CHOICES = [
        ('cotton', 'Cotton'),
        ('yarn', 'Yarn'),
        ('wool', 'Wool'),
        ('silk', 'Silk'),
        ('polyester', 'Polyester'),
        ('nylon', 'Nylon'),
    ]

    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('meter', 'Meter'),
        ('piece', 'Piece'),
        ('litre', 'Litre'),  # kept for other modules if needed
    ]

    # ✅ STANDARD MATERIAL → UNIT MAP
    MATERIAL_UNIT_MAP = {
        'cotton': ['meter', 'piece'],
        'yarn': ['kg', 'meter'],
        'wool': ['kg'],                 # ❌ litre REMOVED
        'silk': ['meter', 'piece'],
        'polyester': ['meter'],
        'nylon': ['meter'],
    }

    name = models.CharField(max_length=100)

    material_type = models.CharField(
        max_length=20,
        choices=MATERIAL_CHOICES,
        default='cotton'
    )

    category = models.CharField(max_length=50)

    unit_type = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES
    )

    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """
        Enforce standard unit per material
        """
        allowed_units = self.MATERIAL_UNIT_MAP.get(self.material_type, [])

        if self.unit_type not in allowed_units:
            raise ValidationError({
                'unit_type': f"{self.get_unit_type_display()} is not valid for {self.get_material_type_display()}"
            })

    def save(self, *args, **kwargs):
        self.full_clean()  # ✅ Enforce validation everywhere
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    
class Sale(models.Model):
    invoice_no = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesperson = models.ForeignKey(Salesperson, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    sale_date = models.DateField()
    status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # ✅ Ensure numeric calculation
        self.total_amount = Decimal(self.quantity) * Decimal(self.price_per_unit)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.invoice_no

    
# models.py
from django.db import models
from django.utils.timezone import now


class Invoice(models.Model):
    INVOICE_TYPES = (
        ("cash", "Cash"),
        ("credit", "Credit"),
    )

    invoice_number = models.CharField(max_length=20, unique=True)

    # ✅ IMPORTANT: default added
    sale_date = models.DateField(default=now)

    sale_type = models.CharField(
        max_length=10,
        choices=INVOICE_TYPES
    )

    salesperson = models.ForeignKey(
        Salesperson,
        on_delete=models.CASCADE
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    remarks = models.TextField(blank=True, null=True)

    grand_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # ---------- PROPERTIES ----------
    @property
    def invoice_no(self):
        return self.invoice_number

    @property
    def date(self):
        return self.sale_date

    @property
    def invoice_type(self):
        return self.sale_type

    def material_types(self):
        return ", ".join(
            self.invoiceitems.values_list(
                "product__material_type", flat=True
            ).distinct()
        )

    def __str__(self):
        return self.invoice_number


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        related_name="invoiceitems",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    def save(self, *args, **kwargs):
        # ✅ Always keep total in sync
        self.total = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} x {self.quantity}"



    
class Target(models.Model):
    TARGET_TYPE_CHOICES = [
        ('value', 'Sales Value (₹)'),
        ('quantity', 'Quantity'),
    ]

    salesperson = models.ForeignKey(Salesperson, on_delete=models.CASCADE)
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField(default=now().year)

    target_type = models.CharField(
        max_length=20,
        choices=TARGET_TYPE_CHOICES
    )

    target_value = models.DecimalField(max_digits=12, decimal_places=2)

    product_category = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('salesperson', 'month', 'year')
        
    def __str__(self):
        return f"{self.salesperson.name} - {self.month}/{self.year}"

class WeeklyTarget(models.Model):
    target = models.ForeignKey(
        Target,
        related_name="weekly_targets",
        on_delete=models.CASCADE
    )

    week_number = models.PositiveIntegerField()  # 1–4
    target_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    target_quantity = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    class Meta:
        unique_together = ('target', 'week_number')

    def __str__(self):
        return f"{self.target} - Week {self.week_number}"

    
class MonthlySales(models.Model):
    salesperson = models.ForeignKey(Salesperson, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    month = models.DateField()

    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    achieved_amount = models.DecimalField(max_digits=12, decimal_places=2)

    client_meetings = models.IntegerField(default=0)
    working_days = models.IntegerField(default=22)

    def __str__(self):
        return f"{self.salesperson} - {self.month}"
    
class NextMonthPrediction(models.Model):
    salesperson = models.ForeignKey(Salesperson, on_delete=models.CASCADE)
    predicted_amount = models.FloatField()
    confidence = models.FloatField()
    based_on_months = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.salesperson} - {self.predicted_amount}"