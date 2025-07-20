from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from . import models
from .models import TODO

# Create your views here.
def index_view(request):
    return render(request, 'login.html')

@login_required(login_url = 'sign-in')
def todo(request):
    if request.method == 'POST':
        title=request.POST.get('title')
        print(title)
        obj = models.TODO(title=title,user=request.user)
        obj.save()
        user=request.user        
        res = models.TODO.objects.filter(user=user).order_by('-date')
        messages.success(request, 'Todo added successfully')
        return redirect('/todopage', {'res':res})
    
    res=models.TODO.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html',{'res':res,})

@login_required(login_url = 'sign-in')
def delete_todo(request, srno):
    print(srno)
    obj = models.TODO.objects.get(srno=srno)
    obj.delete()
    messages.success(request, 'Todo deleted successfully')
    return redirect('/todopage')

@login_required(login_url = 'sign-in')
def edit_todo(request, srno):
    if request.method == 'POST':
        title = request.POST.get('title')
        print(title)
        obj = models.TODO.objects.get(srno=srno)
        obj.title = title
        obj.save()
        messages.success(request, 'Todo edited successfully')
        return redirect('/todopage')

    obj = models.TODO.objects.get(srno=srno)
    return render(request, 'edit_todo.html', {'obj': obj})

def signin_view(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
         # ⚠️ Check for missing input
        if not fnm or not pwd:
            messages.error(request, 'Username and password are required')
            return redirect('sign-in')
        # 🔐 Authenticate user
        userr = authenticate(request, username=fnm, password=pwd)
        if userr is not None:
            login(request,userr)
            messages.success(request, 'Logged in successfully')
            return redirect('/todopage')
        else:
            messages.warning(request, 'Invalid username or password')
            return redirect('sign-in')
               
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('emailid')
        pwd = request.POST.get('pwd')
        if not fnm or not emailid or not pwd:
            messages.warning(request, 'All fields are required')
            return redirect('sign-up')

        # 🚫 Check if username already exists
        if User.objects.filter(username=fnm).exists():
            messages.warning(request, 'Username already taken')
            return redirect('sign-up')

        # 🚫 Check if email already exists
        if User.objects.filter(email=emailid).exists():
            messages.warning(request, 'Email is already registered')
            return redirect('sign-up')

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