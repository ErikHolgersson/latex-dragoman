#!/usr/bin/python3

#what should this do?
# 1. get a 2d list from parse.py
# 2. transform this n x 4 2d-list to a 1d-list of 4*n length
# 3. use rest.py to send a query to deepL using that 1d-list
# 4. reassemble a 2d list out of the translated answer
# 5. use parse to reassemble a latex document out of the translated 2d list
# 6. assemble a bilingual document out of both lists

import parse
import rest
import os
import sys

def delete_first_column(list2d):
    cut_list=[]
    for elem in list2d:
        cut_list.append(elem[1:])
    return cut_list


def list2d_to_list1d(list2d):
    list1d=[]

    for element in list2d:
        for entry in element:
            list1d.append(entry)

    return list1d

def list1d_to_list2d(width, list1d):
    list2d=[]

    i=0
    while(i < len(list1d)):
        templist=[]
        for j in range(0,width):
            templist.append(list1d[i+j])
        list2d.append(templist)
        i += width

    return list2d

#def merge_ltx_lists(orig_list, trans_list):
#    merged_list=[]
#
#    if len(orig_list) == len(trans_list) and len(orig_list[0]) == len(trans_list[0]):
#        for i in range(0,len(orig_list)):
#            ltx_command =orig_list[i][0]
#            opt_params  =orig_list[i][1] if trans_list[i][1] == '' else str(orig_list[i][1]).replace("]","") + " / " + str(trans_list[i][1]).replace("[","")
#            nec_params  =orig_list[i][2] if trans_list[i][2] == '' else str(orig_list[i][2]).replace("}","") + " / " + str(trans_list[i][2]).replace("{","")
#            text        =str(orig_list[i][3]) + "\n" + str(trans_list[i][3]) 
#            merged_list.append( [ ltx_command, opt_params, nec_params, text ] )
#        
#    else:
#        print("Original list and translated list do not have the same dimensions, cannot merge.")
#    return merged_list

def merge_ltx_lists(orig_list, trans_list):
    #what does this do?:
    # 0. add "comment"-Package to document to handle language environments
    # 1. iterate over orig_list and find layout-blocks like chapters
    # 2. encapsulate full layout-block for original and for translated list in \begin{original | translated}
    # 3. handle \begin{align} etc. because they dont need to be present in both lists, they'll be in the doc
    #       regardless of language
    # 4. after encapsulating the blocks, merge both lists blockwise ({original} and {translated} alternate)
    
    layout_cmds = { "\\chapter", "\\part", "\\section", "\\subsection",
                "\\subsubsection", "\\paragraph", "\\subparagraph", "\\end"}
    
    ret_list=[]

    i=0
    while("begin" not in orig_list[i][0]):
        ret_list.append(orig_list[i])
        if "documentclass" in orig_list[i][0]:
            ret_list.append(('\\usepackage','',r'{comment}','###'))
            ret_list.append(('\\includecomment','',r'{original}',r'###%\includecomment{translated}###'))
            ret_list.append(('\\excludecomment','',r'{translated}',r'###%\excludecomment{original}###'))
        i+=1

    for line in range(0, len(trans_list)):
        for row in range(0,len(trans_list[line])):
            if ("index" in trans_list[line][0]):
                trans_list[line] =  [ '','','','' ]
                break
            elif trans_list[line][row] == '':
                trans_list[line][row] = orig_list[line][row]
    
    while i < len(orig_list):
        if orig_list[i][0] in layout_cmds:
            tmp_orig_list=[]
            tmp_trans_list=[]
            if("end" in orig_list[i][0]):
                ret_list.append([orig_list[i][0],orig_list[i][1],orig_list[i][2],'###'])
                tmp_orig_list.append(('\\begin','',r'{original}',orig_list[i][3]))
                tmp_trans_list.append(('\\begin','',r'{translated}',trans_list[i][3]))
                if("document" in orig_list[i][2]):
                    break
            else:
                tmp_orig_list.append(('\\begin','',r'{original}','###'))
                tmp_orig_list.append(orig_list[i])
                tmp_trans_list.append(('\\begin','',r'{translated}','###'))
                tmp_trans_list.append(trans_list[i])



            i+=1
            while not ((orig_list[i][0] in layout_cmds) or ("begin" in orig_list[i][0])):
                tmp_orig_list.append(orig_list[i])
                tmp_trans_list.append(trans_list[i])
                i +=1
            tmp_orig_list.append(('\\end','',r'{original}','###'))
            tmp_trans_list.append(('\\end','',r'{translated}','###'))
            
            for elem in tmp_orig_list: ret_list.append(elem)
            for elem in tmp_trans_list: ret_list.append(elem)

        else:
            ret_list.append(orig_list[i])
            i+=1
    return ret_list

filepath = sys.argv[1]
lang = sys.argv[2]

languages = [ "BG","CS","DA","DE","EL","EN-GB","EN-US","EN","ES","ET","FI","FR","HU","IT","JA","LT","LV","NL",
    "PL","PT-PT","PT-BR","PT","RO","RU","SK","SL","SV","ZH"]

if lang.upper() not in languages:
    print("No supported language has been given, please use one of the following options: ")
    print(languages)
    exit(255)

os.system("rm out/*")

orig_list=parse.ltxfile_to_list(filepath)
with open("out/origlist.txt","x") as f:
    for line in orig_list:
        f.write(str(line)+"\n")

ltx_list=orig_list.copy()

ltx_list=parse.filter_params(ltx_list)

with open("out/filteredlist.txt","x") as f:
    for line in ltx_list:
        f.write(str(line)+"\n")

ltx_list=delete_first_column(ltx_list)
ltx_list1d = list2d_to_list1d(ltx_list)

translated_list=rest.query_deepl(lang, ltx_list1d)
with open("out/translatedlist.txt","x") as f:
    for line in translated_list:
        f.write(str(line)+"\n")

translated_list2d = list1d_to_list2d(3, translated_list)
with open("out/translatedlist2d.txt", "x") as f:
    for line in translated_list2d:
        f.write(str(line)+"\n")

trans_doc_list2d=[]
for i in range(0,len(translated_list2d)):
    trans_doc_list2d.append([orig_list[i][0], translated_list2d[i][0], translated_list2d[i][1], translated_list2d[i][2]])

with open("out/trans_doc_list2d.txt", "x") as f:
    for line in trans_doc_list2d:
        f.write(str(line) +"\n")




transdoc=str(parse.list_to_ltx(trans_doc_list2d))

with open("out/transdoc.tex", "x") as f:
    f.write(transdoc)

merged_list=merge_ltx_lists(orig_list, trans_doc_list2d)

with open("out/mergedlist.txt", "x") as f:
    for line in merged_list:
        f.write(str(line)+"\n")
    
merged_doc = str(parse.list_to_ltx(merged_list))

print(merged_doc)

with open("out/mergeddoc.tex", "x") as f:
    f.write(merged_doc)
