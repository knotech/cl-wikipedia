#!/usr/bin/env python3


import curses
import requests
import sys
import time
from bs4 import BeautifulSoup as page
from curses import wrapper
from sources.wikipedia import *
from utils.scrape import *


stdscr = curses.initscr()
curses.noecho()
# curses.cbreak()
stdscr.keypad(True)


def parse_args_to_query():
    if len(sys.argv) == 1:
        print('Usage: wiki <your search as separate strings>')
        print('\n')

    else:
        query = build_wiki_query(sys.argv)
    return query


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
    paragraphs = format_content()
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