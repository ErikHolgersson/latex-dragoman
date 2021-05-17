#!/usr/bin/python3

import sys
import re


def ltxfile_to_list(filename):
    with open(filename) as file:
        content = file.read()

    content = content.replace('\n', "###")
    content = content.replace('\\','\n\\')
    #print("CONTENT:\n" + str(content)+"\n##################")


    contentList = re.findall('(\\\[A-Za-z]+)'+'(\[.*\])?'+'(\{.*\})?'+'(.*)'+'', content)

    return contentList

def list_to_ltx(ltx_list):
    if len(ltx_list[1]) != 4:
        print("Given ltx_list isn't 4 elements wide, cannot be assmbled to a LaTeX-string")
        return
    
    #ltxstring=""
    #for element in ltx_list:
    #    if "begin" in element[2] and "align" in element[1]:
    #        ltxstring += element[0] + element[1] + element[2] + element[3]
    #    else:
    #        ltxstring += "\n" + element[0] + element[1] + element[2] + "\n" + element[3]
    i = 0
    ltxstring = ""
    while(i < len(ltx_list)):
        if("\\begin" in ltx_list[i][0] and "align" in ltx_list[i][2]):
            ltxstring += "\n" + ltx_list[i][0] + ltx_list[i][1] + ltx_list[i][2] + "\n" + ltx_list[i][3] + "\n"
            print("Begin assembling the align-environment")
            i = i+1
            while("\\end" not in ltx_list[i][0]):
                print("End not found, found \"" + ltx_list[i][0] + "\" instead")
                ltxstring += ltx_list[i][0] + ltx_list[i][1] + ltx_list[i][2] + ltx_list[i][3] + "\n"
                i = i+1
            print("end found.")
        else:
            ltxstring += "\n" + ltx_list[i][0] + ltx_list[i][1] + ltx_list[i][2] + "\n" + ltx_list[i][3]
            i = i+1
        
    ltxstring = ltxstring.replace('###','\n')

    return ltxstring

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
            while("\\end" not in ltx_list[i][0]):
                filtered_list.append([ ltx_list[i][0], '', '', '' ])
                i = i+1
        #only filter out params for all other fields.
        else:
            filtered_list.append([ ltx_list[i][0], '', '', ltx_list[i][3] ])
        i = i+1
        
    return filtered_list


#orig_list = ltxfile_to_list(sys.argv[1])
#trans_list = orig_list.copy()
#
#print(list_to_ltx(trans_list))