from django.contrib import admin
from .models import Category, SideMenu, SubSideMenu, Brand, Product, Reviews, Order, OrderItem, Slider, Banner, ProductImage, KeyFeature, Specification, SpecTable

# Register your models here.
@admin.register(Category)
class categoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


@admin.register(Brand)
class brandAdmin1(admin.ModelAdmin):
    list_display = ['id', 'title']


@admin.register(Banner)
class bannerAdmin1(admin.ModelAdmin):
    list_display = ['id', 'title']


@admin.register(ProductImage)
class productImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product']


admin.site.register(KeyFeature)
admin.site.register(SpecTable)
admin.site.register(Specification)
admin.site.register(SideMenu)
admin.site.register(SubSideMenu)


@admin.register(Product)
class productAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_stock', 'featured', 'offered']


@admin.register(Reviews)
class reviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'product']


@admin.register(Slider)
class sliderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'category']



@admin.register(Order)
class orderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total', 'date']


@admin.register(OrderItem)
class orderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'price']