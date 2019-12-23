from django.contrib import admin

# Register your models here.

from .models import Product, Category, Partner
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget


class ProductResource(resources.ModelResource):

    category = fields.Field(
        column_name='category',
        attribute='category',
        readonly=False,
        widget=ForeignKeyWidget(Category, 'name')
    )

    partner = fields.Field(
        column_name='partner',
        attribute='partner',
        readonly=False,
        widget=ForeignKeyWidget(Partner, 'name')
    )

    class Meta:
        model = Product
        exclude = ('created', 'modified')
        fields = (
            'id', 'name', 'slug', 'bar_code', 'category', 'short_description',
            'description', 'price', 'published', 'stock', 'partner', 'image'
        )


class PartnerAdmin(admin.ModelAdmin):

    list_display = ['name', 'slug', 'phone', 'email', 'site', 'created', 'modified']
    search_fields = ['name', 'slug']


class CategoryAdmin(admin.ModelAdmin):

    list_display = ['name', 'slug', 'created', 'modified']
    search_fields = ['name', 'slug']


class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    list_display = ['name', 'slug', 'category', 'price', 'stock', 'created', 'modified', 'published', 'partner']
    search_fields = ['name', 'slug', 'category__name']
    list_filter = ['created', 'modified']

    resource_class = ProductResource


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Partner, PartnerAdmin)
