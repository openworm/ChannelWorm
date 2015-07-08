import json
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from formtools.wizard.views import SessionWizardView

# Create your views here.
# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from web_app.views import AjaxResponseMixin, AjaxMixinListView, AjaxMixinCreateView
from models import *
from form import *

def index(request):
    return render(request, 'ion_channel/index.html')


class ReferenceList(ListView):
    model = Reference
    context_object_name = 'references'

class ReferenceCreate(CreateView):
    model = Reference
    form_class = ReferenceForm
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('ion_channel:reference-index')

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super(ReferenceCreate, self).form_valid(form)

class ReferenceWizard(SessionWizardView):
    template_name = 'ion_channel/reference_auto_create_form.html'
    def done(self, form_list, **kwargs):
        data = self.get_cleaned_data_for_step('1')
        data['username'] = self.request.user
        instance = Reference()

        for field, value in data.iteritems():
            if (field != 'ion_channels') and (field != 'cells'):
                setattr(instance, field, value)
        instance.save()
        channels = data['ion_channels']
        cells = data['cells']
        for value in channels.iterator():
            instance.ion_channels.add(value.id)
        for value in cells.iterator():
            instance.ion_channels.add(value.id)
        return redirect('/ion_channel/reference')

    def get_form_initial(self, step):
        initial = {}
        if step == '1':

            # TODO: Better handle the problem with creating .cache in HOME dir in OpenShift
            import os
            home_dir = os.environ["HOME"]
            if home_dir == "/var/lib/openshift/55454af95973ca347e00011b":
                os.environ["HOME"] = "/var/lib/openshift/55454af95973ca347e00011b/app-root/data/"
            from metapub import pubmedfetcher

            data = self.get_cleaned_data_for_step('0')
            fetch = pubmedfetcher.PubMedFetcher()
            if data['DOI'] != '':
                article = fetch.article_by_doi(data['DOI'])
            elif data['PMID'] != '':
                article = fetch.article_by_pmid(data['PMID'])

            initial['doi'] = article.doi
            initial['PMID'] = article.pmid
            initial['title'] = article.title
            initial['citation'] = article.__str__()
            initial['year'] = article.year
            initial['authors'] = article.authors_str
            initial['journal'] = article.journal
            initial['volume'] = article.volume
            initial['issue'] = article.issue
            initial['pages'] = article.pages
            initial['url'] = article.url

            os.environ["HOME"] = home_dir

        return initial


class ReferenceUpdate(UpdateView):
    model = Reference
    form_class = ReferenceForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('ion_channel:reference-index')


class ReferenceDelete(DeleteView):
    model = Reference
    success_url = reverse_lazy('ion_channel:reference-index')


class ExperimentList(ListView):
    model = Experiment
    context_object_name = 'experiments'


class ExperimentCreate(CreateView):
    model = Experiment
    fields = ['reference']
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('ion_channel:experiment-index')

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super(ExperimentCreate, self).form_valid(form)

class ExperimentUpdate(UpdateView):
    model = Experiment
    fields = ['reference']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('ion_channel:experiment-index')


class ExperimentDelete(DeleteView):
    model = Experiment
    success_url = reverse_lazy('ion_channel:experiment-index')


class CellCreate(CreateView):
    model = Cell
    fields = '__all__'
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('ion_channel:ion-channel-index')


class IonChannelList(ListView):
    model = IonChannel
    context_object_name = 'ion_channels'

class IonChannelDetail(UpdateView):
    model = IonChannel
    template_name_suffix = '_detail'
    fields = '__all__'



class IonChannelCreate(CreateView):
    model = IonChannel
    fields = '__all__'
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('ion_channel:ion-channel-index')


class IonChannelUpdate(UpdateView):
    model = IonChannel
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('ion_channel:ion-channel-index')


class IonChannelDelete(DeleteView):
    model = IonChannel
    success_url = reverse_lazy('ion_channel:ion-channel-index')




class IonChannelModelList(ListView):
    model = IonChannelModel
    context_object_name = 'ion_channel_models'


class IonChannelModelCreate(CreateView):
    model = IonChannelModel
    fields = '__all__'
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('ion_channel:ion-channel-model-index')


class IonChannelModelUpdate(UpdateView):
    model = IonChannelModel
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('ion_channel:ion-channel-model-index')


class IonChannelModelDelete(DeleteView):
    model = IonChannelModel
    success_url = reverse_lazy('ion_channel:ion-channel-model-index')


class PatchClampList(AjaxMixinListView, ListView):
    model = PatchClamp
    context_object_name = 'patch_clamps'


class PatchClampCreate(AjaxMixinCreateView):
    model = PatchClamp
    fields = '__all__'
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('ion_channel:patch-clamp-index')
    parentId_url_kwarg = 'experimentId'

    def post_ajax(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            response_data = {'status': 'success', 'result': 'PatchClamp data has been saved.'}
            return JsonResponse(response_data)
        else:
            return JsonResponse(form.errors, status=400)


class PatchClampUpdate(UpdateView):
    model = PatchClamp
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('ion_channel:patch-clamp-index')


class PatchClampDelete(DeleteView):
    model = PatchClamp
    success_url = reverse_lazy('ion_channel:patch-clamp-index')


class GraphList(AjaxMixinListView, ListView):
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
