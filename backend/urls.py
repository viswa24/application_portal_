"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.http import JsonResponse
from candidates.views import apply_candidate

def hello_world(request):
    return JsonResponse({"message": "Hello, World!"})

def home(request):
    return JsonResponse({
        "message": "Welcome to Django + React API",
        "endpoints": {
            "hello": "/api/hello/",
            "admin": "/admin/",
            "apply": "/api/apply/"
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/hello/', hello_world, name='hello_world'),
    path('api/apply/', apply_candidate, name='apply_candidate'),
    path('', home, name='home'),  # Root URL pattern
]
