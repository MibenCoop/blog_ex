from blog import views
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index,name='blog'),
    url(r'^add_category/$', views.add_category,name='add_category'),
    url(r'^list_notes/$', views.list_notes,name='list_notes'),
    url(r'^action_list/$', views.action_list,name='action_list'),
    url(r'^about/$', views.about,name='about'),
    url(r'^feed/$', views.feed,name='feed'),
    url(r'^delete_page/(?P<id>[0-9]+)/$', views.delete_page,name='delete_page'),
    url(r'^delete_comment/(?P<id>[0-9]+)/$', views.delete_comment,name='delete_comment'),
    url(r'^like/(?P<id>[0-9]+)/$', views.like,name='like'),
    url(r'^dislike/(?P<id>[0-9]+)/$', views.dislike,name='dislike'),
    url(r'^favorite/(?P<id>[0-9]+)/$', views.favorite,name='favorite'),
    url(r'^edit_comment/(?P<id>[0-9]+)/$', views.edit_comment,name='edit_comment'),
    url(r'^edit_page/(?P<id>[0-9]+)/$', views.edit_page,name='edit_page'),
   # url(r'^add_comment/(?P<id>[0-9]+)/$', views.add_comment,name='add_comment'),
   # url(r'^show_comments/(?P<id>[0-9]+)/$', views.show_comments,name='show_comments'),
    url(r'^profile/(?P<id>[0-9]+)/$',views.profile, name='profile'),
    url(r'^profiles_list/$',views.profiles_list, name='profiles_list'),
    url(r'^categories_list/(?P<id>[0-9]+)/$', views.show_page, name='show_page'),
    url(r'^profiles_list/(?P<id>[0-9]+)/$', views.show_page, name='show_page'),
    url(r'^person_pages/(?P<id>[0-9]+)/$', views.person_pages, name='person_pages'),
    url(r'^person_profile/(?P<id>[0-9]+)/$', views.person_profile, name='person_profile'),
    url(r'^subscribe/(?P<id>[0-9]+)/$', views.subscribe, name='subscribe'),
    url(r'^user_subscribes/(?P<id>[0-9]+)/$', views.user_subscribes, name='user_subscribes'),
    url(r'^show_page/(?P<id>[0-9]+)/$', views.show_page, name='show_page'),
    url(r'^categories_list/$', views.categories_list, name='categories_list'),
    #url(r'^show_page/(?P<page_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),

    url(r'^show_page/(?P<page_id>[0-9]+)/views/$', views.watched_page, name='watched_page'),
    url(r'^show_category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^show_category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
]