"""channelworm URL Configuration

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
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from views import *
from form import *

urlpatterns = [
    url(r'^$', index, name='index'),

    url(r'^ion_channels$', IonChannelList.as_view(), name='ion-channel-index'),
    url(r'^ion_channels/detail/(?P<pk>[0-9]+)$', IonChannelDetail.as_view(), name='ion-channel-detail'),
    url(r'^ion_channels/create$', login_required(IonChannelCreate.as_view()), name='ion-channel-create'),
    url(r'^ion_channels/update/(?P<pk>[0-9]+)$', login_required(IonChannelUpdate.as_view()), name='ion-channel-update'),
    url(r'^ion_channels/delete/(?P<pk>[0-9]+)$', login_required(IonChannelDelete.as_view()), name='ion-channel-delete'),

    url(r'^reference/create/$', login_required(ReferenceCreate.as_view()), name='reference-create'),
    url(r'^reference$', ReferenceList.as_view(), name='reference-index'),
    url(r'^reference/update/(?P<pk>[0-9]+)$', login_required(ReferenceUpdate.as_view()), name='reference-update'),
    url(r'^reference/delete/(?P<pk>[0-9]+)$', login_required(ReferenceDelete.as_view()), name='reference-delete'),
    url(r'^reference/auto_create/$', login_required(ReferenceWizard.as_view([PubForm, ReferenceForm])), name='reference-auto-create'),

    url(r'^experiment/create/$', login_required(ExperimentCreate.as_view()), name='experiment-create'),
    url(r'^home$', ExperimentList.as_view(), name='home'),
    url(r'^experiment$', ExperimentList.as_view(), name='experiment-index'),
    url(r'^experiment/update/(?P<pk>[0-9]+)$', login_required(ExperimentUpdate.as_view()), name='experiment-update'),
    url(r'^experiment/delete/(?P<pk>[0-9]+)$', login_required(ExperimentDelete.as_view()), name='experiment-delete'),

    url(r'^cell/create/$', login_required(CellCreate.as_view()), name='cell-create'),

    url(r'^ion_channel_model$', IonChannelModelList.as_view(), name='ion-channel-model-index'),
    url(r'^ion_channel_model/create$', login_required(IonChannelModelCreate.as_view()), name='ion-channel-model-create'),
    url(r'^ion_channel_model/update/(?P<pk>[0-9]+)$', login_required(IonChannelModelUpdate.as_view()), name='ion-channel-model-update'),
    url(r'^ion_channel_model/delete/(?P<pk>[0-9]+)$', login_required(IonChannelModelDelete.as_view()), name='ion-channel-model-delete'),

    url(r'^patch_clamp$', PatchClampList.as_view(), name='patch-clamp-index'),
    url(r'^patch_clamp/create$', login_required(PatchClampCreate.as_view()), name='patch-clamp-create'),
    url(r'^patch_clamp/update/(?P<pk>[0-9]+)$', login_required(PatchClampUpdate.as_view()), name='patch-clamp-update'),
    url(r'^patch_clamp/delete/(?P<pk>[0-9]+)$', login_required(PatchClampDelete.as_view()), name='patch-clamp-delete'),

    url(r'^graph$', GraphList.as_view(), name='graph-index'),
    url(r'^graph/create$', login_required(GraphCreate.as_view()), name='graph-create'),
    url(r'^graph/update/(?P<pk>[0-9]+)$', login_required(GraphUpdate.as_view()), name='graph-update'),
    url(r'^graph/delete/(?P<pk>[0-9]+)$', login_required(GraphDelete.as_view()), name='graph-delete'),

    url(r'^graph_data/(?P<graph_id>[0-9]+)$', GraphDataList.as_view(), name='graph-data-index'),
    url(r'^graph_data/create$', login_required(save_graph_data), name='graph-data-create'),
    url(r'^graph_data/delete/(?P<graph_id>[0-9]+)/(?P<pk>[0-9]+)/$', login_required(GraphDataDelete.as_view()), name='graph-data-delete'),

]
