from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from item.models import Item
from .models import Conversation
from .forms import ConversationMessageForm
# Create your views here.
@login_required
def new_conversation(request,item_pk):
    item = get_object_or_404(Item,pk=item_pk)

    if item.created_by == request.user:
        redirect("dashboard:index")

    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        return redirect("conversation:detail",pk=conversations.first().id)
    if request.method == "POST" :
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()
            return redirect("item:detail",pk=item_pk)
    else:
        form = ConversationMessageForm()
    template = loader.get_template('conversation/new.html')
    return HttpResponse(template.render({"form":form},request))

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    template = loader.get_template('conversation/inbox.html')
    print(conversations)
    return HttpResponse(template.render({"conversations":conversations},request))

@login_required
def detail(request,pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == "POST" :
        form = ConversationMessageForm(request.POST)
        
        if form.is_valid() :
            conversation_message =form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversation:detail',pk=pk)
        
    else:
        form = ConversationMessageForm()
    
    template = loader.get_template('conversation/detail.html')
    return HttpResponse(template.render({"form":form,'conversation':conversation},request))