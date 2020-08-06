from django.shortcuts import render
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
from predict.forms import ClassificationForm
from predict.models import Classification
# Create your views here.
class ClassificationListView(ListView):
    model = Classification
    form_class = ClassificationForm
    template_name = "classification_list.html"
    context_object_name = 'items'

class ClassificationDetailView(DetailView):
    model = Classification
    template_name = "classification_detail.html"

class ClassificationCreateView(CreateView):

    model = Classification
    fields = ['img']
    template_name="classification_form.html"

class ClassificationUpdateView(UpdateView):
    model = Classification
    fields = ['img']


class ClassificationDeleteView(DeleteView):
    model = Classification
    success_url = "list/"

    