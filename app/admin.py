from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import User, ProductCategory, Product, ProductImage


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'id')
    list_filter = ('name_en',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ['image_tag']

@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ('name_en', 'price', 'sold', 'sale', 'new', 'id')
    list_filter =  ('name_en', 'price', 'sold', 'sale', 'new')
    inlines = [ProductImageInline]
    readonly_fields = ['image_tag']