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
    keep = { "\\title" , "\\section", "\\subsection", "\\date"}
    
    filtered_list = list()
    for i in range(0, len(ltx_list) ):
        if ltx_list[i][0] in keep:
            filtered_list.append(list(ltx_list[i]))
        elif ltx_list[0] is "\\begin" and ltx_list[2] is '\{align\}':
            filtered_list.append([ ltx_list[i][0], '', '', '' ])
        else:
            filtered_list.append([ ltx_list[i][0], '', '', ltx_list[i][3] ])
    return filtered_list

orig_list = ltxfile_to_list(sys.argv[1])
trans_list = orig_list.copy()

trans_list = filter_params(trans_list)

print("Filtered List:")
for entry in trans_list:
    print(entry[0] + " / " + entry[1] + " / " + entry[2] + " / " + entry[3] + "\n")

