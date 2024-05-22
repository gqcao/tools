#!/bin/python

import numpy as np
import re
import sys

def get_line_indent(line):
    """Returns the number of leading spaces in a line."""
    return len(line) - len(line.lstrip())

if len(sys.argv) < 2:
    print("Please provide a filename as a command-line argument.")
else:
    file_path = sys.argv[1]
    print("Reading file:", file_path)

curr_tag = ""
pattern = r'(\w+)\s*=\s*"([^"]+)"'
urls= []

with open(file_path, 'r') as file:
    for line_num, line in enumerate(file, start=1):
        # Calculate the indent of the current line
        indent = get_line_indent(line)
        
        matches = re.findall(pattern, line)
        # Constructing dictionary from extracted key-value pairs
        content = {key: value for key, value in matches}

        if indent == 4 and content.get("title") is not None:
            curr_tag = content["title"]
        if content.get("xmlUrl"):
            urls.append(content.get("xmlUrl") + " " + curr_tag)

wrt_file_path = 'urls'

# Open the file in write mode and write each element of the list to a new line
with open(wrt_file_path, 'w') as file:
    for item in urls:
        file.write(item + '\n')
