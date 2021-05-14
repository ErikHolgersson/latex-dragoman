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
    #print("CONTENT:\n" + str(content)+"\n##################")


    contentList = re.findall('(\\\[A-Za-z]+)'+'(\[.*\])?'+'(\{.*\})?'+'(.*)'+'', content)

    return contentList

def filter_params(ltx_list):
    keep = { "\\title" , "\\date", "\\chapter", "\\part", "\\section", "\\subsection",
                "\\subsubsection", "\\paragraph", "\\subparagraph"}
    delete = { "\\begin" }

    filtered_list = list()
    
    i = 0
    while(i < len(ltx_list)):
        # keep all params that appear in the rendered document
        if(ltx_list[i][0] in keep):
            filtered_list.append(list(ltx_list[i]))
        
        # filter out equations, other environments may stay
        elif("\\begin" in ltx_list[i][0] and "align" in ltx_list[i][2]):
            # filter out all equation strings in the align environment
            print("Begin filterin the align-environment")
            while("\\end" not in ltx_list[i][0]):
                print("End not found, found \"" + ltx_list[i][0] + "\" instead")
                filtered_list.append([ ltx_list[i][0], '', '', '' ])
                i = i+1
            print("end found.")
        #only filter out params for all other fields.
        else:
            filtered_list.append([ ltx_list[i][0], '', '', ltx_list[i][3] ])
        i = i+1
        
    return filtered_list

orig_list = ltxfile_to_list(sys.argv[1])
trans_list = orig_list.copy()

trans_list = filter_params(trans_list)

print("Filtered List:")
for entry in trans_list:
    print(entry[0] + " / " + entry[1] + " / " + entry[2] + " / " + entry[3] + "\n")

