from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms

from . import util

class CreatePageForm(forms.Form):
    name = forms.CharField(label='Page name')
    content = forms.CharField(label='Page content', widget=forms.Textarea(attrs={'name':'page_content'}))
    
    
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
        form = CreatePageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            if util._get_name(name):
                return  render(request, 'encyclopedia/create_page.html', {
                    'create_page_form': form,
                    'error': 'A page with this name already exists.'
                })
            else:
                util.save_entry(name, form.cleaned_data['content'])
                print("AA",name)
                return HttpResponseRedirect(name)


        return render(request,'encyclopedia/create_page.html',{
        'create_page_form':form
        })

    return render(request,'encyclopedia/create_page.html',{
        'create_page_form':CreatePageForm()
        })