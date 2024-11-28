from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from item.models import Item
from django.template import loader
# Create your views here.

@login_required
def index(request):
    items = Item.objects.filter(created_by = request.user)
    template = loader.get_template("dashboard/index.html")
    return HttpResponse(template.render({"items":items},request))