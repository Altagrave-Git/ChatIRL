from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from users.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from users.serializers import UserSerializer


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
    

@login_required
def profile_view(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        return redirect('home')
    
    context = {
        'user': UserSerializer(user).data
    }

    if request.method == 'POST':
        if user == request.user:
            new_username = request.POST.get('new_username')
            color = request.POST.get('color')

            if not new_username or not color:
                messages.error(request, 'Fields cannot be empty')
                return redirect('profile', username=username)
            
            if new_username != username:
                user_check = User.objects.filter(username=new_username)
                if user_check.exists():
                    messages.error(request, 'Username taken')
                    return redirect('profile', username=username)
                
            user.color = color
            user.username = new_username
            user.save()
            return redirect('home')

        else:
            return redirect('home')

    return render(request, 'users/profile.html', context=context)