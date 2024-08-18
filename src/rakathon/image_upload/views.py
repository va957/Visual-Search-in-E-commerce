from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from .forms import ImageUploadForm
from .models import QueryImage
from .input_to_display import fetch_s3_images
import os
import cv2
import numpy as np

def home(request):
    return render(request,'home.html')

def index(request):
    if request.user.is_authenticated:
        return redirect('upload_image')
    return redirect('signup')

def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username = request.POST['username'])
                return render (request,'signup.html', {'error':'Username is already taken!'})
            except User.DoesNotExist:
                last_user_id=User.objects.last().id
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'],id=last_user_id+1)
                auth.login(request,user)
                return redirect('upload_image')
        else:
            return render (request,'signup.html', {'error':'Password does not match!'})
    else:
        return render(request,'signup.html')

def Login(request):
    if request.method=="POST":
        username = request.POST.get('username') 
        password = request.POST.get('password')

        user = authenticate(username = username, password=password)
        
        if user:
            if user.is_active:
                login(request, user) #login is the django's default function
                
                return redirect("upload_image")

            else: 
                return HttpResponse("Account not Active")
        
        else:
            print("Someone tried to login and failed")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("Invalid Login details supplied!")

    else:
        return render(request, 'login.html',{})

@login_required(login_url='/login')
def upload_image(request):
    image_urls=[]
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new Image instance and update the image_id
            new_image = form.save(commit=False)
            new_image.user_id = request.user.id
            if QueryImage.objects.all():
                new_image.image_id = QueryImage.objects.latest('image_id').image_id + 1
            else:
                new_image.image_id = 1
            new_image.save()

            image_urls = fetch_s3_images(request)
            print(image_urls)
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form, 'image_urls': image_urls})