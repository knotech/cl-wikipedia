def links(content):
    links = []
    for link in content.find_all('a'):
        links.append(link)
    return links


def js(webpage):
    scripts = []
    for script in webpage.find_all('script'):
        source = script.get('src')
        if source is not None:
            scripts.append(source)
    return scripts
