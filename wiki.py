#!/usr/bin/env python3


from bs4 import BeautifulSoup as page
from curses import wrapper
import curses
import requests
import sys
import time

stdscr = curses.initscr()
curses.noecho()
# curses.cbreak()
stdscr.keypad(True)


def parse_args_to_query():
    if len(sys.argv) == 1:
        print('Usage: wiki <your search as separate strings>')
        print('\n')

    elif len(sys.argv) > 1:
        query = sys.argv[1].capitalize()

    if len(sys.argv) > 2:
        for arg in sys.argv[2:]:
            if arg != ('the' or 'an' or 'and' or 'or' or 'in' or 'on'):
                print(arg)
                arg = arg.capitalize()
                print(arg)
                query += '_'
                query += arg

    return query


def get_page(url):
    res = requests.get(url)
    return res.text


def map_DOM(webpage):
    webpage = page(webpage, 'html.parser')
    return webpage


def is_valid_wiki_query(webpage):
    check = webpage.find(id='noarticletext')
    if check == None:
        return True
    else:
        return False


def isolate_content(webpage):
    content_container = webpage.find(id='mw-content-text')
    return content_container


def get_paragraphs(content):
    paragraphs = content.find_all('p')
    return paragraphs


def clean_paragraphs(paragraphs):
    clean_paragraphs = []
    for p in paragraphs:
        p = p.get_text()
        if p != '':
            clean_paragraphs.append(p)
            clean_paragraphs.append('NEWLINE')
        else:
            pass
    return clean_paragraphs


def paragraph_list():
    query_string = parse_args_to_query()
    raw_page = get_page('https://en.wikipedia.org/wiki/' + query_string)
    mapped_page = map_DOM(raw_page)
    if is_valid_wiki_query(mapped_page):
        content = isolate_content(mapped_page)
        target_text = get_paragraphs(content)
        display_text = clean_paragraphs(target_text)
        return display_text
    else:
        print(query_string + 'Try different capitalization')
        sys.exit(1)


def line_wrap(text, max_chars):
    text_list = text.split()
    line_list = []
    line = []
    for word in text_list:
        if word == 'NEWLINE':
            line_list.append(' '.join(line))
            line_list.append('NEWLINE')
            line = []
        elif len(' '.join(line)) + len(word) + 1 > max_chars:
            line_list.append(' '.join(line))
            line = [word]
        elif len(' '.join(line)) + len(word) + 1 < max_chars:
            line.append(word)

    line_list.append(' '.join(line))
    return line_list


def teardown():
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.endwin()


def main(stdscr):
    # Establish dimensions
    max_cols = 80
    max_rows = 40

    # Convert list of paragraphs to lines
    paragraphs = paragraph_list()
    lines = line_wrap(' '.join(paragraphs), max_cols)

    top_line = 0

    stdscr.nodelay(True)
    stdscr.clear()

    while True:
        c = stdscr.getch()
        curses.flushinp()
        stdscr.clear()

        for i in range(top_line, top_line + max_rows):
            if lines[i] == 'NEWLINE':
                stdscr.addstr(i-top_line+2, 2, '\n')
            else:
                stdscr.addstr(i-top_line+2, 2, lines[i])
        stdscr.refresh()

        if c == curses.KEY_DOWN and top_line < (len(lines) - max_rows):
            top_line += 1
        elif c == curses.KEY_UP and top_line > 0:
            top_line -= 1
        elif c == ord('q'):
            teardown()
            sys.exit()

        time.sleep(0.05)


wrapper(main)

if __name__ == '__main__':
    main()