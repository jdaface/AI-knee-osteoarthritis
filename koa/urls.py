"""koa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from predict.views import (ClassificationCreateView,ClassificationDeleteView,
    ClassificationListView,ClassificationDetailView, ClassificationUpdateView,)
from users import views as user_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('list/',ClassificationListView.as_view(),name="list"),
    path('detail/<int:pk>/',ClassificationDetailView.as_view(), name="detail"),
    path('create/',ClassificationCreateView.as_view(), name="create"),
    path('update/<int:pk>/',ClassificationUpdateView.as_view(), name ="update"),
    path('delete/<int:pk>/',ClassificationDeleteView.as_view(), name="delete"),
    url("^$", user_views.docLogin, name="docLogin"),
    url("docReg/", user_views.docReg, name="docReg"),
    url("docLogout/", user_views.docLogout, name="docLogout"),
    url("patreg/", user_views.patReg, name="patReg"),
    url("patlogin/", user_views.patLogin, name="patLogin"),
    url("patlogout/", user_views.patLogout, name="patLogout"),
    url("about/", user_views.AboutPageView, name="about"),
    url("how_to/", user_views.HowToPageView, name="howTo"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
