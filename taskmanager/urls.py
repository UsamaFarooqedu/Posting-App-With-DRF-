"""
URL configuration for posting_app project.

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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tasks import views as task_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('accounts/signup/', task_views.signup, name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='task/login.html'), name='login'),
    path('accounts/logout/', task_views.custom_logout, name='logout'),
    
    # Include tasks URLs
    path('', include('tasks.urls')),
    # path('accounts/', include('accounts.urls')),
    # Include API URLs
    path('api/', include('tasks.api.urls')),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
