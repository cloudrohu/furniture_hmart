from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/add/<int:id>/', views.ajax_add_to_cart, name='ajax_add_to_cart'),
    path('addtoshopcart/<int:id>/', views.addtoshopcart, name='addtoshopcart'),
    path('shopcart/', views.shopcart, name='shopcart'),
    path('deletefromcart/<int:id>/', views.deletefromcart, name='deletefromcart'),
    path('orderproduct/', views.orderproduct, name='orderproduct'),
]
