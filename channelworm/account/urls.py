from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^register$', RegisterView.as_view(), name='register'),
    url(r'^edit/$', AccountEditView.as_view(), name='account-edit'),
]