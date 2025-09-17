from django.contrib import admin
from .models import Customer, Entry

class EntryInline(admin.TabularInline):
    model = Entry
    extra = 1

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "total_due", "last_entry_date", "created_at")
    inlines = [EntryInline]

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("customer", "goods", "amount", "remarks", "date")
    list_filter = ("date", "customer")
    search_fields = ("goods", "remarks", "customer__name")
