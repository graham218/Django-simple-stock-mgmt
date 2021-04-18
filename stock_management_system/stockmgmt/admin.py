from django.contrib import admin
from .models import *
from .forms import *

# Register your models here.
class StockCreateAdmin(admin.ModelAdmin):
   list_display = ['category', 'item_name', 'quantity']
   form = StockCreateForm
   list_filter = ['category']
   search_fields = ['category', 'item_name']

class CustomerDetailsAdmin(admin.ModelAdmin):
   form=CustomerDetailsForm
   list_display=['customer_name','national_id','email','phone_number','home_address']
   search_fields=['customer_name','national_id']
   list_filter=['customer_name']


admin.site.register(Stock,StockCreateAdmin)
admin.site.register(Category)
admin.site.register(CustomerDetails,CustomerDetailsAdmin)