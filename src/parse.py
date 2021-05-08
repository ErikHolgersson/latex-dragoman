#!/usr/bin/python3

import sys
import re

# What to do?
# * gegebene LaTeX-Datei einlesen und menschenlesbare Strings ausgeben
#   --> Breakpoints bei jedem LaTeX-Befehl
#   --> Sonderhandling von Titel, Überschriften und weiteren Format-Befehlen

def ltxfile_to_list(filename):
    with open(filename) as file:
        content = file.read()

    content = content.replace('\n', "###")
    content = content.replace('\\','\n\\')
    print("CONTENT:\n" + str(content)+"\n##################")


    contentList = re.findall('(\\\[A-Za-z]+)'+'(\[.*\])?'+'(\{.*\})?'+'(.*)'+'', content)

    return contentList

def filter_params(ltx_list):
    for i in range(0, ltx_list.length):
        if ltx_list[i][1] in keep:
                
            print()
        else:
            print()
    
    return

orig_list = ltxfile_to_list(sys.argv[1]):
trans_list = orig_list.copy()

