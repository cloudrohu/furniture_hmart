from django.contrib import admin
import admin_thumbnails


from .models import *
# Register your models here.

class SettingtAdmin(admin.ModelAdmin):
    list_display = ['title','company', 'update_at','status']

@admin_thumbnails.thumbnail('image')
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title','image','featured_project', 'create_at','update_at']

@admin_thumbnails.thumbnail('image')
class OfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'update_at','create_at']


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name','subject', 'update_at','status','note','message','email','ip',]
    list_editable = ['status','note']
    readonly_fields =('name','subject','email','message','ip')
    list_filter = ['status']

class ShowroomAdmin(admin.ModelAdmin):
    list_display = ('city_name', 'store_count', 'is_active', 'order')
    list_editable = ('store_count', 'is_active', 'order')
    search_fields = ('city_name',)
    list_filter = ('is_active',)
    ordering = ('order',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'rating', 'is_active', 'created_at')
    list_editable = ('is_active', 'rating')
    search_fields = ('name', 'designation', 'message')
    list_filter = ('is_active', 'rating')
    ordering = ('-created_at',)

@admin.register(CustomerSupport)
class CustomerSupportAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'email', 'chat_status', 'opening_time', 'closing_time', 'updated_at']


admin.site.register(Setting,SettingtAdmin)
admin.site.register(Showroom,ShowroomAdmin)
admin.site.register(ContactMessage,ContactMessageAdmin)
admin.site.register(Offer,OfferAdmin)
admin.site.register(Slider,SliderAdmin)
admin.site.register(Banner,)