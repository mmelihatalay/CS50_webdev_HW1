from django.shortcuts import render

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
