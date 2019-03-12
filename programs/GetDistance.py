from Record import MappingInfo


def getDistance(mapping, callgraph1, callgraph2):
    with open(callgraph1, 'r') as origin:
        lists1 = origin.read()
    with open(callgraph1, 'r') as origin:
        lines1 = origin.readlines()
    with open(callgraph2, 'r') as target:
        lists2 = target.readlines()

    lines2 = []
    for list in lists2:
        lines2.append(list[0: -1])

    lines2 = modifyCallgraph(mapping, lines2)

    # for line in lines2:
    #     print(line)

    ########################################################
    # this part is to get distance 1(constructs distance). #
    ########################################################
    distance1_list = []
    for map in mapping:
        distance1_list.append(map.getdistance1())
    distance1 = 0.0
    for i in distance1_list:
        distance1 = i/len(distance1_list)

    ########################################################
    # this part is to get distance 2(call graph distance). #
    ########################################################
    count = 0
    for line2 in lines2:
        if(lists1.find(line2) != -1):
            count = count + 1
    distance2 = 1 - count/(len(lines1))



    ##################################################
    # this part is to get distance 3(token distance) #
    ##################################################
    distance3_list = []
    for map in mapping:
        distance3_list.append(map.getdistance3())
    distance3 = 0.0
    for i in distance3_list:
        distance3 = i/len(distance3_list)


    return distance1, distance2, distance3

def modifyCallgraph(mapping, lines):
    lists = []
    for line in lines:
        if(line.find("M:") == 0):
            line = line[2:]
            tmplists = line.split(" ")
            tmplists1 = tmplists[0].split(":")
            classname1 = tmplists1[0][1:]
            classname1 = findOriginclass(mapping, classname1)

            method1 = tmplists1[1]
            method1 = findOriginmethod(mapping, classname1, method1)

            tmplists2 = tmplists[1].split(":")
            classname2 = tmplists2[0][4:]
            classname2 = findOriginclass(mapping, classname2)

            method2 = tmplists2[1]
            method2 = findOriginmethod(mapping, classname2, method2)

            tmp = "M:L" + classname1 + ":" + method1 + " " + tmplists2[0][:4] + classname2 + ":" + method2
            lists.append(tmp)
        else:
            line = line[2:]
            tmplists = line.split(" ")
            classname1 = tmplists[0][1:]
            classname1 = findOriginclass(mapping, classname1)

            classname2 = tmplists[1][1:]
            classname2 = findOriginclass(mapping, classname2)
            tmp = "C:L" + classname1 + " L" + classname2
            lists.append(tmp)
    return lists


def findOriginclass(mapping, classname):
    for m in mapping:
        if(m.getclassInfo().gettarget() == classname):
            return m.getclassInfo().getorigin()

    return classname

def findOriginmethod(mapping, classname, method):
    for m in mapping:                               #mapping and methods from the same file, order is not taken into consideration there
        if(m.getclassInfo().getorigin() == classname):
            methods = m.getmethods()
            for me in methods:
                if(me.gettarget() == method):
                    return me.getorigin()
    return method