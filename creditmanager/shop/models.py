from django.db import models
from django.utils import timezone


class Customer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    @property
    def total_due(self):
        """Total purchases - total payments"""
        purchases = sum(e.amount for e in self.entries.filter(is_payment=False))
        payments = sum(e.amount for e in self.entries.filter(is_payment=True))
        return purchases - payments

    @property
    def last_entry_date(self):
        last_entry = self.entries.order_by("-date").first()
        return last_entry.date if last_entry else None

    def __str__(self):
        return self.name


class Entry(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="entries")
    goods = models.CharField(max_length=255, blank=True, null=True)  # optional for payments
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_payment = models.BooleanField(default=False)  # True if it's a payment
    remarks = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        kind = "Payment" if self.is_payment else "Purchase"
        return f"{self.customer.name} - {kind} {self.amount}"
