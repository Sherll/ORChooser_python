#-*-coding:utf-8-*-
#written by sherlloo 2018.10.04
import os

def managertype(types):
    return  types

def collectLists(lists, callgraph):
    className = ""
    methodName = ""
    origin = callgraph
    if os.path.exists(origin):
        os.remove(origin)
    flag = 0 #0 for class field; 1 for front method name and parameters-type; 2 for target class and method.
    result = []
    for list in lists:
        if(list.find("Class descriptor") != -1):
            className = list[list.find('\'') + 1: list.rfind('\'') - 1]
            flag = 0
        if(list.find("methods") != -1 and list.find("-") == 20):
            flag = 1
        if(flag == 1 and list.find("name") != -1 and list.find(":") == 20):
            methodName = list[list.find('\'') + 1: list.rfind('\'')]
        if(flag == 1 and list.find("type") != -1 and list.find(":") == 20):
            parameters = list[list.find('\'') + 1: list.rfind(')')]
            if(list.find('(') != list.find(')') - 1):
                parameters = parameters + ')'
            else:
                parameters = parameters + ')'
            parameters = parameters.replace(';', ',')
            parameters = managertype(parameters)
            methodName = methodName + parameters
        if(list.find("insns size") != -1):
            flag = 2
        if(flag == 2 and list.find('invoke-') != -1):
            list = list[list.find("invoke-") : list.find('//') - 1]
            tmplists = list.split(' ')
            tmp = tmplists[0][tmplists[0].find('-') + 1:]
            if(tmp.find("virtual") != -1):
                tmp = "(M)"
            elif(tmp.find("interface") != -1):
                tmp = "(I)"
            elif(tmp.find("super") != -1):
                tmp = "(O)"
            elif(tmp.find("static") != -1):
                tmp = "(S)"
            elif(tmp.find("direct") != -1):
                tmp = "(D)"
            else:
                tmp = "(R)"
            if(tmplists[-1][tmplists[-1].find(';') + 1: tmplists[-1].find(';') + 2] == '.'):
                tmp = tmp + tmplists[-1][:tmplists[-1].find(';')] + ":" + tmplists[-1][tmplists[-1].find(';') + 2: tmplists[-1].find(':')]
            else:
                tmp = tmp + tmplists[-1][:tmplists[-1].find(';')] + ":" + tmplists[-1][tmplists[-1].find(';') + 3: tmplists[-1].find(':')]
            types = tmplists[-1][tmplists[-1].find('('): tmplists[-1].find(')') + 1]
            if(types[-2: -1] == ';'):
                types = types[: -2] + ")"
            types = types.replace(';', ',')
            types = managertype(types)
            tmp = tmp + types
            tmp = "M:" + className + ":" + methodName + " " + tmp + "\n"
            tmp1 = "C:" + className + " " + tmplists[-1][:tmplists[-1].find(';')] + "\n"
            if(tmp1 not in result):
                result.append(tmp1)
            if(tmp not in result):
                result.append(tmp)

    myresult = ""
    for re in result:
        myresult = myresult + re
    with open(origin, 'w') as forigin:
        forigin.write(myresult)





def callGraph(dump, callgraph):
    inputfile = dump
    with open(inputfile, 'r') as f:
        lines = f.readlines()
        lists = []
        for line in lines:
            lists.append(line[0: -1])

    collectLists(lists, callgraph)


# if __name__ == "__main__":
#     callGraph()
