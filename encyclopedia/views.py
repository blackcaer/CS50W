from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util


def index(request):
    all_sites = util.list_entries()

    if request.method=='POST':
        return util._handle_search(request,all_sites)
        
    return render(request, "encyclopedia/index.html", {
        "entries": all_sites
    })

def content(request,content_name):
    if request.method=='POST':
        return util._handle_search(request)

    content = util.get_entry(content_name)
    if not content:
        return render(request,'encyclopedia/404_error.html',{
            'content_name':content_name,
        })
    else:
        return render(request,'encyclopedia/content.html',{
            'content_name':content_name.capitalize(),
            'content':content,
        })
    
def create_page(request):
    if request.method=='POST':
        pass

    return render(request,'encyclopedia/create_page.html')