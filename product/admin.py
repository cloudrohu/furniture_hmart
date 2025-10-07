import admin_thumbnails
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from product.models import (
    Category,
    ModularKitchen,
    Specification,
    TopProductOfWeek,
    Product,
    Images,
    Comment,
    Color,
    Size,
    Variants,
    Brand
)


# 🖼 Product Image Inline Thumbnail
@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1
    list_display = ['id', 'image_thumbnail']


# 🧩 Product Variants Inline
class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True


# 📑 Product Specification Inline
class SpecificationInline(admin.TabularInline):
    model = Specification
    fields = ('key', 'value')
    extra = 1
    show_change_link = True


# 🗂 Category Admin with Thumbnails
@admin_thumbnails.thumbnail('image')
class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = (
        'id',
        'tree_actions',
        'indented_title',
        'image_thumbnail',
        'related_products_count',
        'related_products_cumulative_count',
    )
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ()  # ⚡ required for admin_thumbnails

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_cumulative_count',
            cumulative=True
        )
        qs = Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_count',
            cumulative=False
        )
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'


# 🖼 Images Admin
@admin_thumbnails.thumbnail('image')
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'image_thumbnail']
    readonly_fields = ()  # ⚡


# 🧾 Product Admin
@admin_thumbnails.thumbnail('image')
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_thumbnail', 'category', 'price', 'discount', 'featured_project', 'brand', 'status', 'slug']
    list_filter = ['category']
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline, ProductVariantsInline, SpecificationInline]
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ()  # ⚡


# 💬 Comment Admin
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'comment', 'product', 'status', 'create_at', 'rate', 'ip']
    list_filter = ['status']
    list_editable = ['status']
    readonly_fields = ('subject', 'comment', 'ip', 'user', 'product', 'rate', 'id')


# 🌈 Color Admin
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'color_tag']


# 📏 Size Admin
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']


# 🧬 Variants Admin
class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'color', 'size', 'price', 'quantity', 'image_tag']


# 🧰 Modular Kitchen Admin
@admin_thumbnails.thumbnail('image')
class ModularKitchenAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_thumbnail', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('title',)
    list_filter = ('is_active',)
    ordering = ('order',)
    readonly_fields = ()  # ⚡


# 🏆 Top Product of the Week Admin
@admin_thumbnails.thumbnail('image')
@admin.register(TopProductOfWeek)
class TopProductOfWeekAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_thumbnail', 'original_price', 'discount_percent', 'discounted_price', 'is_active')
    readonly_fields = ('discounted_price',)
    readonly_fields = ()  # ⚡


# 📑 Specification Admin
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'key', 'value')


# ✅ Register all models
admin.site.register(Specification, SpecificationAdmin)
admin.site.register(Category, CategoryAdmin2)
admin.site.register(ModularKitchen, ModularKitchenAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Brand)
admin.site.register(Variants, VariantsAdmin)
