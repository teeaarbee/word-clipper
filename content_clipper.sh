#!/bin/bash

# Try to find a working Python with tkinter
if [ -f "/opt/homebrew/bin/python3" ]; then
    /opt/homebrew/bin/python3 content_finder.py
elif [ -f "/usr/local/bin/python3" ]; then
    /usr/local/bin/python3 content_finder.py
else
    python3 content_finder.py
fi

