"""blog_ex URL Configuration

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
from blog import views
from blog.views import MyRegistrationView
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$',views.index,name="index"),
    #url(r'^accounts/register/$',MyRegistrationView.as_view(),name='registration_register'),
    url(r'^admin/', admin.site.urls),
    url(r'^blog/',include('blog.urls')),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^settings/password/$', views.password, name='password'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^register_profile/$',views.register_profile,name='register_profile'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^oauth/', include('social.apps.django_app.urls', namespace='social')),  # <--
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
