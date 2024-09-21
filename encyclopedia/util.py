from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.shortcuts import render
import re
import markdown2


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def _get_name(name: str):
    """ If site name exists, returns that site name, otherwise, returns None """

    result = [site_name for site_name in list_entries(
    ) if name.strip().lower() == site_name.lower()]
    return result[0] if result else None


def _handle_search(request, all_sites=None):
    if not all_sites:
        all_sites = list_entries()
    if request.method == 'POST':
        query = request.POST.get('q').strip().lower()

        site_name = _get_name(query)
        if site_name:
            return HttpResponseRedirect(site_name)
        else:
            simmilar_names = [
                name for name in all_sites if query in name.lower()]
            return render(request, 'encyclopedia/search_results.html', {
                'simmilar_names': simmilar_names
            })


def markdown(content):
    # return markdown2.markdown(content)

    def replace(text, span, replacement):
        return text[:span[0]]+replacement+text[span[1]:]

    def wrap_expression(text, regex, open_tag, close_tag, del_s=0, del_e=0, x=0):
        p = re.compile(regex, flags=re.MULTILINE)
        startpos, changes = 0, []

        while (True):
            match = p.search(text, startpos)

            if match is None:
                break
            if x == 1:
                print('XX', match.span(), ' ',
                      text[match.span()[0]:match.span()[1]])
            start, end = match.span()
            changes.append(((start, start + del_s), open_tag))
            changes.append(((end - del_e, end), close_tag))
            startpos = match.span()[1]

        changes.reverse()
        for change in changes:
            text = replace(text, *change)

        return text

    mdc = content  # mdc - markdown content

    mdc = wrap_expression(mdc, r'\*\*.+\*\*', '<strong>', '</strong>', 2, 2)
    mdc = wrap_expression(mdc, r'\*.+\*', '<em>', '</em>', 1, 1)

    mdc = wrap_expression(mdc, r'^\*\s\w.*$', '<li>', '</li>', 1, 0)
    mdc = wrap_expression(mdc, r'(<li>.*</li>\n)+', '<ul>', '</ul>')

    mdc = wrap_expression(mdc, r'^###.+$', '<h3>', '</h3>', 3, 0)
    mdc = wrap_expression(mdc, r'^##.+$', '<h2>', '</h2>', 2, 0)
    mdc = wrap_expression(mdc, r'^#.+$', '<h1>', '</h1>', 1, 0)

    mdc = wrap_expression(mdc, r'^.*\w.*(\n.*\w.*)*', '<p>', '</p>', x=1)

    return mdc
