from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
from django.views.decorators.csrf import csrf_exempt
from .paytm import checksum
import json
# Create your views here.
MERCHANT_KEY = 'xxxxxxxxxxxxxxxx'
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
def searchMatch(query,item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allprods = []
    catprods = Product.objects.values('category','id')
    cats = {item ['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) !=0:
            allprods.append([prod, range(1,nSlides),nSlides])
    params = {'allProds' : allprods,'msg':""}
    if len(allprods) == 0 or len(query)<4:
        params = {'msg' : "Please make sure to enter relevant search query"}
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
                    response = json.dumps({"status": "success", "updates": updates, "itemsJson" :order[0].items_json},default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request,'shop/tracker.html')

def productview(request,myid):
    #Fetch the product using id
    product = Product.objects.filter(id=myid)
    return render(request,'shop/prodview.html',{'product':product[0]})
def checkout(request):
    if request.method =="POST":
        print(request)
        name = request.POST.get('name','')
        amount = request.POST.get('amount','')
        items_json = request.POST.get('itemsjson','')
        email= request.POST.get('email','')
        address= request.POST.get('address1','') + " " +request.POST.get('address2','')
        city= request.POST.get('city','')
        state= request.POST.get('state','')
        zip_code= request.POST.get('zip','')
        phone = request.POST.get('phone','')
        checkout = Orders(items_json=items_json,name=name,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone,amount=amount)
        checkout.save()
        update = OrderUpdate(order_id=checkout.order_id,update_desc="The Order Has Been Placed")
        update.save()
        thank = True
        id=checkout.order_id
        # return render(request,'shop/checkout.html',{'thank':thank,'id':id})
        #Request paytm to transfer amount to your account after payment by user
        param_dict ={
            'MID': 'Your-Merchant-Id-Here',
            'ORDER_ID': str(checkout.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request,'shop/paytm.html',{'param_dict' : param_dict})
    return render(request,'shop/checkout.html')

@csrf_exempt
def handlerequest(request):
    #Paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response.dict[i] = form[i]
        if i =='CHECKSUMHASH':
            checksum = form[i]
    verify = checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because ' + response_dict['RESPMSG'])
    return render(request,'shop/paymentstatus.html',{'response': response_dict})
    pass