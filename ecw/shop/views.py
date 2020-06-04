from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json
# Create your views here.
def index(request):
    allprods = []
    catprods = Product.objects.values('category','id')
    cats = {item ['category'] for item in catprods}
    for cat in cats:
         prod = Product.objects.filter(category=cat)
         n = len(prod)
         nSlides = n // 4 + ceil((n / 4) - (n // 4))
         allprods.append([prod, range(1,nSlides),nSlides])
    params = {'allProds' : allprods}
    return render(request,'shop/index.html', params)
def about(request):
    return render(request, 'shop/about.html')
def contact(request):
    if request.method =="POST":
        print(request)
        email= request.POST.get('email','')
        msg =request.POST.get('msg','')
        contact = Contact(c_email=email, c_msg=msg)
        contact.save()
        submit = True
        return render(request,'shop/contact.html',{'submit':submit})
    return render(request,'shop/contact.html')
def tracker(request):
    if request.method=="POST":
        OrderId = request.POST.get("orderId", '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=OrderId, email=email)
            if len(order)>0:
                Update = OrderUpdate.objects.filter(order_id=OrderId)
                updates = []
                for item in Update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response = json.dumps([updates,order[0].items_json],default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')
    return render(request,'shop/tracker.html')
def search(request):
    return render(request,'shop/search.html')
def productview(request,myid):
    #Fetch the product using id
    product = Product.objects.filter(id=myid)
    return render(request,'shop/prodview.html',{'product':product[0]})
def checkout(request):
    if request.method =="POST":
        print(request)
        name = request.POST.get('name','')
        items_json = request.POST.get('itemsjson','')
        email= request.POST.get('email','')
        address= request.POST.get('address1','') + " " +request.POST.get('address2','')
        city= request.POST.get('city','')
        state= request.POST.get('state','')
        zip_code= request.POST.get('zip','')
        phone = request.POST.get('phone','')
        checkout = Orders(items_json=items_json,name=name,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone)
        checkout.save()
        update = OrderUpdate(order_id=checkout.order_id,update_desc="The Order Has Been Placed")
        update.save()
        thank = True
        id=checkout.order_id
        return render(request,'shop/checkout.html',{'thank':thank,'id':id})
    return render(request,'shop/checkout.html') 