from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from phone.forms import CreateUserForm, LoginUserForm ,Paymentform
from phone.models import Cart, ItemDetails, Items, Payment
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'request':request}))

def showphone(request):
    template = loader.get_template('showphone.html')
    phone = ItemDetails.objects.select_related()
    return HttpResponse(template.render({'phone': phone , 'request':request}))

def details(request,id):
    template = loader.get_template('details.html')
    phone = ItemDetails.objects.select_related('itemsid').filter(id=id)
    context={
        'phone':phone,
        'request':request
    }
    return HttpResponse(template.render(context))

@csrf_exempt
def auth_register(request):
    template=loader.get_template('auth_register.html')
    form=CreateUserForm()
    if request.method=="POST":
           form=CreateUserForm(request.POST)
           if form.is_valid():
                form.save()
                return redirect('auth_login')
    context={'registerform':form}
    return HttpResponse(template.render(context=context))

@csrf_exempt
def auth_login(request):
     template=loader.get_template('auth_login.html')
     form=LoginUserForm()
     if request.method=="POST":
           form=LoginUserForm(data=request.POST)
           if form.is_valid():
                username=form.cleaned_data['username']
                password=form.cleaned_data['password']
                
                user=authenticate(username=username,password=password)
                if user:
                     if user.is_active:
                          login(request,user)
                          return render(request,'index.html')
     context={'form':form}
     return render(request,'auth_login.html',context)

@csrf_exempt
def auth_logout(request):
     if request.method=="POST":
          logout(request)
          return redirect("/")
     
@login_required(login_url='/auth_login/')   
def checkout(request):
    template = loader.get_template('checkout.html')
    current_user=request.user.id
    cart=Cart.objects.all().filter(Id_user=current_user).first()
    product=Items.objects.get(id=cart.Id_product)

    context={
         'cart':cart,
         'productname':product,
         'request':request,
    }

    return HttpResponse(template.render(context=context))

def add_to_cart(request,id):
     currentuser=request.user
     discount=2
     status=False
     phone = ItemDetails.objects.select_related('itemsid').filter(id=id)
     for item in phone:
           net=item.total-discount
     cart= Cart(
      Id_product=item.id,
      Id_user=currentuser.id,
      price=item.price,
      qty=item.qty,
      tax=item.tax,
      total=item.total, 
      discount=discount,
      net=net,
      status=status,
)
     currentuser=request.user.id
     count=Cart.objects.filter(Id_user=currentuser).count()
     request.session['countcart']=count
     cart.save()
     return redirect("/library")

def aboutus(request):
    template = loader.get_template('aboutus.html')
    return HttpResponse(template.render({'request':request}))


@csrf_exempt
def payments(request):
    name = request.POST.get('name')
    number = request.POST.get('number')
    expiration = request.POST.get('expiration')
    CVV = request.POST.get('CVV')
    payment = Payment(name=name, number=number, expiration=expiration, CVV=CVV)
    payment.save()
    return redirect('/pay')

def pay(request):
    template = loader.get_template('pay.html')
    return HttpResponse(template.render({'request':request}))