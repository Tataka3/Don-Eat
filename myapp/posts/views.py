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
def donate(request):
    if request.method == 'POST':
        donate_form = ItemForm(request.POST,request.FILES)

        if donate_form.is_valid():
            user = request.user
            org = ProfileModel.objects.get(user=user)
            donate_form.instance.organization = org
            donate_form.save()
            messages.success(request, f'Post created successfully!')
            return redirect('index')

    else: 
        donate_form = ItemForm()
    context = {
        'd_form': donate_form
    }
    return render(request,'posts/donate.html',context)


def viewDonation(request):
    text = "This is view donation page"
    
    return render(request,'posts/donate.html',{'item_obj':text})

def index(request):
    item_objects = Item.objects.all()

    '''#adding search functionality
    if item_name != '' and item_name is not None:
        item_objects = item_objects.filter(title__icontains=item_name)

    #adding pagination
    paginator = Paginator(item_objects,6)
    page = request.GET.get('page')
    item_objects = paginator.get_page(page)'''

    return render(request, 'posts/index.html', {'item_objects': item_objects})

