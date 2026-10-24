from django.contrib import admin
from .models import Category, Product, Order, OrderItem

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=["name","slug"]
    prepopulated_fields ={"slug":("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title","category","price","stock","is_active"]
    list_filter = ["category","is_active"]
    search_fields = ["title","brand"]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra=0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "status","total","created_at"]
    list_filter = ["status"]
    inlines = [OrderItemInline]

