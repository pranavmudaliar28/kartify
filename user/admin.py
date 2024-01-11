from django.contrib import admin
from .models import *

# Register your models here.
class Product_Images(admin.TabularInline):
    model = Product_Image

class product_images(admin.ModelAdmin):
    list_display = ['id', 'admin_photo']
    readonly_fields = [ "admin_photo"]


class Additional_informations(admin.TabularInline):
    model = Additional_information

class Product_Admin(admin.ModelAdmin):
    inlines = (Product_Images, Additional_informations)
    list_display = ["id","admin_photo","product_name","main_catgories", "catergories","sub_catergories","price", "Discount" ,"Availablity","total_quantity","date"]
    list_display_links = ['product_name']
    list_editable = [ "main_catgories","catergories","sub_catergories", "price", "Discount", "Availablity", "total_quantity"]
    readonly_fields = ['date',"admin_photo"]
    list_filter = ['product_name','price','Discount','date']

class order_placed(admin.ModelAdmin):
    list_display = ["id",'admin_photo','user','product','price','total','quantity','address','phonenumber','date']
    list_filter = ['date',"price"]
    readonly_fields = ['admin_photo']

class Main_category(admin.ModelAdmin):
    list_display = ['id','name']
    list_editable = ['name']
    list_filter = ['name']

class category(admin.ModelAdmin):
    list_display = ['id',"maincatgory",'name']
    list_editable = ['name',"maincatgory"]
    list_filter = ['name']

class sub_category(admin.ModelAdmin):
    list_display = ['id',"category",'name']
    list_editable = ['name',"category"]
    list_filter = ['name']

class Slider(admin.ModelAdmin):
    list_display = ['id',"admin_photo", "Discount_Deal", 'Product_Name','SALE',"Discount",'Link']
    list_editable = [ "Discount_Deal",  'Product_Name','SALE',"Discount",'Link']
    list_filter = ["Discount_Deal",'SALE',"Discount"]
    readonly_fields = ['admin_photo']

class User(admin.ModelAdmin):
    list_display = ["id", "uname", "email","phonenumber", "password" ,"addresss"]
    list_filter = ["uname", "email","phonenumber", "password" ,"addresss"]

class Banner(admin.ModelAdmin):
    list_display = ["id", "admin_photo", "Discount_Deal","Quote", "Discount" ,"Link"]
    list_filter = ["Discount_Deal","Quote", "Discount" ,"Link"]
    readonly_fields = ['admin_photo']


class Teammember(admin.ModelAdmin):
    list_display = ["id", "admin_photo", "name", "designation", "facebook", "twitter","linkedin"]
    list_editable = [ "name", "designation", "facebook", "twitter","linkedin"]
    list_filter = [ "name", "designation"]
    readonly_fields = ['admin_photo']

class State(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_editable = ['name']
    list_filter = ['name']

class City(admin.ModelAdmin):
    list_display = ['id','state', 'name']
    list_editable = ['name','state']
    list_filter = ['name','state']

class Pincode(admin.ModelAdmin):
    list_display = ['id', 'city','areaname','pincodeno']
    list_editable = ['city','areaname','pincodeno']
    list_filter = ['city','areaname','pincodeno']

class Subscribe(admin.ModelAdmin):
    list_display = ['id','user','email1']

class Contactus(admin.ModelAdmin):
    list_display = ['id', 'user','uname' ,'email','subject','message']


admin.site.register(slider,Slider)
admin.site.register(banner,Banner)
admin.site.register(main_catgory,Main_category)
admin.site.register(Category,category)
admin.site.register(Sub_Category,sub_category)
admin.site.register(teammember,Teammember)
admin.site.register(Product,Product_Admin)
admin.site.register(Product_Image,product_images)
admin.site.register(Additional_information)
admin.site.register(Order)
admin.site.register(user,User)
admin.site.register(state,State)
admin.site.register(city,City)
admin.site.register(pincode,Pincode)
admin.site.register(checkout,order_placed)
admin.site.register(subscribe,Subscribe)
admin.site.register(contactus,Contactus)
admin.site.register(Review)
admin.site.register(coupon_code)

