from django.shortcuts import render,redirect
from django.contrib import messages
import random
import markdown2
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_content(request,title):
    
    content = util.get_entry(title)
    if content is None:
        print("hello")
        return render(request,"encyclopedia/content.html",{
            "message":"ERROR 404 Page not Found"
        })
    
    return render(request,"encyclopedia/content.html",{
        "content": markdown2.Markdown().convert(content),
        "title": title
    })

def search(request):
    query = request.GET.get("q","")
    entries = util.list_entries()
    
    for entry in entries:
        if query.lower() == entry.lower():
            return redirect(reverse("wiki",args=[entry]))

    results = [entry for entry in entries if query.lower() in entry.lower()]

    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "results": results
    })

def add(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        if content and title:
            if not util.get_entry(title):
                messages.success(request,'Entry saved successfully')
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse('wiki',args=[title]))
            else:
                messages.error(request,f'An entry with the title "{title}", already exists.')
            
    return render(request,"encyclopedia/add_entry.html")

def randomContent(request):
    results = util.list_entries()
    randomEntry = results[random.randint(0,len(results)-1)]
    content = util.get_entry(randomEntry)
    return render(request,"encyclopedia/content.html",{
        "content": markdown2.Markdown().convert(content),
        "title": randomEntry
    })

def editEntry(request,title):
    content = util.get_entry(title)
    if request.method == "POST":
       
       if content and title:
        editedContent = request.POST.get("content")
        if  editedContent != content :
            util.save_entry(title,editedContent)
            return HttpResponseRedirect(reverse('wiki',args=[title]))
        else:
            messages.error(request,f"The entry wasn't edited")
            
    return render(request,"encyclopedia/edit_entry.html",{
        "title":title,
        "content":content
    })
