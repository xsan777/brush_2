"""wine_2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from brush import views as brush_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', brush_views.Login.as_view(), name='login'),
                  path('usermanagement/', brush_views.Usermanagement.as_view(), name='usermanagement'),
                  path('search_total_count/', brush_views.search_total_count, name='search_total_count'),
                  path('search_total_count/', brush_views.search_total_count, name='search_total_count'),
                  path('search_total_count/', brush_views.search_total_count, name='search_total_count'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
