import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404


# Create your views here.
from ion_channel.models import Graph


def index(request):
    return render(request, 'digitizer/index.html')


def digitize(request, graph_id):
    graph = get_object_or_404(Graph, pk=graph_id)
    return render(request, 'digitizer/index.html', {'graph': graph})


def csv_export(request):
    data = request.POST.get("data")
    file_name = request.POST.get("filename")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + file_name + '.csv"'

    response.write(json.loads(data))
    return response
