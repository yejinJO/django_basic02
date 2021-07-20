from .models import Order
from django.contrib import admin

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('fcuser', 'product')

admin.site.register(Order, OrderAdmin)