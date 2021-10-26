# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import random
import time

from bootstrap_datepicker_plus import DateTimePickerInput
from django import forms
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from skpy import SkypeGroupChat

from app.requests import skype, Contact, Chat
from core.models import UserMapping


def collectChats(skype_chats, chats):
    print("Already Collected " + str(len(skype_chats)) + " chats")
    for chat in chats:
        if (chat.__class__ is SkypeGroupChat):
            skype_chats.append(Chat(
                chat.id,
                chat.topic))
    recent_chats = skype.chats.recent().values()
    if len(recent_chats) != 0:
        collectChats(skype_chats, recent_chats)


skype_chats = list()
collectChats(skype_chats, skype.chats.recent().values())


@login_required(login_url="/login/")
def index(request):
    context = {}
    context['segment'] = 'index'

    contacts = list()
    for contact in skype.contacts:
        contacts.append(Contact(
            contact.id,
            contact.name.first,
            contact.location.city,
            contact.birthday))
    context['contacts'] = contacts

    context['chats'] = skype_chats
    context['form'] = MessageSenderForm()
    html_template = loader.get_template('index.html')

    id_map = dict()
    for chat in skype_chats:
        id_map.update({chat.topic: chat.id})

    if request.method == "POST":
        name_map = dict()
        for object in UserMapping.objects:
            name_map.update({object.external_id: object.name})

        form = MessageSenderForm(request.POST)
        text = form.data.get("message_text")
        security_key = form.data.get("security_key")
        if security_key == "?!Qmc?wT8UDSrBQVxa^Vg_q-^G!9=aLywaPVr?H$@jf7$EUCXBRUPtn_Ey2kQD@A":
            for contact in form.data.get("recipients").split():
                name = name_map.get(contact)
                if name is not None:
                    id = id_map.get(name)
                    if id is not None:
                        if id.endswith("@thread.skype"):
                            skype.chats[id].sendMsg(text)
                        else:
                            skype.contacts[id].chat.sendMsg(text)
                        time.sleep(random.randint(3, 12))
        else:
            raise Exception("Invalid key")

    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def add_ids(request):
    context = {}
    context['segment'] = 'add_ids'

    context['contacts'] = UserMapping.objects
    context['form'] = AddIdForm()

    html_template = loader.get_template('add_ids.html')

    if request.method == "POST":
        form = AddIdForm(request.POST)
        for contact in form.data.get("recipients").split(sep=','):
            sep = contact.split(sep=':')
            UserMapping(external_id=sep[0], name=sep[1]).save()

    return HttpResponse(html_template.render(context, request))


class MessageSenderForm(forms.Form):
    recipients = forms.CharField(widget=forms.Textarea(attrs={'style': "width:100%; height:75%"}))
    message_text = forms.CharField(widget=forms.Textarea(attrs={'style': "width:100%; height:75%"}))
    security_key = forms.CharField(widget=forms.Textarea(attrs={'style': "width:100%; height:75%"}))
    date = forms.DateField(required=False, widget=DateTimePickerInput())

    def clean_title(self):
        title = self.cleaned_data['title']
        # Add a check for existing pipeline
        return title


class AddIdForm(forms.Form):
    recipients = forms.CharField(widget=forms.Textarea(attrs={'style': "width:100%; height:75%"}))

    def clean_title(self):
        title = self.cleaned_data['title']
        # Add a check for existing pipeline
        return title


# @login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))
