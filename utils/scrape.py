import requests
from bs4 import BeautifulSoup as page


def get_page(url):
    res = requests.get(url)
    return res.text


def map_DOM(webpage):
    webpage = page(webpage, 'html.parser')
    return webpage


def get_section_by_id(webpage, id):
    section = webpage.find(id=id)
    return section


def get_paragraphs(content):
    paragraphs = content.find_all('p')
    return paragraphs


def get_links(webpage):
    links = []
    for link in webpage.find_all('a'):
        links.append(link)
    return links


def get_js(webpage):
    scripts = []
    for script in webpage.find_all('script'):
        source = script.get('src')
        if source is not None:
            scripts.append(source)
    return scripts


if __name__ == '__main__':
    get_page()
