import ast
import csv
import json

import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

from config.settings import BASE_DIR
from core.models import Dataset


def main_page(request):

    names = []
    for root, dirs, files in os.walk(BASE_DIR + '/fixtures/'):
        for file in files:
            if file.endswith(".csv"):
                names.append(((root[root.find('fixtures'):]).split('/', 1)[1:])[0])

    list_of_dataset = []
    for dataset in Dataset.objects.all():
        list_of_dataset.append(dataset.name)

    success_message = ''

    if request.method == "POST":

        if 'file' in request.POST:

            sent_file_name = request.POST['file']
            url = BASE_DIR + '/fixtures/' + sent_file_name + '/t.csv'
            file_values = {}

            with open(url) as csvfile:
                for row in csv.reader(csvfile):
                    for column, value in enumerate(row):
                        if not value:
                            value = 0
                        file_values[column] = value

            Dataset.objects.update_or_create(name=sent_file_name, defaults={'data': json.dumps(file_values)})

            return HttpResponseRedirect('/')

        elif 'dataset' in request.POST:
            chart_id = Dataset.objects.get(name=request.POST['dataset']).id
            return redirect('chart', chart_id=chart_id)

    return render(request, 'index.html', {
        'import': names,
        'datasets': list_of_dataset,
        'message': success_message,
    })


def chart(request, chart_id):
    data = Dataset.objects.get(id=chart_id).data

    data_dict = ast.literal_eval(data)

    fig = Figure()
    ax = fig.add_subplot(111)
    x = [int(value) for value in data_dict.keys()]
    y = [int(value) for value in data_dict.values()]

    ax.plot(x, y, 'ro')
    ax.set_xticks(x)
    ax.grid(color='b', linewidth='1 ')
    canvas = FigureCanvasAgg(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
