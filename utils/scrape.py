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


def get_bold(content):
    bolded = content.find_all('b')
    return bolded


def get_headings(content, index=1):
    headings = content.find_all('h' + str(index))
    return headings


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


def get_code(webpage):
    code_blocks = []
    for code_block in webpage.find_all('code'):
        code_blocks.append(code_block)
    return code_blocks


if __name__ == '__main__':
    get_page()