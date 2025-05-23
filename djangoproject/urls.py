"""
URL configuration for djangoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings

from adminpanel import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name='index'), 
      path('register/',views.register, name='register'),  # Add this line to include the index view
       
   path('login/',views.login, name='login'),  # Add this line to include the index view
  path('home/',views.home,name='home'),
           path('chat/', views.chat, name='chat'),
      path('example/',views.examples, name='example'),  
     

     path('resume_form/', views.resume_form, name='resume_form'),
  
  path('resumes/', views.manage_resumes, name='manage_resumes'),


   path('logout/',views.logout, name='logout'),  # Add this line to include the index view
]
