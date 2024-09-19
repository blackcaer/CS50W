from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
import random
from . import util


class CreatePageForm(forms.Form):
    name = forms.CharField(label='Page name')
    content = forms.CharField(
        label='Page content', widget=forms.Textarea(attrs={'name': 'page_content'}))


def index(request):
    all_sites = util.list_entries()

    if request.method == 'POST':
        return util._handle_search(request, all_sites)

    return render(request, "encyclopedia/index.html", {
        "entries": all_sites
    })


def content(request, content_name):
    if request.method == 'POST':
        return util._handle_search(request)

    content = util.get_entry(content_name)
    if not content:
        return render(request, 'encyclopedia/404_error.html', {
            'content_name': content_name,
        })
    else:
        content_markdown = util.markdown(content)

        return render(request, 'encyclopedia/content.html', {
            'content_name': content_name,
            'content': content_markdown,
        })


def create_page(request):
    if request.method == 'POST':
        form = CreatePageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            if util._get_name(name):
                return render(request, 'encyclopedia/create_page.html', {
                    'create_page_form': form,
                    'error': 'A page with this name already exists.'
                })
            else:
                util.save_entry(name, form.cleaned_data['content'])
                print("AA", name)
                return HttpResponseRedirect(name)

        return render(request, 'encyclopedia/create_page.html', {
            'create_page_form': form
        })

    return render(request, 'encyclopedia/create_page.html', {
        'create_page_form': CreatePageForm()
    })


def edit_page(request, content_name):
    content_name_safe = util._get_name(content_name)

    if content_name_safe is None:
        return render(request, 'encyclopedia/404_error.html', {
            'content_name': content_name,
        })
    del content_name

    content = util.get_entry(content_name_safe)

    if request.method == 'POST':
        form = CreatePageForm(request.POST)
        if not form.is_valid():
            return render(request, 'encyclopedia/edit_page.html', {
                'error': 'Invalid input',
                'create_page_form': form
            })

        util.save_entry(content_name_safe, form.cleaned_data['content'])
        return HttpResponseRedirect(reverse(f'content', args=[content_name_safe]))

    initial_data = {
        'name': content_name_safe,
        'content': content
    }

    edit_form = CreatePageForm(initial=initial_data)
    edit_form.fields['name'].widget.attrs['readonly'] = 'readonly'

    return render(request, 'encyclopedia/edit_page.html', {
        'create_page_form': edit_form
    })


def random_page(request):
    return HttpResponseRedirect(reverse('content', args=[random.choice(util.list_entries())]))
