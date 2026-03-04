from django.contrib import admin
from .models import (
    Customer,
    Salesperson,
    Product,
    Sale,
    Invoice,
    InvoiceItem,
    Target
)

# ================= CUSTOMER =================
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'business_name',
        'contact_person',
        'customer_type',   # ✅ FIXED
        'credit_limit',
        'status',
    )

    list_filter = (
        'status',
        'customer_type',   # ✅ FIXED
    )

    search_fields = (
        'business_name',
        'contact_person',
        'location',
    )


# ================= SALESPERSON =================
from django.contrib import admin
from .models import Salesperson

@admin.register(Salesperson)
class SalespersonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "region",
        "product_category",
        "status",
        "join_date",
    )
    search_fields = ("name", "email", "phone")
    list_filter = ("region", "status", "product_category")



# ================= PRODUCT =================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "material_display",
        "category_badge",
        "unit_display",
        "price_per_unit",
        "status_colored",
    )

    list_filter = (
        "material_type",
        "category",
        "status",
    )

    search_fields = ("name",)
    ordering = ("id",)

    # ✅ READABLE MATERIAL
    @admin.display(description="Material")
    def material_display(self, obj):
        return obj.get_material_type_display()

    # ✅ READABLE UNIT
    @admin.display(description="Unit")
    def unit_display(self, obj):
        return obj.get_unit_type_display()

    # ✅ STATUS COLOR
    @admin.display(description="Status")
    def status_colored(self, obj):
        if obj.status:
            return "🟢 Active"
        return "🔴 Inactive"

    # ✅ CATEGORY BADGE STYLE
    @admin.display(description="Category")
    def category_badge(self, obj):
        return obj.category


# ================= SALE =================
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_no",
        "customer",
        "salesperson",
        "product",
        "quantity",
        "price_per_unit",
        "total_amount",
        "sale_date",
        "status",
    )
    list_filter = ("sale_date", "status")
    search_fields = ("invoice_no",)


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    fields = ("product", "quantity", "price", "total")
    readonly_fields = ("total",)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_no",
        "date",
        "salesperson",
        "customer",
        "get_type",
        "grand_total",
    )

    def get_type(self, obj):
        return obj.get_invoice_type_display()
    get_type.short_description = "Type"

# ================= TARGET =================
@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = (
        "salesperson",
        "month",
        "year",
        "target_type",
        "target_value",
        "product_category",
    )
    list_filter = ("year", "target_type")





# ================= INVOICE ADMIN =================
