from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from users.models import User
from django.contrib.auth import login


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'E-mail and password are required')
            return redirect('login')
        
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'No user matching e-mail')
            return redirect('login')
        
        is_password = check_password(password=password, encoded=user.password)

        if is_password:
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, 'Incorrect password. Try again')
            return redirect('login')
        
    else:
        return render(request, 'users/login.html')


def signup_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not email or not username or not password1 or not password2:
            messages.error(request, 'All fields are required')
            return redirect('signup')
        
        try:
            user = User.objects.get(email=email)
            messages.error(request, 'Email is taken')
            return redirect('signup')
        except: pass

        try:
            user = User.objects.get(username=username)
            messages.error(request, 'Username is taken')
            return redirect('signup')
        except: pass

        if password1 != password2:
            messages.error(request, 'Passwords did not match')
            return redirect('signup')
        
        else:
            user = User(email=email, username=username)
            user.set_password(password1)
            user.save()
            login(request, user)
            return redirect('home')
        
    else:
        return render(request, 'users/registration.html')