from django.contrib import admin

from . models import Category,Products,Cart,CartProduct,Order

admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)