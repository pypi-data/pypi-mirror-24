'''
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
'''

"""sample_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django_tequila.admin import TequilaAdminSite
from django_tequila.urls import urlpatterns as django_tequila_urlpatterns

from sample_app.views import index, protected_view, unprotected_view

admin.autodiscover()
admin.site.__class__ = TequilaAdminSite

urlpatterns = [
    url(r'^$', index,
        name="index"),
    url(r'^protected/$', protected_view,
        name='protected'),
    url(r'^unprotected/$', unprotected_view,
        name='unprotected'),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += django_tequila_urlpatterns