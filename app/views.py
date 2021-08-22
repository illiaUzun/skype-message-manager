# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import random
import time

from django import forms
from django import template
from django.http import HttpResponse
from django.template import loader
from skpy import SkypeGroupChat
from app.requests import skype, Contact, Chat
from bootstrap_datepicker_plus import DateTimePickerInput

# @login_required(login_url="/login/")
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

    skype_chats = list()
    for chat in skype.chats.recent().values():
        if (chat.__class__ is SkypeGroupChat):
            skype_chats.append(Chat(
                chat.id,
                chat.topic))
    context['chats'] = skype_chats
    context['form'] = MessageSenderForm()
    html_template = loader.get_template('index.html')

    if request.method == "POST":
        form = MessageSenderForm(request.POST)
        text = form.data.get("message_text")
        for contact in form.data.get("recipients").split():
            if contact.endswith("@thread.skype"):
                skype.chats[contact].sendMsg(text)
            else:
                skype.contacts[contact].chat.sendMsg(text)
            time.sleep(random.randint(1, 10))

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
