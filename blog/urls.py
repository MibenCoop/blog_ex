from blog import views
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index,name='blog'),
    url(r'^add_category/$', views.add_category,name='add_category'),
    url(r'^categories_list/(?P<id>[1-9]+)/$', views.show_page, name='show_page'),
    url(r'^show_page/(?P<id>[1-9]+)/$', views.show_page, name='show_page'),
    url(r'^categories_list/$', views.categories_list, name='categories_list'),
    url(r'^show_category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    #url(r'^categories/journalism/add_page/$', views.add_page, name='add_page'),
    url(r'^show_category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^show_category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^show_category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
]