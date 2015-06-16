"""channel_worm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url

from ion_channel import views
from ion_channel.views import *

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^experiment/create/$', ExperimentCreate.as_view(), name='experiment-create'),
    url(r'^home$', ExperimentList.as_view(), name='home'),
    url(r'^experiment$', ExperimentList.as_view(), name='experiment-index'),
    url(r'^experiment/update/(?P<pk>[0-9]+)$', ExperimentUpdate.as_view(), name='experiment-update'),
    url(r'^experiment/delete/(?P<pk>[0-9]+)$', ExperimentDelete.as_view(), name='experiment-delete'),

    url(r'^channel_model$', IonChannelList.as_view(), name='ion-channel-index'),
    url(r'^channel_model/create$', IonChannelCreate.as_view(), name='ion-channel-create'),
    url(r'^channel_model/update/(?P<pk>[0-9]+)$', IonChannelUpdate.as_view(), name='ion-channel-update'),
    url(r'^channel_model/delete/(?P<pk>[0-9]+)$', IonChannelDelete.as_view(), name='ion-channel-delete'),

    url(r'^patch_clamp$', PatchClampList.as_view(), name='patch-clamp-index'),
    url(r'^patch_clamp/create$', PatchClampCreate.as_view(), name='patch-clamp-create'),
    url(r'^patch_clamp/update/(?P<pk>[0-9]+)$', PatchClampUpdate.as_view(), name='patch-clamp-update'),
    url(r'^patch_clamp/delete/(?P<pk>[0-9]+)$', PatchClampDelete.as_view(), name='patch-clamp-delete'),

    url(r'^graph$', GraphList.as_view(), name='graph-index'),
    url(r'^graph/create$', GraphCreate.as_view(), name='graph-create'),
    url(r'^graph/update/(?P<pk>[0-9]+)$', GraphUpdate.as_view(), name='graph-update'),
    url(r'^graph/delete/(?P<pk>[0-9]+)$', GraphDelete.as_view(), name='graph-delete'),

    url(r'^graph_data/(?P<graph_id>[0-9]+)$', GraphDataList.as_view(), name='graph-data-index'),
    url(r'^graph_data/create$', save_graph_data, name='graph-data-create'),
    url(r'^graph_data/delete/(?P<graph_id>[0-9]+)/(?P<pk>[0-9]+)/$', GraphDataDelete.as_view(), name='graph-data-delete'),

]
