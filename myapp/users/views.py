from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . forms import RegisterForm , UserUpdateForm , ProfileUpdateForm,ProfileForm
from .models import ProfileModel

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Account created successfully!')
            return redirect('setProfile')

    else:
        form = RegisterForm()
    context = {
        'form': form,
    }
    return render(request,'users/register.html',context)


@login_required
def setProfileData(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST,request.FILES)

        if profile_form.is_valid():
            profile_form.instance.user = request.user
            profile_form.instance.category='USER'
            profile_form.instance.acceptanceRate=0
            profile_form.save()
            messages.success(request, f'Account created successfully!')
            return redirect('index')

    else:

        profile_form = ProfileForm()

    context = {
        'p_form': profile_form,
        'role':'USER'
    }
    return render(request,'users/setprofile.html',context)


@login_required
def profile(request):

    obj = ProfileModel.objects.get(user=request.user)
    role = obj.category

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profilemodel)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, f'Account updated successfully!')
            return redirect('profile')

    else:

        profile_form = ProfileUpdateForm(instance=request.user.profilemodel)

    context = {
        'p_form': profile_form,
        'obj': obj,
        'role':role
    }
    return render(request,'users/profile.html',context)







