from django.shortcuts import render
from django.http import response
import markdown, random

from . import util

def convert(title):
    content= util.get_entry(title)
    markdowner= markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    convert_content= convert(title)
    if convert_content == None:
        return render(request, "encyclopedia/notfound.html", {
            "message": "Entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": convert_content
        })

def search(request):
    if request.method== 'POST':
        entry_title= request.POST["q"]
        if convert(entry_title) is not None:
            return render(request, "encyclopedia/entry.html", {
            "title": entry_title,
            "content": convert(entry_title)
        })
        else:
            titles= util.list_entries()
            filtered_titles= [title for title in titles if entry_title.lower() in title.lower()]
            if len(filtered_titles)>0:
                return render(request, "encyclopedia/searchresults.html", {
                    "filtered_titles": filtered_titles
                })
            else:
                return render(request, "encyclopedia/notfound.html", {
                    "message": "Entry does not exist"
                 })

def newpage(request):
    if request.method== 'GET':
        return render(request, "encyclopedia/newpage.html")
    else:
        request.method =='POST'
        new_title= request.POST["newtitle"]
        new_content= request.POST["newcontent"]
        if util.get_entry(new_title) is not None:
            error_message= "A page with this title already exists"
            return render(request, "encyclopedia/newpage.html", {
                "error_message": error_message
            })
        else:
            util.save_entry(new_title, new_content)
            return render(request, "encyclopedia/entry.html", {
            "title": new_title,
            "content": convert(new_title)
        })

def editpage(request):
     if request.method== 'POST':
        title= request.POST["edit_title"]
        content= util.get_entry(title)
        return render(request, "encyclopedia/editpage.html", {
            "title": title,
            "content": content
        })

def save(request):
    if request.method== 'POST':
        title= request.POST["title"]
        content= request.POST["content"]
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": convert(title)
        })

def randompage(request):
    list_entries= util.list_entries()
    entry_title= random.choice(list_entries)
    return render(request, "encyclopedia/entry.html", {
            "title": entry_title,
            "content": convert(entry_title)
    })