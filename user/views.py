import random
from django.shortcuts import render, redirect
from .models import *
from django.core.mail import send_mail
import smtplib
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import razorpay
from .constants import PaymentStatus
from django.db.models import Max, Min, Sum
from django.contrib import messages
from django.contrib.sessions.models import Session
import json,time
from cart.cart import Cart


# Create your views here.


def Home(request):
    sliders = slider.objects.all()
    banners = banner.objects.all().order_by('-id')[0:3]
    bannerarea = banner.objects.all().order_by('-id')[0:2]
    main_category = main_catgory.objects.all()
    product = Product.objects.all()
    product1 = Product.objects.all().order_by('-id')[0:1]
    product2 = Product.objects.all().order_by('-id')[1:4]
    rate  = Review.objects.all()
    product_cat = Product.objects.filter(catergories=1).all()
    product_cat1 = Product.objects.filter(catergories=1).all()
    product_cat2 = Product.objects.filter(catergories=2).all()
    for i in rate:
        review = Review.objects.filter(product_id=i.product_id)
        data = review.count()
    localtime = time.asctime(time.localtime(time.time()))

    context = {
        'sliders': sliders,
        "banners": banners,
        "main_category": main_category,
        "product": product,
        "product_cat": product_cat,
        "bannerarea": bannerarea,
        "product1": product1,
        "product2": product2,
        "product_cat1": product_cat1,
        "product_cat2": product_cat2,
        "rate":rate,
        "localtime":localtime


    }
    return render(request, "user/home.html", context)


def signin(request):
    if request.POST:
        uname = request.POST['uname']
        email = request.POST['email']
        password = request.POST['password']
        phonenumber = request.POST['phonenumber']

        if not uname:
            messages.error(request, "username must be  required!!! ")
            return redirect('/signin')
        elif len(uname) < 10:
            messages.error(request, "username must be 10 characters")
            return redirect('/signin')
        if not email:
            messages.error(request, "Email must be required!!!")
            return redirect('/signin')
        if not password:
            messages.error(request, "Password must be  required!!! ")
            return redirect('/signin')
        elif len(password) < 6:
            messages.error(request, "Password must be 6 characters only!!!")
            return redirect('/signin')
        if not phonenumber:
            messages.error(request, "Phonenumber must be  required!!! ")
            return redirect('/signin')
        elif len(phonenumber) < 10:
            messages.error(request, "Phonenumber must be 10 number only!!!")
            return redirect('/signin')
        if user.objects.filter(email=email).exists():
            messages.warning(request, "This user is already exist")
            return redirect('/login')
        else:
            obj = user(uname=uname, email=email, password=password, phonenumber=phonenumber)
            obj.save()

            request.session['uname'] = uname
            request.session['email'] = email
            request.session['password'] = password
            request.session['phonenumber'] = phonenumber

            subject = "thanks you for registering to our site"
            message = 'successfully register in our website'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)
            messages.success(request, "Register Successfull Completed")
        return redirect("/login")
    return render(request, "user/register.html")


def login(request):
    if request.session.has_key('is_login'):
        return redirect('/Home')
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        count = user.objects.filter(email=email, password=password).count()
        if count > 0:
            request.session['is_login'] = True
            request.session['user_id'] = user.objects.values('id').filter(email=email, password=password)[0]['id']
            uid = request.session.get('user_id')
            data = user.objects.get(id=uid)
            uname = data.uname
            return redirect('/Home')
        else:
            if not user.objects.filter(email=email):
                messages.error(request, "Please must be enter a valid email!!!")
                return redirect('/login')
            if not user.objects.filter(password=password):
                messages.error(request, "Password must be enter a valid password!!! ")
                return redirect('/login')
    return render(request, "user/login.html")


def logout(request):
    Session.objects.all().delete()
    messages.success(request, "logout successfully")
    return redirect('/Home')


def myprofile(request):
    uid = request.session.get('user_id')

    if user.objects.filter(id=uid).exists():
        data = user.objects.get(id=uid)
        if request.POST:
            firstname = request.POST['firstname']
            lastname = request.POST['Lastname']
            uname = request.POST['uname']
            email = request.POST['email']
            phonenumber = request.POST['phonenumber']
            address = request.POST['addresss']
            obj = user.objects.filter(id=uid).update(firstname=firstname, Lastname=lastname, uname=uname, email=email,
                                                     phonenumber=phonenumber, addresss=address)
            return redirect('/myprofile')
    else:
        return redirect('/login')

    main_category = main_catgory.objects.all()
    context = {

        "main_category": main_category,
        "data": data
    }
    return render(request, "user/myprofile.html", context)


def yourorder(request):
    uid = request.session.get('user_id')

    if user.objects.filter(id=uid).exists():
        User = user.objects.get(id=uid)
        order = checkout.objects.filter(user=User)
    else:
        return redirect('/login')

    category = Category.objects.all()
    main_category = main_catgory.objects.all()
    context = {
        "order": order,
        "category": category,
        "main_category": main_category,
    }
    return render(request, "user/yourorder.html", context)


def Shop(request):
    main_category = main_catgory.objects.all()
    category = Category.objects.all()

    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))
    FilterPrice = request.GET.get('FilterPrice')
    CATID = request.GET.get('category')
    ATOZID = request.GET.get('ATOZ')
    ZTOAID = request.GET.get('ZTOA')
    Price_lowtohighid = request.GET.get('Price_lowtohigh')
    Price_hightolowid = request.GET.get('Price_hightolow')

    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Product.objects.filter(price__lte=Int_FilterPrice)
        data = product.count()
    elif CATID:
        product = Product.objects.filter(catergories=CATID)
        data = product.count()
    elif ATOZID:
        product = Product.objects.filter().order_by('product_name')
        data = product.count()
    elif ZTOAID:
        product = Product.objects.filter().order_by('-product_name')
        data = product.count()
    elif Price_lowtohighid:
        product = Product.objects.filter().order_by('price')
        data = product.count()
    elif Price_hightolowid:
        product = Product.objects.filter().order_by('-price')
        data = product.count()
    else:
        product = Product.objects.all()
        data = product.count()

    context = {
        "category": category,
        "product": product,
        "main_category": main_category,
        "min_price": min_price,
        "max_price": max_price,
        "FilterPrice": FilterPrice,
        'data': data,
    }
    return render(request, "user/shop.html", context)


def Product_detail(request, id):
    main_category = main_catgory.objects.all()
    product = Product.objects.get(id=id)
    productreview = Product.objects.get(id=id)
    review = Review.objects.filter(product=productreview)
    data = review.count()
    context = {
        "review": review,
        "main_category": main_category,
        "product": product,
        "data": data,
    }
    return render(request, "user/product-details.html", context)


def Checkout(request):
    uid = request.session.get('user_id')
    main_category = main_catgory.objects.all()
    otp_generate = random.randint(1000, 9999)

    if request.POST:
        pin = request.POST['pincode']
        count = pincode.objects.filter(pincodeno=pin).count()

        if user.objects.filter(id=uid).exists():
            if count > 0:
                data = user.objects.get(id=uid)
                email = data.email
                phonenumber = data.phonenumber

                if request.POST:
                    firstname = request.POST['firstname']
                    lastname = request.POST['lastname']
                    email = request.POST['email']
                    phonenumber = request.POST['phonenumber']
                    address = request.POST['address']
                    pin = request.POST['pincode']
                    cart = request.session.get('cart')

                    subject = "your order will be successfull placeorder"
                    message = 'your otp:-' + str(otp_generate) + 'for delivery time is required.'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [email]
                    send_mail(subject, message, email_from, recipient_list)

                    for i in cart:
                        a = (int(cart[i]['price']))
                        b = cart[i]['quantity']
                        total = a * b
                        obj = checkout(pincode=pin, firstname=firstname, lastname=lastname, email=email,
                                       phonenumber=phonenumber, address=address, product=cart[i]['product_name'],
                                       price=cart[i]['price'], quantity=cart[i]['quantity'],
                                       image=cart[i]['Featured_image'], total=total, otp=otp_generate)
                        obj.user_id = uid
                        obj.save()
                    request.session['cart'] = {}
                    return redirect('/placeorder')
            else:
                return redirect('/Checkout')
        else:
            return redirect('/login')
    context = {
        "main_category": main_category,
    }
    return render(request, "user/checkout.html", context)


def placeorder(request):
    uid = request.session.get('user_id')
    data = checkout.objects.get(id=uid)

    subject = "your tracking id "
    message = 'your tracking id:-' + str(data.id) + 'for  track your order is required.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [data.email]
    send_mail(subject, message, email_from, recipient_list)
    return render(request, "user/index.html")


def order_payment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        client = razorpay.Client(auth=("rzp_test_EzRXaEPj18jZ4C", "lKO1INSpF9M47pI816Mm0vLr"))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=razorpay_order["id"]
        )
        order.save()
        return render(
            request,
            "user/payment.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "/callback",
                "razorpay_key": "rzp_test_EzRXaEPj18jZ4C",
                "order": order,
            },
        )
    return render(request, "user/payment.html")


@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=("rzp_test_EzRXaEPj18jZ4C", "lKO1INSpF9M47pI816Mm0vLr"))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return redirect('/Home')
            return render(request, "user/callback.html", context={"status": order.status})
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "user/callback.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "user/callback.html", context={"status": order.status})


def Termscondition(request):
    main_category = main_catgory.objects.all()
    context = {
        "main_category": main_category,
    }
    return render(request, "user/Terms&conditions.html", context)


def Returnpolicy(request):
    main_category = main_catgory.objects.all()
    context = {
        "main_category": main_category,
    }
    return render(request, "user/returnpolicy.html", context)


def Contactus(request):
    uid = request.session.get('user_id')
    main_category = main_catgory.objects.all()
    if request.POST:
        uname = request.POST['uname']
        email = request.POST['email']
        subject1 = request.POST['subject']
        message1 = request.POST['message']
        subject = "Contactus "
        message = 'your message will be successfully received our team-member and check your message then after our team contact you shortly. '
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)
        messages.success(request, "Successfull message will be sended")
        obj = contactus(uname=uname, email=email, subject=subject1, message=message1)
        obj.user_id = uid
        obj.save()
    context = {
        "main_category": main_category,
    }
    return render(request, "user/contact.html", context)


def Aboutus(request):
    main_category = main_catgory.objects.all()
    teammembers = teammember.objects.all()
    context = {
        "teammembers": teammembers,
        "main_category": main_category,
    }
    return render(request, "user/about.html", context)


def Subscribe(request):
    uid = request.session.get('user_id')
    if request.POST:
        email1 = request.POST['email1']
        if not email1:
            messages.error(request, "email must be required!!!")
            return redirect("/Home")
        else:
            obj = subscribe(email1=email1)
            obj.user_id = uid
            obj.save()
            subject = "thanks you for registering to our site"
            message = 'successfully register in our website'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email1]
            send_mail(subject, message, email_from, recipient_list)
            messages.success(request, "Successfull Subscribe")
            return redirect('/Home')
    return render(request, "user/footer.html")


def Trackorder(request):
    main_category = main_catgory.objects.all()
    if request.POST:
        track = request.POST['OrderId']
        data = checkout.objects.filter(id=track).count()

        if data > 0:
            data = checkout.objects.get(id=track)
            return render(request, 'user/trackdetail.html', {"data": data})
        else:
            return redirect('/Trackorder')

    context = {
        "main_category": main_category
    }
    return render(request, "user/trackorder.html", context)


def faq(request):
    main_category = main_catgory.objects.all()
    context = {

        "main_category": main_category
    }
    return render(request, "user/faq.html", context)


def cart(request):
    main_category = main_catgory.objects.all()
    context = {
        "main_category": main_category,
    }
    return render(request, "user/cart.html", context)


def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    messages.success(request, "Add To cart successfull")
    return redirect("cart_detail")


def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    messages.success(request, "product remove from cart")
    return redirect("cart_detail")


def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


def cart_detail(request):
    cart = request.session.get('cart')
    uid = request.session.get('user_id')
    main_category = main_catgory.objects.all()

    valid_coupon = None
    coupon = None
    invalid_coupon = None
    if request.method == "GET":
        Coupon_code = request.GET.get('coupon_code')
        if Coupon_code:
            try:
                coupon = coupon_code.objects.get(code=Coupon_code)
                valid_coupon = "Are Applicable on Current Order !"
            except:
                invalid_coupon = "Invalid Coupon Code ! "
    context = {
        'coupon': coupon,
        'valid_coupon': valid_coupon,
        'invalid_coupon': invalid_coupon,
        "main_category": main_category,
    }
    return render(request, 'user/cart.html', context)


def search(request):
    if request.GET:
        query = request.GET['query']
        category = Category.objects.all()
        main_category = main_catgory.objects.all()
        product = Product.objects.filter(catergories__name__icontains=query)
        data = product.count()
        context = {
            "product": product,
            "category": category,
            "main_category": main_category,
            "data": data,
        }
    return render(request, 'user/shop.html', context)


def review(request):
    uid = request.session.get('user_id')
    if request.method == "GET":
        product_id = request.GET.get('product_id')
        product = Product.objects.get(id=product_id)
        comment = request.GET.get('comment')
        rate = request.GET.get('rate')
        User = user.objects.get(id=uid)
        obj = Review(product=product, comment=comment, rate=rate)
        obj.user_id = uid
        obj.save()
        return redirect("/Product_detail/<int:id>", id=product_id)


def password_reset(request):
    otp = random.randint(1000, 9999)
    if request.POST:
        email = request.POST['email']

        if user.objects.filter(email=email).exists():
            obj = user.objects.filter(email=email).update(password=otp)
            subject = "Kartify"
            message = 'Your Otp:- ' + str(otp)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)

            request.session['email'] = email
            return redirect('/otp')
        else:
            messages.warning(request, "Please Enter Valid email")
            return redirect('/password_reset')
    return render(request, "user/password_reset_form.html")


def otp(request):
    uid = request.session.get('user_id')
    if request.POST:
        otp = request.POST['otp']
        data = user.objects.filter(password=otp).count()
        if data > 0:
            return redirect('/password')
        else:
            return redirect('/otp')
    return render(request, 'user/otp.html')


def password(request):
    uid = request.session.get('user_id')
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['cpassword']

        if password == confirm_password:
            messages.success(request, "Please Enter Valid email ")
            obj = user.objects.filter(email=email).update(password=password)
            messages.success(request, "password will be  Successfull change ")
            return redirect('/login')
        else:
            return redirect('/password')
    return render(request, 'user/password.html')


def maincat(request, id):
    main_category = main_catgory.objects.all()
    maincats = main_catgory.objects.get(id=id)
    product = Product.objects.filter(main_catgories=maincats)
    data = product.count()
    context = {
        "maincats ": maincats,
        "product": product,
        "main_category": main_category,
        "data": data,
    }
    return render(request, "user/maincatprod.html", context)


def cat(request, id):
    cats = Category.objects.get(id=id)
    main_category = main_catgory.objects.all()
    product = Product.objects.filter(catergories=cats)
    data = product.count()
    context = {
        "cats ": cats,
        "product": product,
        "main_category": main_category,
        "data": data
    }
    return render(request, "user/maincatprod.html", context)


def subcat(request, id):
    subcats = Sub_Category.objects.get(id=id)
    main_category = main_catgory.objects.all()
    product = Product.objects.filter(sub_catergories=subcats)
    data = product.count()
    context = {
        "subcats ": subcats,
        "product": product,
        "main_category": main_category,
        "data": data,
    }
    return render(request, "user/maincatprod.html", context)


