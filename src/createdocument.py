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


orig_list=parse.ltxfile_to_list("/home/erikhw/latex-dragoman/in/sample.tex")
ltx_list=orig_list.copy()

ltx_list=parse.filter_params(ltx_list)
ltx_list=delete_first_column(ltx_list)
ltx_list1d = list2d_to_list1d(ltx_list)

translated_list=rest.query_deepl("EN", ltx_list1d)

translated_list2d = list1d_to_list2d(3, translated_list)

trans_doc_list2d=[]
for i in range(0,len(translated_list2d)):
    trans_doc_list2d.append([ltx_list[i][0], translated_list2d[i][0], translated_list2d[i][1], translated_list2d[i][2]])

print(parse.list_to_ltx(trans_doc_list2d))