from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.utils.html import mark_safe
# Create your models here.
from django.db.models import Avg, Count
from django.forms import ModelForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.db.models.signals import pre_save

from django.utils.text import slugify


class Brand(models.Model):
    title = models.CharField(max_length=250)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image=models.ImageField(blank=True,upload_to='images/')
    slug = models.SlugField(unique=True , null=True , blank=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self , *args , **kwargs):
        self.slug = slugify(self.title)
        super(Brand ,self).save(*args , **kwargs)

    def get_absolute_url(self):
        return reverse('brand_detail', kwargs={'slug': self.slug})
    
    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))



class Category(MPTTModel):
    # Status choices
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    # MPTT TreeForeignKey for self-referencing hierarchy
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE, )   
    title = models.CharField(max_length=250, unique=True) # Title ko unique kar dena accha practice hai
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS, default='True')
    featured_category = models.BooleanField(default=False)
    
    # Slug for clean URLs
    slug = models.SlugField(unique=True, null=True, blank=True)
    
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # --- Methods ---

    # Method to display image in Django Admin
    def image_tag(self):
        if self.image:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        return ""
    image_tag.short_description = 'Image Preview'
    
    # Overriding save method to auto-generate the slug
    def save(self, *args, **kwargs):
        if not self.slug: # Agar slug pehle se set nahi hai to generate karo
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)
    
    # Returns the absolute URL for the object
    def get_absolute_url(self):
        # Make sure you have a URL pattern named 'category_detail' defined in your urls.py
        try:
            return reverse('category_detail', kwargs={'slug': self.slug})
        except:
            return f"/category/{self.slug}" # Fallback if URL name not found

    # Custom __str__ method to show the full path (e.g., Furniture / Sofas / 2-Seater)
    def __str__(self): 
        full_path = [self.title] 
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        # The path is constructed backwards, so reverse it
        return ' / '.join(full_path[::-1])

    # --- MPTT Metadata ---
    class MPTTMeta:
        # MPTT uses this to order nodes at the same level
        order_insertion_by = ['title']
        
    # --- Django Metadata ---
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    PRODUCT_TYPE = (
        ('None', 'None'),
        ('New Arrivals', 'New Arrivals'),
        ('Top Rated', 'Top Rated'),
        ('Featured', 'Featured'),
    )

    AVAILABILITY_CHOICES = (
        ('In Stock', 'In Stock'),
        ('Out of Stock', 'Out of Stock'),
        ('Limited Stock', 'Limited Stock'),
        ('Pre Order', 'Pre Order'),
    )

    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),
    )
    type=models.CharField(max_length=25,choices=PRODUCT_TYPE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #many to one relation with Category
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE) #many to one relation with Brand
    title = models.CharField(max_length=250)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image=models.ImageField(upload_to='images/',null=False)
    price=models.IntegerField(default=0)
    discount=models.IntegerField(default=0)
    variant=models.CharField(max_length=10,choices=VARIANTS, default='None')
    availability=models.CharField(max_length=50,choices=AVAILABILITY_CHOICES, default='In Stock')
    detail=RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
    status=models.CharField(max_length=10,choices=STATUS)
    featured_project = models.BooleanField(default=False)
    best_seller = models.BooleanField(default=False)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    
    def get_final_price(self):
        """Return price after applying % discount."""
        try:
            if self.discount and self.discount > 0:
                return int(round(self.price - (self.price * self.discount / 100)))
        except Exception:
            pass
        return self.price


    ## method to create a fake table field in read only mode
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    def save(self , *args , **kwargs):
        self.slug = slugify(self.title)
        super(Product ,self).save(*args , **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'id': self.id, 'slug': self.slug})


    def avaregereview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(avarage=Avg('rate'))
        avg=0
        if reviews["avarage"] is not None:
            avg=float(reviews["avarage"])
        return avg

    def countreview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(count=Count('id'))
        cnt=0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt




class Specification(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=255)


    def __str__(self):
        return self.key



class Images(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title




class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250,blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status=models.CharField(max_length=10,choices=STATUS, default='New')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']


class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)
    def __str__(self):
        return self.name
    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""


class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)
    def __str__(self):
        return self.name

class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True,null=True)
    image_id = models.IntegerField(blank=True,null=True,default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)

    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             varimage=img.image.url
        else:
            varimage=""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""

class Showroom(models.Model):
    city_name = models.CharField(max_length=100)
    store_count = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='showrooms/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower number = first)")

    class Meta:
        ordering = ['order', 'city_name']


class ModularKitchen(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='modular_kitchen/')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower number = first)")

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Modular Kitchen"
        verbose_name_plural = "Modular Kitchens"

    def __str__(self):
        return self.title
    


class TopProductOfWeek(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='top_products/')
    description = models.TextField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.PositiveIntegerField(default=0)
    feature_1 = models.CharField(max_length=255, blank=True, null=True)
    feature_2 = models.CharField(max_length=255, blank=True, null=True)
    feature_3 = models.CharField(max_length=255, blank=True, null=True)
    feature_4 = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @property
    def discounted_price(self):
        if self.discount_percent > 0:
            return round(self.original_price - (self.original_price * self.discount_percent / 100))
        return round(self.original_price)
    


