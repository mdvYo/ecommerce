from django.contrib import admin

from apps.sellers.models import Seller


# Register your models here.


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['user', 'business_name', 'business_description', 'is_approved']
    list_editable = ['is_approved']

