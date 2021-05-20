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

def merge_ltx_lists(orig_list, trans_list):
    merged_list=[]

    if len(orig_list) == len(trans_list) and len(orig_list[0]) == len(trans_list[0]):
        for i in range(0,len(orig_list)):
            ltx_command =orig_list[i][0]
            opt_params  =orig_list[i][1] if trans_list[i][1] == '' else str(orig_list[i][1]).replace("]","") + " / " + str(trans_list[i][1]).replace("[","")
            nec_params  =orig_list[i][2] if trans_list[i][2] == '' else str(orig_list[i][2]).replace("}","") + " / " + str(trans_list[i][2]).replace("{","")
            text        =str(orig_list[i][3]) + "\n" + str(trans_list[i][3]) 
            merged_list.append( [ ltx_command, opt_params, nec_params, text ] )
        
    else:
        print("Original list and translated list do not have the same dimensions, cannot merge.")
    return merged_list

os.system("rm out/*")

orig_list=parse.ltxfile_to_list("/home/erikhw/latex-dragoman/in/sample.tex")
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

translated_list=rest.query_deepl("EN", ltx_list1d)
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
