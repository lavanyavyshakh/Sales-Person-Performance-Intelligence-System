from django import forms
from django.forms import inlineformset_factory
from decimal import Decimal
from django.utils.timezone import now
from .models import (
    Customer,
    Salesperson,
    Product,
    Sale,
    Invoice,
    InvoiceItem,
    Target
)

class CustomerForm(forms.ModelForm):

    STATUS_CHOICES = (
        (True, 'Active'),
        (False, 'Inactive'),
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select()
    )

    class Meta:
        model = Customer
        fields = [
            'business_name',
            'contact_person',
            'phone',
            'email',
            'location',
            'customer_type',
            'credit_limit',
            'status',
        ]
        labels = {
            'business_name': 'Business Name',
            'contact_person': 'Customer Name',
            'phone': 'Phone Number',
            'email': 'Email',
            'location': 'Location',
            'customer_type': 'Customer Type',
            'credit_limit': 'Credit Limit (₹)',
            'status': 'Status',
        }


from django import forms
from .models import Salesperson

class SalespersonForm(forms.ModelForm):

    STATUS_CHOICES = (
        (True, "Active"),
        (False, "Inactive"),
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select()
    )

    class Meta:
        model = Salesperson
        fields = [
            "name",
            "region",
            "product_category",
            "phone",
            "email",
            "status",
        ]
        labels = {
            "name": "Salesperson Name",
            "region": "Region / Territory",
            "product_category": "Product Category",
            "phone": "Phone Number",
            "email": "Email Address",
            "status": "Status",
        }



    def clean_employee_id(self):
        emp_id = self.cleaned_data["employee_id"]
        if Salesperson.objects.filter(employee_id=emp_id).exists():
            raise forms.ValidationError(
                "Employee ID already exists. Please use a unique ID."
            )
        return emp_id


from django import forms
from .models import Product

class ProductForm(forms.ModelForm):

    MATERIAL_UNIT_MAP = {
        'cotton': ['meter', 'piece'],
        'yarn': ['kg', 'meter'],
        'wool': ['kg'],
        'silk': ['meter', 'piece'],
        'polyester': ['meter'],
        'nylon': ['meter'],
    }

    class Meta:
        model = Product
        fields = [
            "name",
            "material_type",
            "category",
            "unit_type",
            "price_per_unit",
            "status",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),

            "material_type": forms.Select(
                choices=Product.MATERIAL_CHOICES,
                attrs={"class": "form-control", "id": "id_material_type"}
            ),

            "category": forms.TextInput(attrs={"class": "form-control"}),

            "unit_type": forms.Select(
                choices=Product.UNIT_CHOICES,
                attrs={"class": "form-control", "id": "id_unit_type"}
            ),

            "price_per_unit": forms.NumberInput(attrs={"class": "form-control"}),

            "status": forms.Select(
                choices=[(True, "Active"), (False, "Inactive")],
                attrs={"class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        material = None

        # edit form
        if self.instance and self.instance.pk:
            material = self.instance.material_type

        # add form (POST)
        if self.data.get("material_type"):
            material = self.data.get("material_type")

        if material in self.MATERIAL_UNIT_MAP:
            allowed_units = self.MATERIAL_UNIT_MAP[material]
            self.fields["unit_type"].choices = [
                (key, label)
                for key, label in Product.UNIT_CHOICES
                if key in allowed_units
            ]


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = [
            "invoice_no",
            "customer",
            "salesperson",
            "product",
            "quantity",
            "price_per_unit",
            "sale_date",
            "status",
        ]

from django import forms
from django.forms import inlineformset_factory
from django.utils.timezone import now

from myapp.models import Invoice, InvoiceItem


# =====================================================
# INVOICE FORM
# =====================================================
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            "invoice_number",
            "sale_date",
            "sale_type",
            "salesperson",
            "customer",
            "remarks",
        ]

        labels = {
            "invoice_number": "Invoice No",
            "sale_date": "Sale Date",
            "sale_type": "Invoice Type",
            "remarks": "Remarks",
        }

        widgets = {
            "invoice_number": forms.TextInput(attrs={
                "class": "form-control",
                "readonly": "readonly"  # 🔒 prevent user editing
            }),
            "sale_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "sale_type": forms.Select(attrs={
                "class": "form-control"
            }),
            "salesperson": forms.Select(attrs={
                "class": "form-control"
            }),
            "customer": forms.Select(attrs={
                "class": "form-control"
            }),
            "remarks": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Enter remarks..."
            }),
        }

    # ✅ ensure default date if frontend fails
    def clean_sale_date(self):
        return self.cleaned_data.get("sale_date") or now().date()


# =====================================================
# INVOICE ITEM FORM
# =====================================================
class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ["product", "quantity", "price"]

        widgets = {
            "product": forms.Select(attrs={
                "class": "form-control product-select"
            }),
            "quantity": forms.NumberInput(attrs={
                "class": "form-control qty-input",
                "min": 1
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control price-input",
                "step": "0.01",
                "readonly": "readonly"
            }),
        }

    # ✅ backend safety
    def clean_quantity(self):
        qty = self.cleaned_data.get("quantity", 0)
        if qty <= 0:
            raise forms.ValidationError("Quantity must be greater than zero")
        return qty


# =====================================================
# FORMSET
# =====================================================
InvoiceItemFormSet = inlineformset_factory(
    Invoice,
    InvoiceItem,
    form=InvoiceItemForm,
    extra=1,
    can_delete=True
)



class TargetForm(forms.ModelForm):
    class Meta:
        model = Target
        fields = [
            "salesperson",
            "month",
            "year",
            "target_type",
            "target_value",
            "product_category",
        ]

