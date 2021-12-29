from django.contrib import admin
from django.contrib.admin import TabularInline, ModelAdmin

from commerce.models import (
    Product,
    Category,
    Item, ProductImage
)



class InlineproductImage(admin.TabularInline):
        model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [InlineproductImage]
    list_display = ['id', 'name', 'qty', 'size', 'description', 'cost', 'price', 'discounted_price']
    list_filter = ['category']
    search_fields = ['name', 'qty', 'description', 'cost', 'price', 'discounted_price']


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['category']
    list_display = ['id', 'name', 'description' ,'created','image']


class ItemAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'product', 'item_qty', 'ordered',]

'''
class ProductImageAdmin(admin.ModelAdmin):
     list_display = ['product','is_default_image','image']

'''
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item,ItemAdmin)
admin.site.register(ProductImage)
