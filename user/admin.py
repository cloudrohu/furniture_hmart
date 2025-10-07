from django.contrib import admin
import admin_thumbnails
from user.models import UserProfile


@admin_thumbnails.thumbnail('image')
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'image_thumbnail', 'address', 'phone', 'city', 'country']
    readonly_fields = ()  # ⚡ thumbnail decorator ke liye zaroori

admin.site.register(UserProfile, UserProfileAdmin)
