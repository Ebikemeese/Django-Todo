from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from . import models
from .models import TODO

# Create your views here.
@login_required(login_url = 'sign-in')
def delete_todo(request, srno):
    print(srno)
    obj = models.TODO.objects.get(srno=srno)
    obj.delete()
    messages.success(request, 'Todo deleted successfully')
    return redirect('index')

@login_required(login_url = 'sign-in')
def edit_todo(request, srno):
    if request.method == 'POST':
        title = request.POST.get('title')
        print(title)
        obj = models.TODO.objects.get(srno=srno)
        obj.title = title
        obj.save()
        messages.success(request, 'Todo edited successfully')
        return redirect('index')

    obj = models.TODO.objects.get(srno=srno)
    return render(request, 'edit_todo.html', {'obj': obj})

@login_required(login_url = 'sign-in')
def index_view(request):
    if request.method == 'POST':
        title=request.POST.get('title')
        print(title)
        obj = models.TODO(title=title,user=request.user)
        obj.save()
        user=request.user        
        res = models.TODO.objects.filter(user=user).order_by('-date')
        messages.success(request, 'Todo added successfully')
        return redirect('index',{'res':res})
    
    res=models.TODOO.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html',{'res':res,})

def signin_view(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        print(fnm,pwd)
        userr = authenticate(request, username=fnm, password=pwd)
        if userr is not None:
            login(request,userr)
            messages.success(request, 'Logged in successfully')
            return redirect('index')
        else:
            return redirect('sign-in')
               
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('emailid')
        pwd = request.POST.get('pwd')
        my_user = User.objects.create_user(fnm, emailid, pwd)
        my_user.save()
        messages.success(request, 'Account created successfully')
        return redirect('sign-in')
    return render(request, 'signup.html')

@login_required(login_url = 'sign-in')
def signout_view(request):
    logout(request)
    messages.success(request, 'Logged in successfully')
    return redirect('index')