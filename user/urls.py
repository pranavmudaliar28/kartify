"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path("", views.Home),
                  path('Home', views.Home, name='Home'),
                  path('Termscondition', views.Termscondition, name='Termscondition'),
                  path('Returnpolicy', views.Returnpolicy, name='Returnpolicy'),
                  path('Contactus', views.Contactus, name='Contactus'),
                  path('Aboutus', views.Aboutus, name='Aboutus'),
                  path('Trackorder', views.Trackorder, name='Trackorder'),
                  path('Product_detail/<int:id>/', views.Product_detail, name='Product_detail'),
                  path('Shop', views.Shop, name='Shop'),
                  path('signin', views.signin, name='signin'),
                  path('login', views.login, name='login'),
                  path('logout', views.logout, name='logout'),
                  path('Subscribe', views.Subscribe, name='Subscribe'),
                  path('myprofile', views.myprofile, name='myprofile'),
                  path('Checkout', views.Checkout, name='Checkout'),
                  path("placeorder", views.placeorder, name='placeorder'),
                  path("order_payment", views.order_payment, name='order_payment'),
                  path("callback", views.callback, name='callback'),
                  path("yourorder", views.yourorder, name='yourorder'),
                  path("cart", views.cart, name='cart'),
                  path("faq", views.faq, name='faq'),
                  path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
                  path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
                  path('cart/item_increment/<int:id>/',
                       views.item_increment, name='item_increment'),
                  path('cart/item_decrement/<int:id>/',
                       views.item_decrement, name='item_decrement'),
                  path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
                  path('cart/cart-detail/', views.cart_detail, name='cart_detail'),
                  path('search/', views.search, name='search'),
                  path('review', views.review, name='review'),
                  path('password_reset', views.password_reset, name='password_reset'),
                  path('maincat/<int:id>/', views.maincat, name='maincat'),
                  path('cat/<int:id>', views.cat, name='cat'),
                  path('subcat/<int:id>', views.subcat, name='subcat'),
                  path('otp', views.otp, name='otp'),
                  path('password', views.password, name="password")
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
