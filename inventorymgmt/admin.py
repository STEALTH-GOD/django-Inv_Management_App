from django.contrib import admin
from .forms import StockCreateForm
from .models import Stock
# Register your models here.

class StockAdminForm(admin.ModelAdmin):
    form = StockCreateForm
    list_display = ['item_name', 'quantity', 'category', 'brand', 'price']
    search_fields = ['item_name', 'category', 'brand']
    list_filter = ['category',  'brand',]


admin.site.register(Stock, StockAdminForm)