import sys
from utils.scrape import *


def build_wiki_query():
    """
        Build our query
    """
    url = 'https://en.wikipedia.org/wiki/'
    query = ''

    if len(sys.argv) > 1:
        query = sys.argv[1].capitalize()

    if len(sys.argv) > 2:
        for arg in sys.argv[2:]:
            if arg != ('the' or 'an' or 'and' or 'or' or 'in' or 'on'):
                print(arg)
                arg = arg.capitalize()
                print(arg)
                query += '_'
                query += arg
    query = url + query
    return query


def get_response(query):
    raw_page = get_page(query)
    mapped_page = map_DOM(raw_page)
    return mapped_page


def isolate_content(webpage):
    content_container = webpage.find(id='mw-content-text')
    return content_container


def get_page_content():
    content = isolate_content(get_response(build_wiki_query()))
    return content


def page_type(content):
    if content.find_all('div', {'class': 'noarticletext'}) != []:
        return 'Nothing'
    elif content.find(id='disambigbox') is not None:
        return 'Disambiguation'
    else:
        return 'Article'


def target_text(content):
    paragraphs = get_paragraphs(content)
    return paragraphs


def clean_article(paragraphs):
    clean_paragraphs = []
    for p in paragraphs:
        p = p.get_text()
        if p != '':
            clean_paragraphs.append(p)
            clean_paragraphs.append('NEWLINE')
        else:
            pass
    return clean_paragraphs


def format_article(content):
    target_text = get_paragraphs(content)
    display_text = clean_article(target_text)
    return display_text


def clean_disambiguation(content):
    links = []
    # Remove TOC
    content.find(id='toc').decompose()
    for link_lists in content.find_all('ul'):
        for item in link_lists.find_all('li'):
            for link in item.find_all('a'):
                link = {
                    'href': link.get('href'),
                    'title': link.get('title'),
                    'text': link.get_text()
                }
                links.append(link)
                print(link)
    return links


def format_disambiguation(content):
    link_list = clean_disambiguation(content)
    for _ in link_list:
        print(_)


if __name__ == '__main__':
    format_disambiguation()
