from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util


def index(request):
    entries = util.list_entries()

    if len(request.GET) != 0:
        checkEntries = [el.lower() for el in entries]
        if request.GET["q"] in checkEntries:
            return show(request, request.GET["q"])
        else:
            return suggestion(request, request.GET["q"])

    return render(request, "encyclopedia/index.html", {
        "entries": entries,
    })


def show(request, name):

    text = util.get_entry(name)
    if text == None:
        text = f"{name.upper()} is not in the encyclopedia. Try a different entry!!"
    return render(request, "encyclopedia/show.html", {
        "text": text,
        "name": name
    })


def suggestion(request, name):
    print(name)
    entries = util.list_entries()
    suggestions = []
    for entry in entries:
        if name.lower() in entry.lower():
            suggestions.append(entry)

    return render(request, "encyclopedia/suggestions.html", {
        "suggestions": suggestions
    })


class EntryForm(forms.Form):

    title = forms.CharField(label="Title")
    text = forms.CharField(label="Text")


def addnewentry(request):
    form = EntryForm()
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            util.save_entry(title, text)
            return HttpResponseRedirect(reverse("index"))

    return render(request, "encyclopedia/newEntry.html", {
        "form": EntryForm()
    })
