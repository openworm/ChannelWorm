from django.contrib import admin
from .models import *
admin.site.register(Experiment)
admin.site.register(IonChannelModel)
admin.site.register(PatchClamp)
admin.site.register(Graph)
admin.site.register(GraphData)
# Register your models here.
