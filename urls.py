from django.conf.urls import patterns, url
from students import views
from django.contrib.auth.views import logout_then_login, login

urlpatterns = patterns('',
    url(r'^$', views.search, name='search'),
    url(r'^add/$', views.add, name='add'),
    url(r'^docs/(?P<pk>\d+)/$', views.documents, name='documents'),
    url(r'^edit/(?P<pk>\d+)/$', views.edit, name='edit'),
    url(r'^logout/$', logout_then_login, name='logout'),
    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    #url(r'^unlock/(?P<pk>\d+)/$', views.unlock, name='unlock'),
    url(r'^view/(?P<pk>\d+)/$', views.view, name='view'),
    url(r'^test/(?P<pk>\d+)/$', views.test, name='test'),
    url(r'^ajax_search/$', views.ajax_search, name='ajax_search'),
    url(r'^countries/$', views.countries, name='countries'),
    url(r'^lists/$', views.lists, name='lists'),
    url(r'^doc/(?P<pk>\d+)/(?P<doc>[\w.]+)/$', views.doc_render, name='doc_render'),


)