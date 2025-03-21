from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Django Admin mặc định
    path('', include('myapp.urls')),  # Bao gồm URL của myapp
]
