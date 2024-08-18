from django.contrib import admin
from django.urls import path, include
from image_upload import views
from django.conf import settings  
from django.conf.urls.static import static  
from django.contrib.auth.views import LogoutView 


urlpatterns = [
    path('', views.index, name="index"),
    path('home', views.home, name="home"),
    path("login", views.Login,name="Login"),
    path("logout", LogoutView.as_view(next_page="Login"),name="logout"),
    path("signup", views.signup,name="signup"),
    path("upload_image", views.upload_image, name="upload_image")
]

if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  