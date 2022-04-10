from django.shortcuts import render , redirect
from .models import Item 
#from algorithms.giveEther import give_ether
from algorithms.application import credit
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from django.views.generic import DetailView , CreateView , UpdateView , DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from . forms import ItemForm
from users.models import ProfileModel
from django.core.mail import send_mail


# Create your views here.
@login_required
def donate(request):
    ob = ProfileModel.objects.get(user=request.user)
    role = ob.category

    wPublicAddress = ProfileModel.objects.get(user=request.user).walletPublicAddress
    if request.method == 'POST':
        donate_form = ItemForm(request.POST,request.FILES)

        if donate_form.is_valid():
            user = request.user
            org = ProfileModel.objects.get(user=user)
            donate_form.instance.posting_organization = org
            donate_form.instance.walletPublicAddress = wPublicAddress
            donate_form.save()
            messages.success(request, f'Post created successfully!')
            return redirect('index')

    else: 
        donate_form = ItemForm()
    context = {
        'd_form': donate_form,
        'role':role
    }
    return render(request,'posts/donate.html',context)

@login_required
def viewDonation(request,id):
    ob = ProfileModel.objects.get(user=request.user)
    role = ob.category

    inst = Item.objects.get(id=id)
    if request.method == 'POST':
        org = ProfileModel.objects.get(user=request.user)
        inst.ordering_organization = org
        inst.isOrdered = True
        inst.save()
        messages.success(request, f'Order accepted successfully!')
        return redirect('index')

    context = {
        'item_obj': inst,
        'role':role
    }
    
    return render(request,'posts/view_donations.html',context)

@login_required
def index(request):

    ob = ProfileModel.objects.get(user=request.user)
    role = ob.category

    item_objects = Item.objects.all()
    item_objects = item_objects.filter(isOrdered=False)
    '''#adding search functionality
    if item_name != '' and item_name is not None:
        item_objects = item_objects.filter(title__icontains=item_name)

    #adding pagination
    paginator = Paginator(item_objects,6)
    page = request.GET.get('page')
    item_objects = paginator.get_page(page)'''

    return render(request, 'posts/index.html', {'item_objects': item_objects,'role':role})

@login_required
def myOrders(request):

    ob = ProfileModel.objects.get(user=request.user)
    role = ob.category

    item_objects = Item.objects.all()
    org = ProfileModel.objects.get(user=request.user)
    item_objects = item_objects.filter(ordering_organization=org)
    '''#adding search functionality
    if item_name != '' and item_name is not None:
        item_objects = item_objects.filter(title__icontains=item_name)

    #adding pagination
    paginator = Paginator(item_objects,6)
    page = request.GET.get('page')
    item_objects = paginator.get_page(page)'''

    return render(request, 'posts/myOrders.html', {'item_objects': item_objects,'role':role})

@login_required
def myPosts(request):

    ob = ProfileModel.objects.get(user=request.user)
    role = ob.category

    item_objects = Item.objects.all()
    org = ProfileModel.objects.get(user=request.user)
    item_objects = item_objects.filter(posting_organization=org)
    '''#adding search functionality
    if item_name != '' and item_name is not None:
        item_objects = item_objects.filter(title__icontains=item_name)

    #adding pagination
    paginator = Paginator(item_objects,6)
    page = request.GET.get('page')
    item_objects = paginator.get_page(page)'''

    return render(request, 'posts/myPosts.html', {'item_objects': item_objects,'role':role})

@login_required
def myDeliveries(request):

    ob = ProfileModel.objects.get(user=request.user)
    role = ob.category

    item_objects = Item.objects.all()
    org = ProfileModel.objects.get(user=request.user)
    item_objects = item_objects.filter(deliveredBy=org)
    '''#adding search functionality
    if item_name != '' and item_name is not None:
        item_objects = item_objects.filter(title__icontains=item_name)

    #adding pagination
    paginator = Paginator(item_objects,6)
    page = request.GET.get('page')
    item_objects = paginator.get_page(page)'''

    return render(request, 'posts/myDeliveries.html', {'item_objects': item_objects,'role':role})

@login_required
def pendingDeliveries(request):

    ob = ProfileModel.objects.get(user=request.user)
    role = ob.category

    item_objects = Item.objects.all()
    org = ProfileModel.objects.get(user=request.user)
    item_objects = item_objects.filter(isOrdered=True)
    item_objects = item_objects.filter(isDelivered=False)
    item_objects = item_objects.filter(isChecked=False)
    '''#adding search functionality
    if item_name != '' and item_name is not None:
        item_objects = item_objects.filter(title__icontains=item_name)

    #adding pagination
    paginator = Paginator(item_objects,6)
    page = request.GET.get('page')
    item_objects = paginator.get_page(page)'''

    return render(request, 'posts/pendingDeliveries.html', {'item_objects': item_objects,'role':role})



@login_required
def verifyDonation(request,id):
    ob = ProfileModel.objects.get(user=request.user)
    role = ob.category

    inst = Item.objects.get(id=id)
    walletAddress = inst.ordering_organization.walletPublicAddress
    email = inst.posting_organization.user.email

    if request.method == 'POST':
        quality = request.POST.get("quality")
        quantity = request.POST.get("quantity")
        inst.isChecked = True
        if quality=='True' and quantity=='True':

            inst.isDelivered = True
            inst.isQuantityOK = True
            inst.isQualityOK = True
            inst.save()
            message = give_ether(walletAddress)
            #message = credit(walletAddress,1)
            subject = f'Tokens from Don-Eat'
            email_from = 'jainookun@gmail.com'
            recipient_list = [email, ]
            send_mail( subject, message, email_from, recipient_list )
            print("Success mail sent")
            messages.success(request, f'Order accepted successfully!')
            return redirect('index')

        else:
            inst.isDelivered = False
            if quantity == 'False':
                inst.isQuantityOK = False
            else:
                inst.isQuantityOK = True
            if quality == 'False':
                inst.isQualityOK = False
            else:
                inst.isQualityOK = True
            inst.save()

            messages.success(request, f'Order rejected due to failure of meeting the standards! Sumimasen :(')
            return redirect('index')

    context = {
        'item_obj': inst,
        'role':role
    }
    
    return render(request,'posts/verify_donations.html',context)

# @login_required
# def myOrders(request):

#     ob = ProfileModel.objects.get(user=request.user)
#     role = ob.category

#     item_objects = Item.objects.all()
#     org = ProfileModel.objects.get(user=request.user)
#     item_objects = item_objects.filter(ordering_organization=org)
#     item_objects = item_objects.filter(isChecked=True)
#     item_objects = item_objects.filter(isDelivered=False)
#     '''#adding search functionality
#     if item_name != '' and item_name is not None:
#         item_objects = item_objects.filter(title__icontains=item_name)

#     #adding pagination
#     paginator = Paginator(item_objects,6)
#     page = request.GET.get('page')
#     item_objects = paginator.get_page(page)'''

#     return render(request, 'posts/myFailedOrders.html', {'item_objects': item_objects,'role':role})