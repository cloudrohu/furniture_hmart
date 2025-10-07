# user/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
import os
from .models import UserProfile

THUMBNAIL_SIZE = (300, 300)
MAX_SIZE_MB = 2

def get_file_size_mb(path):
    return os.path.getsize(path) / (1024 * 1024)

def compress_and_thumbnail(image_path):
    """Compress image to WebP and create thumbnail"""
    if not image_path or not os.path.exists(image_path):
        return None, None

    img = Image.open(image_path)
    img = img.convert('RGB')

    # Resize if file is too large
    if get_file_size_mb(image_path) > MAX_SIZE_MB:
        img.thumbnail((1600, 1600))  

    # Save as WebP
    webp_path = image_path.rsplit('.', 1)[0] + '.webp'
    img.save(webp_path, format='WEBP', quality=70)

    # Create thumbnail
    thumb_img = img.copy()
    thumb_img.thumbnail(THUMBNAIL_SIZE)
    thumb_path = image_path.rsplit('.', 1)[0] + '_thumb.webp'
    thumb_img.save(thumb_path, format='WEBP', quality=80)

    # Remove original
    os.remove(image_path)

    return webp_path, thumb_path

def process_image_field(instance, field_name):
    image_field = getattr(instance, field_name)
    if image_field and not str(image_field).endswith('.webp'):
        webp_path, thumb_path = compress_and_thumbnail(image_field.path)
        if webp_path:
            relative_webp_path = image_field.name.rsplit('.', 1)[0] + '.webp'
            setattr(instance, field_name, relative_webp_path)
            instance.save(update_fields=[field_name])

# ✅ UserProfile image compression
@receiver(post_save, sender=UserProfile)
def compress_user_profile_image(sender, instance, **kwargs):
    process_image_field(instance, 'image')
