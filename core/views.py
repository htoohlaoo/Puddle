from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader

from item.models import Item,Category
from .forms import SignupForm
# Create your views here.
def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories =Category.objects.all()
    template = loader.get_template('core/index.html')
    return HttpResponse(template.render({"items":items,"categories":categories},request))

def contact(request):
    template = loader.get_template('core/contact.html')
    return HttpResponse(template.render({},request))

def signup(request):
    if(request.method == 'POST'):
        form=SignupForm(request.POST)

        if form.is_valid():
            form.save()
            print("Valid")
            return redirect("/login/")
    else:
        form = SignupForm()
    template = loader.get_template('core/signup.html')
    return HttpResponse(template.render({"form":form},request))
