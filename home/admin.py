from django.contrib import admin
import admin_thumbnails
from .models import (
    Setting,
    ContactMessage,
    Offer,
    Slider,
    Banner,
    Showroom,
    Testimonial,
    CustomerSupport
)


# 🧾 Setting Admin (multiple images → no thumbnail decorator)
class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'status', 'update_at']
    readonly_fields = ['create_at', 'update_at']


# 🖼 Slider Admin — thumbnail
@admin_thumbnails.thumbnail('image')
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_thumbnail', 'featured_project', 'create_at', 'update_at']
    readonly_fields = ()  # ⚡ Fix for admin_thumbnails bug


# 🏷 Offer Admin — thumbnail
@admin_thumbnails.thumbnail('image')
class OfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_thumbnail', 'create_at', 'update_at']
    readonly_fields = ()  # ⚡


# 🖼 Banner Admin — thumbnail
@admin_thumbnails.thumbnail('image')
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_thumbnail', 'featured_project', 'create_at', 'update_at']
    readonly_fields = ()  # ⚡


# 📬 Contact Message Admin
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'email', 'status', 'note', 'ip', 'update_at']
    list_editable = ['status', 'note']
    readonly_fields = ('name', 'subject', 'email', 'message', 'ip')
    list_filter = ['status']
    search_fields = ['name', 'email', 'subject']


# 🏢 Showroom Admin — thumbnail
@admin_thumbnails.thumbnail('image')
class ShowroomAdmin(admin.ModelAdmin):
    list_display = ('city_name', 'image_thumbnail', 'store_count', 'is_active', 'order')
    list_editable = ('store_count', 'is_active', 'order')
    search_fields = ('city_name',)
    list_filter = ('is_active',)
    ordering = ('order',)
    readonly_fields = ()  # ⚡


# 🧍 Testimonial Admin — thumbnail
@admin_thumbnails.thumbnail('image')
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_thumbnail', 'designation', 'rating', 'is_active', 'created_at')
    list_editable = ('is_active', 'rating')
    search_fields = ('name', 'designation', 'message')
    list_filter = ('is_active', 'rating')
    ordering = ('-created_at',)
    readonly_fields = ()  # ⚡


# 🧰 Customer Support Admin
@admin.register(CustomerSupport)
class CustomerSupportAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'email', 'chat_status', 'opening_time', 'closing_time', 'updated_at']
    list_editable = ['chat_status']


# ✅ Final Registrations
admin.site.register(Setting, SettingAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Showroom, ShowroomAdmin)
