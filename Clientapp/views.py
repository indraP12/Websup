from django.shortcuts import render, HttpResponseRedirect
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.

#####################
#   Website Views
#####################
def homepage(request):
    template = 'website/homepage.html'
    context = {}
    return render(request, template,context)

def aboutus(request):
    template = "website/aboutus.html"
    context = {}
    return render(request, template, context)

def plans(request):
    template = "website/plans.html"
    context = {}
    return render(request, template, context)

def contactus(request):
    errors = None
    if (request.method == "POST"):
        contact_form = ContactusForm(request.POST, request.FILES)
        if contact_form.is_valid():
            new_contact = contact_form.save(commit=False)
            new_contact.from_user = request.user
            new_contact.save()
            return HttpResponseRedirect("/index")
        else:
            errors = str(new_member_form.errors)
    contact_form = ContactusForm()
    template = "website/contactus.html"
    context = {"form": contact_form, "errors": errors}
    return render(request, template, context)


#####################
#   User Views
#####################
@login_required
def dashboard(request):
    template = "clientapp/dashboard.html"
    context = {}
    return render(request, template, context)


@login_required
def send(request):
    errors = None
    if (request.method == "POST"):
        message_form = Whatsapp_Message_Form(request.POST, request.FILES)
        if message_form.is_valid():
            new_message = message_form.save(commit=False)
            new_message.from_user = request.user
            new_message.save()
            return HttpResponseRedirect("/send")
        else:
            errors = str(new_member_form.errors)
    message_form = Whatsapp_Message_Form()
    template = "clientapp/send.html"
    context = {"form": message_form, "errors": errors}
    return render(request, template, context)


@login_required
def report(request):
    template = "clientapp/report.html"
    context = {}
    return render(request, template, context)


@login_required
def currentplan(request):
    template = "clientapp/currentplan.html"
    context = {}
    return render(request, template, context)