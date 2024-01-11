from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus
from django.utils.safestring import mark_safe
import datetime



# Create your models here.


class slider(models.Model):
    DISCOUNT_DEAL =(
        ('HOT DEALS', "HOT DEALS"),
        ("NEW ARRIVALS", "NEW ARRIVALS")
    )
    Image = models.ImageField(upload_to='slider/')
    Discount_Deal = models.CharField(choices=DISCOUNT_DEAL, max_length=100)
    SALE = models.IntegerField()
    Product_Name = models.CharField(max_length=200)
    Discount = models.IntegerField()
    Link = models.CharField(max_length=200)

    def admin_photo(self):
        return mark_safe('<img src="{}" width="100" />'.format(self.Image.url))

    admin_photo.short_description = "Slider Image"
    admin_photo.allow_tags = True

    def __str__(self):
        return self.Product_Name


class banner(models.Model):
    image = models.ImageField(upload_to='banner/')
    Discount_Deal = models.CharField( max_length=100)
    Quote = models.CharField(max_length=100)
    Discount = models.IntegerField()
    Link = models.CharField(max_length=200, null=True)

    def admin_photo(self):
        return mark_safe('<img src="{}" width="100" />'.format(self.image.url))

    admin_photo.short_description = "Banner Image"
    admin_photo.allow_tags = True

    def __str__(self):
        return self.Quote


class main_catgory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    maincatgory = models.ForeignKey(main_catgory, on_delete=models.CASCADE)
    name =models.CharField(max_length=100)


    def __str__(self):
        return self.maincatgory.name + "--" + self.name


class Sub_Category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.category.maincatgory.name + " -- " + self.category.name + " -- " + self.name

class teammember(models.Model):
    name = models.CharField(max_length=30)
    designation = models.CharField(max_length=30)
    facebook = models.URLField(max_length=200)
    twitter = models.URLField(max_length=200)
    linkedin = models.URLField(max_length=200)
    img = models.ImageField(upload_to="teamember/")

    def admin_photo(self):
        return mark_safe('<img src="{}" width="100" />'.format(self.img.url))

    admin_photo.short_description = "Team-member Image"
    admin_photo.allow_tags = True

    def __str__(self):
        return self.name + "--"+ self.designation

class user(models.Model):
    uname = models.CharField(max_length=30)
    email = models.EmailField()
    phonenumber = models.IntegerField()
    password = models.CharField(max_length=6)
    addresss = models.CharField(max_length=100)
    firstname = models.CharField(max_length=30,default=False)
    Lastname = models.CharField(max_length=30, default=False)

    def __str__(self):
       return self.uname

class subscribe(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    email1 = models.EmailField()

class contactus(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    uname = models.CharField(max_length=30)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.TextField(max_length=200)

    def __str__(self):
        return self.uname


class state(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class city(models.Model):
    state = models.ForeignKey(state, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.state.name + "--" + self.name

class pincode(models.Model):
    city = models.ForeignKey(city, on_delete=models.CASCADE)
    areaname = models.CharField(max_length=100)
    pincodeno = models.CharField(max_length=6)

    def __str__(self):
        return self.city.state.name + "--" + self.city.name + "--" + self.areaname + "--" + self.pincodeno

class Product(models.Model):
    total_quantity = models.IntegerField()
    Availablity = models.IntegerField()
    Featured_image = models.ImageField(upload_to="featuredproduct/")
    product_name = models.CharField(max_length=100)
    price = models.IntegerField()
    Discount = models.IntegerField()
    catergories =  models.ForeignKey(Category, on_delete=models.CASCADE)
    main_catgories = models.ForeignKey(main_catgory, on_delete=models.CASCADE, default=True)
    sub_catergories = models.ForeignKey(Sub_Category, on_delete=models.CASCADE,default=True)
    Description = RichTextField()
    date =  models.DateField(default=datetime.datetime.today)

    def admin_photo(self):
        return mark_safe('<img src="{}" width="100" />'.format(self.Featured_image.url))
    admin_photo.short_description = "Product Image"
    admin_photo.allow_tags = True

    def __str__(self):
        return self.product_name

class Product_Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image =  models.ImageField(upload_to="productimg/")

    def admin_photo(self):
        return mark_safe('<img src="{}" width="100" />'.format(self.image.url))
    admin_photo.short_description = "Image"
    admin_photo.allow_tags = True


class Additional_information(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.CharField(max_length=100)
    detail = models.CharField(max_length=100)


class Order(models.Model):
    name = CharField(_("Customer Name"), max_length=254, blank=False, null=False)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False
    )

    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"


class checkout(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField()
    address = models.TextField()
    phonenumber = models.CharField(max_length=10)
    pincode = models.CharField(max_length=6)
    product = models.CharField(max_length=100)
    image = models.ImageField(upload_to='order/image')
    quantity = models.CharField(max_length=5)
    price = models.IntegerField()
    total = models.CharField(max_length=1000)
    date = models.DateField(default=datetime.datetime.today)
    otp=models.CharField(max_length=6)

    def __str__(self):
        return self.product

    def admin_photo(self):
        return mark_safe('<img src="{}" width="100" />'.format(self.image))

    admin_photo.short_description = "Image"
    admin_photo.allow_tags = True

class Review(models.Model):
    user = models.ForeignKey(user,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    comment = models.TextField(max_length=250)
    rate = models.IntegerField(default=0)
    created_at =  models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.uname +"--"+ self.product.product_name +"--"+ self.comment

class coupon_code(models.Model):
        code = models.CharField(max_length=100)
        discount = models.IntegerField()

        def __str__(self):
            return self.code

class shipper(models.Model):
    shippername = models.CharField(max_length=30)
    shipperemail = models.EmailField()
    shipperpassword = models.IntegerField()
    shipperaddress = models.TextField(max_length=255)
    shipperphonenumber = models.IntegerField()
    aadhar = models.FileField(upload_to='shipperaadhardoc/')
    pancard = models.FileField(upload_to='shipperpancarddoc/')
    drivinglience = models.FileField(upload_to='shipperdrivingliencedoc/')
    shipperimage =  models.ImageField(upload_to='shipper/image/')
    dob = models.DateTimeField()


class order_complete(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField()
    address = models.TextField()
    phonenumber = models.CharField(max_length=10)
    pincode = models.CharField(max_length=6)
    product = models.CharField(max_length=100)
    image = models.ImageField(upload_to='completeorder/image')
    quantity = models.CharField(max_length=5)
    price = models.IntegerField()
    total = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    shipper = models.ForeignKey(shipper,on_delete=models.CASCADE)

