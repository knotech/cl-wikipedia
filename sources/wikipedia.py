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
        for arg in arg_list:
            if arg != ('the' or 'an' or 'and' or 'or' or 'in' or 'on'):
                print(arg)
                arg = arg.capitalize()
                print(arg)
                query += '_'
                query += arg
    query = url + query
    return query


def is_article(webpage):
    """
        Checks if page in response is article
    """
    check = webpage.find(id='noarticletext')
    if check is None:
        return True
    else:
        return False


def is_disambiguation_page(webpage):
    """
        Checks if page in response is disambiguation link page
    """
    redirection = webpage.find_all('span', {'class': 'mw-redirectedfrom'})
    if redirection is not None:
        return True
    else:
        return False


# If page in response is article
def get_response(query):
    raw_page = get_page(query)
    mapped_page = map_DOM(raw_page)
    return mapped_page


def isolate_content(webpage):
    content_container = webpage.find(id='mw-content-text')
    return content_container


def target_text(content):
    paragraphs = get_paragraphs(content)
    return paragraphs


def clean_article_paragraphs(paragraphs):
    clean_paragraphs = []
    for p in paragraphs:
        p = p.get_text()
        if p != '':
            clean_paragraphs.append(p)
            clean_paragraphs.append('NEWLINE')
        else:
            pass
    return clean_paragraphs


def format_content():
    query_string = build_wiki_query()
    response = get_response(query_string)
    if is_article(response):
        content = isolate_content(response)
        target_text = get_paragraphs(content)
        display_text = clean_article_paragraphs(target_text)
        return display_text
    elif is_disambiguation_page(response):
        content = isolate_content(response)
        return content.text


# If page in response is disambiguation list
def list_disambiguations(content):
    pass
