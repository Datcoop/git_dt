"""djangocrud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.views.static import serve
from django.urls import re_path

from django.contrib import admin
from django.urls import path, include
from tasks import views

from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('apps/', include('apps.urls')),
    path('tasks/', include('tasks.urls')),
    path('joeschan36/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('usuario/', views.usuario, name='usuario'),
    path('eximport/', views.eximport, name='eximport'),
    path('convertir/', views.convertir, name='convertir'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('contacto/', views.contacto, name='contacto'),
    path('subir_archivo/', views.subir_archivo, name='subir_archivo'),
    path('combos/', views.combos, name='combos'),
    path('gallery/', include('gallery.urls')),
    path('fichero/', include('fichero.urls')),
    path('util/<int:nrut>/<str:prm>', views.util, name='util'),
]

#urlpatterns += staticfiles_urlpatterns()
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]




