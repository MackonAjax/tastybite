from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail

from .import models
# Create your views here.

#
# CUSTOM AUTHENTICATION VIEWS
#

# login
def cutom_login(request):
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = "Invalid user name or password"
            return render(request, 'Authentication/login.html', {"error":error})

    return render(request, 'Authentication/login.html')

# logout
def custom_logout(request):
    return render(request, 'Authentication/login.html')

# signup
def custom_signup(request):

    #   ...UPDATE__This view should send a mail with an OTP for verifying email in the future.

    if request.POST:
        full_name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # print(f"{full_name} : {email} : {password} : {confirm_password}")

        if password == confirm_password:
            user = User.objects.create_user(first_name=full_name, email=email, password=password, username=email)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            error = "Your passwords don't match. Please provide similar passwords"
            return render(request, 'Authentication/signup.html', {"error":error})

    return render(request, 'Authentication/signup.html')

# reset password
def custom_password_reset(request):
    return render(request, 'Authentication/reset-password.html')



#
#   CUSTOM_URLS
#

# home 
def home(request):
    return render(request, 'Qualitaste/home.html')

# order page ::> login required
@login_required
def order(request):
    if request.POST:
        user = request.user

        if user.is_authenticated:
            flavor = request.POST['flavour']
            delivery_date = request.POST['delivery_date']
            location = request.POST['delivery_point']
            extra_note = request.POST['extra_note']

            customer_order = models.Orders(user_id=user.id, cake={'flavor': flavor}, delivery_date=delivery_date, location=location, extra_note=extra_note)
            customer_order.save()

            # sendmail to bakery when a new order has been saved    ...UPDATE__Design

            send_mail(
                'Subject: An order',
                f""" user: {user}, 
                        flavor: {flavor},
                        delivery_date: {delivery_date},
                        location: {location},
                        extra_note: {extra_note}""",
                'qualitastebakery@gmail.com',

                ['ajaxmackon@gmail.com'],
                fail_silently=False
            )

            # send another email to the user approving his order   ...UPDATE__Design

            send_mail(
                'Subject: Your Order has been received',
                f"""Hello {user.first_name}, we have gladly received your order.
                            Please make payments and we can start working on your order.
                            Thanks.""",
                'qualitastebakery@gmail.com',
                [user.email],
                fail_silently=False
            )



        # print(request.POST)

        order_sent_message = "Your order has been sent successfully. You can check out your orders in your profile where you can perform more actions or cancel the order. "

        # return render(request, 'Qualitaste/order.html', {"order_sent_message":order_sent_message})
    
    else:
        order_sent_message = False
    
    ###### THE ORDERS SET ON THE ORDERS PAGE SHOUDLD BE PENDING ONES. ######
    try:
        user = request.user
        orders_set = user.orders_set.all()

        # the query set could be empty, this ensures its not
        # is_it_empty = orders_set[0]

        # print(orders_set)
    except:
        orders_set = False
        print("failed")
    return render(request, 'Qualitaste/order.html', {'orders_set': orders_set, "order_sent_message":order_sent_message})

# gallery page
def gallery(request):
    return render(request, 'Qualitaste/gallery.html')

# help page
def help(request):
    return render(request, 'Qualitaste/help.html')


# view for displaying ones profile
@login_required
def profile(request):
    user = request.user
    orders = user.orders_set.all()

    return render(request, 'Qualitaste/profile.html', {'orders':orders})


#
#   PAYMENTS
#
@login_required
def payments(request):
    return render(request, 'Qualitaste/payments.html')


# canceling an order
def cancel_order(request, pk):
    try:
        order_to_be_deleted = get_object_or_404(models.Orders, pk=pk)
        order_to_be_deleted.delete()
    except Exception:
        message = 'Failed to cancel order. Please try again.'
    else:
        message = 'Order successfully cancelled.'
    return render(request, 'Qualitaste/cancel_order.html', {'message': message})
