from django.shortcuts import render, redirect
from user.models import *
from django.contrib import messages
from django.core.mail import send_mail
import smtplib
from django.conf import settings
import random
from django.contrib.sessions.models import Session


# Create your views here.

def loadfile(request):
    return render(request, "shipper/dashbroad.html")


def shipperlogin(request):
    if request.session.has_key('is_login'):
        return redirect('/dashboard')
    if request.POST:
        shipperemail = request.POST['shipperemail']
        shipperpassword = request.POST['shipperpassword']
        count = shipper.objects.filter(shipperemail=shipperemail, shipperpassword=shipperpassword).count()
        if count > 0:
            request.session['is_login'] = True
            request.session['shipper_id'] = shipper.objects.values('id').filter(shipperemail=shipperemail, shipperpassword=shipperpassword)[0]['id']
            messages.success(request, "Login is Successfull")
            return redirect("/dashboard")
        else:
            if not shipper.objects.filter(shipperemail=shipperemail):
                messages.error(request, "Please must be enter a valid email!!!")
                return redirect('/shipperlogin')
            if not shipper.objects.filter(shipperpassword=shipperpassword):
                messages.error(request, "Password must be enter a valid password!!! ")
                return redirect('/shipperlogin')
    return render(request, "shipper/shipperlogin.html")


def logout(request):
    Session.objects.all().delete()
    messages.success(request, "logout successfully")
    return redirect('/dashboard')


def dashboard(request):
    order = checkout.objects.all()
    order1 =order_complete.objects.all()
    shipperid = request.session.get('shipper_id')

    if shipper.objects.filter(id=shipperid):
        data = shipper.objects.get(id=shipperid)
        shippername = data.shippername

        request.session['shippername'] = shippername
        data = order.count()
        data1 = order1.count()
        messages.success(request, "Hi, Welcome To Shipper Dashboard")

    else:
        return redirect('/shipperlogin')
    context = {
        "order": order,
        "data": data,
        "order1":order1,
        "data1":data1,

    }

    return render(request, "shipper/dashbroad.html", context)


def profile(request):
    shipperid = request.session.get('shipper_id')

    if shipper.objects.filter(id=shipperid):
        data = shipper.objects.get(id=shipperid)

        shippername = data.shippername
        shipperphonenumber = data.shipperphonenumber
        shipperemail = data.shipperemail
        shipperaddress = data.shipperaddress

        request.session['shipperemail'] = shipperemail
        request.session['shippername'] = shippername
        request.session['shipperphonenumber'] = shipperphonenumber
        request.session['shipperaddress'] = shipperaddress
    else:
        return redirect('/shipperlogin')

    return render(request, "shipper/profile.html")


def Orderdetail(request, id):
    data = checkout.objects.get(id=id)
    return render(request, "shipper/orderdetail.html", {"data": data})


def confirm_otp(request):
    shipperid = request.session.get('shipper_id')
    if request.POST:
        otp = request.POST['otp']
        id=request.POST['id']
        request.session['id']=id
        if checkout.objects.filter(otp=otp):
            data = checkout.objects.get(id=id)
            firstname = data.firstname
            lastname = data.lastname
            address=data.address
            email = data.email
            phonenumber = data.phonenumber
            pincode = data.pincode
            product = data.product
            image = data.image
            quantity= data.quantity
            price = data.price
            total = data.total
            user=data.user.id
            data2=order_complete(firstname=firstname, lastname=lastname, email=email, address=address, phonenumber=phonenumber, pincode=pincode, product=product, image=image, quantity=quantity, price=price, total=total)
            data2.shipper_id=shipperid
            data2.user_id=user
            data2.save()
            data3=checkout.objects.get(id=id).delete()


            return redirect('/dashboard')
    return render(request , "shipper/orderdetail.html")


def ordertable(request):
    order = checkout.objects.all()
    context = {
        "order": order
    }
    return render(request, "shipper/ordertable.html", context)
