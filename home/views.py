import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q, F
from django.db.models.functions import Concat
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import translation

from home.forms import SearchForm
from home.models import Setting, CustomerSupport, ContactForm, ContactMessage,FAQ, Testimonial, Showroom,Slider,Offer,Banner
from furniture_hmart import settings
from product.models import Category, Specification, TopProductOfWeek, Product, Images, Comment, Variants,Brand,ModularKitchen
from user.models import UserProfile
# Create your views here.


def index(request):
    setting = Setting.objects.all().order_by('-id')[:1]
    support_info = CustomerSupport.objects.first()
    category = Category.objects.all()
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-created_at')[:100]
    offer = Offer.objects.filter(featured_project = 'True').order_by('id')[:2]  #first 4 products
    featured_category = Category.objects.filter(featured_category = 'True').order_by('id')[:3]  #first 4 products
    slider = Slider.objects.filter(featured_project = 'True').order_by('id')[0:6]  #first 4 products
    banner = Banner.objects.filter(featured_project = 'True').order_by('id')[0:2] 
    showrooms = Showroom.objects.filter(is_active=True).order_by('order', 'city_name')
    brand = Brand.objects.all().order_by('?')[0:20]  #first 4 products
    products_slider = Product.objects.all().order_by('id')[:4]  #first 4 products
    products_latest = Product.objects.all().order_by('-id')[:8]  # last 4 products
    featured_project = Product.objects.filter(featured_project = 'True').order_by('-id')[:12]  # last 4 products
    New_Arrivals = Product.objects.filter(type = 'New Arrivals').order_by('-id')[:8]  # last 4 products
    Top_Rated = Product.objects.filter(type = 'Top Rated').order_by('-id')[:8]  # last 4 products
    featured = Product.objects.filter(type = 'Featured').order_by('-id')[:8]  # last 4 products
    best_sellers = Product.objects.filter(best_seller=True, status='True').order_by('-id')[:8]
    products_picked = Product.objects.all().order_by('?')[:8]   #Random selected 4 products
    top_product = TopProductOfWeek.objects.filter(is_active=True).first()
    modular_kitchens = ModularKitchen.objects.filter(is_active=True).order_by('order', 'title')[0:6]
    page="home"
    context={
        'support_info': support_info,
        'testimonials': testimonials,
        'top_product': top_product,
        'showrooms': showrooms,
        'brand':brand,
        'banner':banner,
        'offer':offer,
        'modular_kitchens': modular_kitchens,
        'slider':slider,
        'setting':setting,
        'category':category,
        'page':page,
        'products_picked':products_picked,
        'products_slider':products_slider,
        'products_latest':products_latest,
        'featured_project':featured_project,
        'featured_category':featured_category,
        'New_Arrivals':New_Arrivals,
        'Top_Rated':Top_Rated,
        'featured':featured,
        'best_sellers': best_sellers,
    }

    return render(request,'index.html',context)

def SERVICES(request):
    #category = categoryTree(0,'',currentlang)
    setting = Setting.objects.all().order_by('-id')[:1]
    category = Category.objects.all()    
    context={
        'setting':setting,
        'category':category
    } 
    return render(request, 'service.html',context)

def furniture(request):
    #category = categoryTree(0,'',currentlang)
    setting = Setting.objects.all().order_by('-id')[:1]
    category = Category.objects.all()    
    context={
        'setting':setting,
        'category':category
    } 
    return render(request, 'furniture.html',context)


def aboutus(request):
    #category = categoryTree(0,'',currentlang)
    setting = Setting.objects.all().order_by('-id')[:1]

    category = Category.objects.all()

    
    context={
        'setting':setting,
        'category':category
    }
 
    return render(request, 'about.html',context)

def contactus(request):
    setting = Setting.objects.all().order_by('-id')[:1]

    category = Category.objects.all()

    if request.method == 'POST': # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage() #create relation with model
            data.name = form.cleaned_data['name'] # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  #save data to table
            messages.success(request,"Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')
    form = ContactForm
    context={
        'setting':setting,
        'form':form ,
        'category':category,
    }    
    return render(request, 'contactus.html',context)

def category_products(request,id,slug):
    setting = Setting.objects.all().order_by('-id')[:1]
    
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id) #default language
    
    context={'products': products,
             'setting':setting,
             #'category':category,
             'category':category }
    return render(request,'category_products.html',context)


def search(request):
    setting = Setting.objects.all().order_by('-id')[:1]

    if request.method == 'POST': # check post
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query'] # get form input data
            catid = form.cleaned_data['catid']
            if catid==0:
                products=Product.objects.filter(title__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(title__icontains=query,category_id=catid)

            category = Category.objects.all()
            context = {'products': products,
                        'query':query,
                       'category': category,
                       'setting': setting,

                         }
            return render(request, 'search_products.html', context)

    return HttpResponseRedirect('/')


def search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(title__icontains=q)

        results = []
        for rs in products:
            product_json = {}
            product_json = rs.title +" > " + rs.category.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def product_detail(request, id, slug):

    
    setting = Setting.objects.all().order_by('-id')[:1]

    category = Category.objects.all()

    product = get_object_or_404(Product, pk=id, slug=slug)

    specifications = Specification.objects.filter(product=product)


    images = Images.objects.filter(product_id=id)

    comments = Comment.objects.filter(product_id=id, status='True')

    related_products = Product.objects.filter(category=product.category, status='True').exclude(id=product.id)[:4]

    if product.variant != "None":
        if request.method == 'POST':
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id)
            colors = Variants.objects.filter(product_id=id, size_id=variant.size_id)
            sizes = Variants.objects.raw(
                'SELECT * FROM product_variants WHERE product_id=%s GROUP BY size_id', [id]
            )
        else:
            variants = Variants.objects.filter(product_id=id)
            if variants.exists():
                variant = variants.first()
                colors = Variants.objects.filter(product_id=id, size_id=variant.size_id)
                sizes = Variants.objects.raw(
                    'SELECT * FROM product_variants WHERE product_id=%s GROUP BY size_id', [id]
                )
            else:
                variant = None
                colors = []
                sizes = []

    else:
        variant = None
        colors = []
        sizes = []

    average_rating = product.avaregereview()
    total_reviews = product.countreview()

    context = {
        'setting': setting,
        'category': category,
        'product': product,
        'images': images,
        'comments': comments,
        'related_products': related_products,
        'variant': variant,
        'colors': colors,
        'specifications': specifications,
        'sizes': sizes,
        'average_rating': average_rating,
        'total_reviews': total_reviews,
    }

    return render(request, 'product_detail.html', context)




def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


def faq(request):
   
    return render(request, 'faq.html')



def All_Product(request):
    setting = Setting.objects.all().order_by('-id')[:1]
    category = Category.objects.all()
    offer = Offer.objects.filter(featured_project = 'True').order_by('id')[:2]  #first 4 products
    featured_category = Category.objects.filter(featured_category = 'True').order_by('id')[:3]  #first 4 products
    slider = Slider.objects.filter(featured_project = 'True').order_by('id')[0:6]  #first 4 products
    banner = Banner.objects.filter(featured_project = 'True').order_by('id')[0:2]  #first 4 products
    brand = Brand.objects.all().order_by('?')[0:20]  #first 4 products
    products_slider = Product.objects.all().order_by('id')[:4]  #first 4 products
    products_latest = Product.objects.all().order_by('-id')[:8]  # last 4 products
    featured_project = Product.objects.filter(featured_project = 'True').order_by('-id')[:12]  # last 4 products
    New_Arrivals = Product.objects.filter(type = 'New Arrivals').order_by('-id')[:8]  # last 4 products
    Top_Rated = Product.objects.filter(type = 'Top Rated').order_by('-id')[:8]  # last 4 products
    featured = Product.objects.filter(type = 'Featured').order_by('-id')[:8]  # last 4 products
    products_picked = Product.objects.all().order_by('?')[:8]   #Random selected 4 products
    page="home"
    context={
        'brand':brand,
        'banner':banner,
        'offer':offer,
        'slider':slider,
        'setting':setting,
        'category':category,
        'page':page,
        'products_picked':products_picked,
        'products_slider':products_slider,
        'products_latest':products_latest,
        'featured_project':featured_project,
        'featured_category':featured_category,
        'New_Arrivals':New_Arrivals,
        'Top_Rated':Top_Rated,
        'featured':featured,
    }

    return render(request,'all_product.html',context)
