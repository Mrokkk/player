#!/usr/bin/env python3

def try_to_scroll(listbox, key):
    try:
        if key[0] == 'mouse press':
            if key[1] == 5.0:
                listbox.focus_position += 1
            elif key[1] == 4.0:
                listbox.focus_position -= 1
    except:
        pass

