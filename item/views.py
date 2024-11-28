from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.
from .models import Item,Category
from .forms import NewItemForm,EditItemForm

def items(request):
    query = request.GET.get('query','')
    category_id = request.GET.get('category',0)
    categories = Category.objects.all();
    items = Item.objects.filter(is_sold=False)

    if(category_id):
        items = items.filter(category_id=category_id)
    if(query):
        items = items.filter(Q(name__icontains=query)|Q(description__icontains=query))
    template = loader.get_template('item/items.html')
    return HttpResponse(template.render({"items":items,"query":query,'categories':categories,'category_id':int(category_id)},request))

def detail(request,pk):
    item = get_object_or_404(Item,pk=pk)
    related_items = Item.objects.filter(category=item.category,is_sold=False).exclude(pk=pk)[0:3]
    template = loader.get_template('item/detail.html')
    return HttpResponse(template.render({"item":item,"related_items":related_items},request))

@login_required
def new(request):
    if(request.method=="POST"):
        form = NewItemForm(request.POST,request.FILES)
        if(form.is_valid()):
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect("item:detail",pk=item.id)
    else:
        form = NewItemForm()
    template = loader.get_template('item/form.html')
    return HttpResponse(template.render({'form':form,"title":'New Item'},request))

@login_required
def delete(request,pk):
    item = get_object_or_404(Item,pk=pk,created_by= request.user)
    item.delete()
    return redirect('dashboard:index')


@login_required
def edit(request,pk):
    item = get_object_or_404(Item,created_by=request.user,pk=pk)
    if(request.method=="POST"):
        form = EditItemForm(request.POST,request.FILES,instance=item)
        if(form.is_valid()):
            form.save()
            return redirect("item:detail",pk=pk)
    else:
        form = NewItemForm(instance=item)
    template = loader.get_template('item/form.html')
    return HttpResponse(template.render({'form':form,"title":'Edit Item'},request))
