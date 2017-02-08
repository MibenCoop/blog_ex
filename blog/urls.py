from blog import views
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index,name='blog'),
    url(r'^add_category/$', views.add_category,name='add_category'),
    url(r'^profile/(?P<username>[\w\-]+)/$',views.profile, name='profile'),

    url(r'^categories_list/(?P<id>[1-9]+)/$', views.show_page, name='show_page'),
    url(r'^show_page/(?P<id>[1-9]+)/$', views.show_page, name='show_page'),
    url(r'^categories_list/$', views.categories_list, name='categories_list'),
    url(r'^show_page/(?P<page_id>[1-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^show_page/(?P<page_id>[1-9]+)/views/$', views.watched_page, name='watched_page'),
    url(r'^show_category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^show_category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
]