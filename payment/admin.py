from django.contrib import admin
from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'payment_date', 'payment_amount','payment_parking_slot', 'payment_complete')
    list_filter = ('payment_date', 'payment_complete')
    ordering = ('-payment_date',)
    readonly_fields = ('payment_date',)


admin.site.register(Payment, PaymentAdmin)
