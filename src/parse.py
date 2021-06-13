#!/usr/bin/python3

import re


def ltxfile_to_list(filename):
    with open(filename) as file:
        content = file.read()

    #Wordsplitting interferes with proper translation
    content = content.replace('\\-','')
    content = content.replace('\n', "###")
    content = content.replace('\\','\n\\')
    


    contentList = re.findall('(\\\[A-Za-z#]+)'
                            +'(\[.*\])?'
                            +'(\{.*\})?'
                            +'(.*)?', content)

    return contentList

def list_to_ltx(ltx_list):
    if len(ltx_list[1]) != 4:
        print("Given ltx_list isn't 4 elements wide, cannot be assembled to a LaTeX-string")
        return

    eq_envs = { "{align}" , "{equation}", "{equation*}"}

    i = 0
    ltxstring = ""
    while( i < len(ltx_list)):
        if("\\begin" in ltx_list[i][0] and ltx_list[i][2] in eq_envs):
            ltxstring += "\n" + ltx_list[i][0] + ltx_list[i][1] + ltx_list[i][2] + ltx_list[i][3]
            #print("Begin assembling the align-environment")
            i = i+1
            while("\\end" not in ltx_list[i][0]):
                #print("End not found, found \"" + ltx_list[i][0] + "\" instead")
                ltxstring += ltx_list[i][0].replace("\n","") + ltx_list[i][1] + ltx_list[i][2] + ltx_list[i][3].replace("\n","")
                i = i+1
            #print("end found.")
        else:
            ltxstring += ltx_list[i][0] + ltx_list[i][1] + ltx_list[i][2] + ltx_list[i][3]
            i = i+1
    
    ltxstring = str(ltxstring) + '###\end{document}'
    ltxstring = ltxstring.replace('***', r'\index')
    ltxstring = ltxstring.replace('###','\n')

    return ltxstring

def filter_params(ltx_list):
    keep = { "\\title" , "\\date", "\\chapter", "\\part", "\\section", "\\subsection",
                "\\subsubsection", "\\paragraph", "\\subparagraph"}
    delete_envs = { "{align}" , "{equation}", "{equation*}", "{figure}"}

    filtered_list = list()
    
    i = 0
    while(i < len(ltx_list)):
        # keep all params that appear in the rendered document
        if(ltx_list[i][0] in keep):
            filtered_list.append(list(ltx_list[i]))
            i+=1
        # filter out equations, other environments may stay
        elif("begin" in ltx_list[i][0]) and (ltx_list[i][2] in delete_envs):
            # filter out all environments that dont need translating

            tmp_env=ltx_list[i][2]
            print("Found Environment to clear: " + tmp_env)

            filtered_list.append([ ltx_list[i][0], '', '', '' ])
            i = i+1
            while True:
                if("end" in ltx_list[i][0] and tmp_env in ltx_list[i][2]):
                    break
                
                print("cleaning out environment, command: " + ltx_list[i][0])
                filtered_list.append([ ltx_list[i][0], '', '', '' ])
                
                i = i+1
            #filtered_list.append([ ltx_list[i][0], '', '', ltx_list[i][3] ])   
    
        index_num = 0
        entry_cmd = ltx_list[i][0]
        entry_str = ltx_list[i][3]
        while (i < len(ltx_list)-1) and ("index" in ltx_list[i+1][0]):
            entry_str += "***" + ltx_list[i+1][2] + " " + ltx_list[i+1][3]
            i+=1
            index_num += 1
        filtered_list.append([ entry_cmd, '', '', entry_str ])
        for num in range(0,index_num): filtered_list.append( ['###', ' ', ' ', ' '])
        i = i+1
        
    return filtered_list


#orig_list = ltxfile_to_list(sys.argv[1])
#trans_list = orig_list.copy()
#
#print(list_to_ltx(trans_list))