from django.shortcuts import render , redirect
from .models import Item 
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import loader
import pdfkit
from django.http import HttpResponse
from django.views.generic import DetailView , CreateView , UpdateView , DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from . forms import ItemForm
from users.models import ProfileModel

# Create your views here.
@login_required
def donate(request):

    wPublicAddress = ProfileModel.objects.get(user=request.user).walletPublicAddress
    if request.method == 'POST':
        donate_form = ItemForm(request.POST,request.FILES)

        if donate_form.is_valid():
            user = request.user
            org = ProfileModel.objects.get(user=user)
            donate_form.instance.organization = org
            donate_form.instance.walletPublicAddress = wPublicAddress
            donate_form.save()
            messages.success(request, f'Post created successfully!')
            return redirect('index')

    else: 
        donate_form = ItemForm()
    context = {
        'd_form': donate_form
    }
    return render(request,'posts/donate.html',context)

@login_required
def viewDonation(request,id):
    inst = Item.objects.get(id=id)
    if request.method == 'POST':
        org = ProfileModel.objects.get(user=request.user)
        inst.ordering_organization = org
        inst.isOrdered = True
        inst.save()
        messages.success(request, f'Order accepted successfully!')
        return redirect('index')

    context = {
        'item_obj': inst
    }
    
    return render(request,'posts/view_donations.html',context)

@login_required
def index(request):
    item_objects = Item.objects.all()
    item_objects = item_objects.filter(isOrdered=False)
    '''#adding search functionality
    if item_name != '' and item_name is not None:
        item_objects = item_objects.filter(title__icontains=item_name)

    #adding pagination
    paginator = Paginator(item_objects,6)
    page = request.GET.get('page')
    item_objects = paginator.get_page(page)'''

    return render(request, 'posts/index.html', {'item_objects': item_objects})

@login_required
def myOrders(request):
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

    return render(request, 'posts/myOrders.html', {'item_objects': item_objects})

@login_required
def myPosts(request):
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

    return render(request, 'posts/myPosts.html', {'item_objects': item_objects})

