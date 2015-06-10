import json
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from ion_channel.models import Experiment, IonChannelModel, PatchClamp, Graph, GraphData


def index(request):
    return render(request, 'ion_channel/index.html')


class ExperimentList(ListView):
    model = Experiment
    context_object_name = 'experiments'


class ExperimentCreate(CreateView):
    model = Experiment
    fields = ['doi']
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('ion_channel:experiment-index')


class ExperimentUpdate(UpdateView):
    model = Experiment
    fields = ['doi']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('ion_channel:experiment-index')


class ExperimentDelete(DeleteView):
    model = Experiment
    success_url = reverse_lazy('ion_channel:experiment-index')


class IonChannelList(ListView):
    model = IonChannelModel
    context_object_name = 'ion_channel_models'


class IonChannelCreate(CreateView):
    model = IonChannelModel
    fields = '__all__'
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('ion_channel:ion-channel-index')


class IonChannelUpdate(UpdateView):
    model = IonChannelModel
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('ion_channel:ion-channel-index')


class IonChannelDelete(DeleteView):
    model = IonChannelModel
    success_url = reverse_lazy('ion_channel:ion-channel-index')


class PatchClampList(ListView):
    model = PatchClamp
    context_object_name = 'patch_clamps'


class PatchClampCreate(CreateView):
    model = PatchClamp
    fields = '__all__'
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('ion_channel:patch-clamp-index')


class PatchClampUpdate(UpdateView):
    model = PatchClamp
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('ion_channel:patch-clamp-index')


class PatchClampDelete(DeleteView):
    model = PatchClamp
    success_url = reverse_lazy('ion_channel:patch-clamp-index')


class GraphList(ListView):
    model = Graph
    context_object_name = 'graphs'


class GraphCreate(CreateView):
    model = Graph
    fields = '__all__'
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('ion_channel:graph-index')


class GraphUpdate(UpdateView):
    model = Graph
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('ion_channel:graph-index')


class GraphDelete(DeleteView):
    model = Graph
    success_url = reverse_lazy('ion_channel:graph-index')


class GraphDataList(ListView):
    model = GraphData
    context_object_name = 'graph_data'

    def get_queryset(self):
        print self.kwargs
        self.graph = get_object_or_404(Graph, id=self.kwargs['graph_id'])
        return GraphData.objects.filter(graph=self.graph)


class GraphDataDelete(DeleteView):
    model = GraphData

    def get_success_url(self):
        return reverse_lazy('ion_channel:graph-data-index', kwargs={'graph_id': self.object.graph_id})


def save_graph_data(request):
    response_data = {'status': 'error', 'result': 'Saving graph data has been failed'}
    print response_data
    if request.method == 'POST':
        print "is post"
        graph = get_object_or_404(Graph, pk=request.POST.get("graph_id"))
        data = GraphData(graph=graph, series_name=request.POST.get("series_name"),
                         series_data=request.POST.get("series_data"))
        data.save()
        response_data = {'status': 'success', 'result': 'Graph data has been saved.'}

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )
