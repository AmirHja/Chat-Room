import os
import hashlib
from Crypto.Cipher import AES
import base64


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm
from .models import User


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            print(f"Registration <{user.username}> <{form.cleaned_data['password']}>")
            # login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        print(request.POST)
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                print(f"Login <{user.username}>")
                print(f"Key <{generate_encryption_key(password)}>")
                print(f"Hello <{user.username}>")
                return redirect('home')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def generate_encryption_key(password):
    key = os.urandom(16)
    hashed_password = hashlib.sha256(password.encode()).digest()[:16]
    cipher = AES.new(hashed_password, AES.MODE_ECB)
    encrypted_key = cipher.encrypt(key.ljust(16, b"\0"))
    encrypted_key_b64 = base64.b64encode(encrypted_key).decode()
    return encrypted_key_b64

