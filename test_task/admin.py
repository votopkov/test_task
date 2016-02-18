from django.contrib import admin
from models import Product


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'modified_at', )

admin.site.register(Product, ProductAdmin)
