import callGraph
import RecordClass
from subprocess import Popen
from Record import MappingSingle
from Record import MappingInfo
import os
import math
import numpy as np
import GetDistance
import GetR8Dex
import Levenshtein

def getDump(dump1, dump2):
    if(os.path.exists(dump1)):
        os.remove(dump1)
    if(os.path.exists(dump2)):
        os.remove(dump2)
    p = Popen("../build-tools/26.0.1/dexdump -d -h ../output/Tetrisd8.dex > Tetrisd8.txt", shell = True)
    p.wait()
    if p.returncode != 0:
        print("Error")
        return -1
    p.kill()
    p = Popen("../build-tools/26.0.1/dexdump -d -h ../output/Tetrisr8.dex > Tetrisr8.txt", shell = True)
    p.wait()
    if p.returncode != 0:
        print("Error")
        return -1
    p.kill()

def getPerDump(source, dump):
    if(os.path.exists(dump)):
        os.remove(dump)
    cmd = "../build-tools/26.0.1/dexdump -d -h " + source + " > " + dump
    p = Popen(cmd, shell=True)
    p.wait()
    if p.returncode != 0:
        print("Error")
        return -1
    p.kill()

def calculateClass(info1, info2):
    dimensions = 0
    sum = 0.0
    distance = [0.0] * 5
    donominator = math.sqrt(math.pow(info1.getStaticfieldssize(), 2) + math.pow(info1.getInstancefieldssize(), 2) + math.pow(info1.getDirectmethodssize(), 2) \
                             + math.pow(info1.getVirtualmethodssize(), 2) \
                          + math.pow(info2.getStaticfieldssize(), 2) + math.pow(info2.getInstancefieldssize(), 2) + math.pow(info2.getDirectmethodssize(), 2) \
                             + math.pow(info2.getVirtualmethodssize(), 2)) + 1
    distance[0] = abs(info1.getStaticfieldssize() - info2.getStaticfieldssize()) / donominator
    distance[1] = abs(info1.getInstancefieldssize() - info2.getInstancefieldssize()) / donominator
    distance[2] = abs(info1.getDirectmethodssize() - info2.getDirectmethodssize()) / donominator
    distance[3] = abs(info1.getVirtualmethodssize() - info2.getVirtualmethodssize()) / donominator
    distance[4] = abs(info1.getInstructionsize() - info2.getInstructionsize()) / (donominator + math.sqrt(math.pow(info1.getInstructionsize(), 2) + math.pow(info2.getInstructionsize(), 2)))

    for i in range(5):
        if(distance[i] != 0):
            dimensions = dimensions + 1
        sum = sum + distance[i]
    sum = sum * dimensions
    return sum

def calculateMethod(method1, method2):
    #calculate the instruction distance
    ins1 = method1.getInstruction()
    ins2 = method2.getInstruction()
    lenth = len(ins1)
    sum1 = 0.0
    for i in range(lenth):
        sum1= sum1 + math.pow(ins1[i], 2) + math.pow(ins2[i], 2)
    sum1 = math.sqrt(sum1) + 1
    result = 0.0
    for i in range(lenth):
        result = result + abs(ins1[i] - ins2[i])/sum1

    if(method1.getMethodtype() != method2.getMethodtype()):
        return (10000.0 + result)
    else:
        donominator = math.sqrt(math.pow(method1.getTotalparameter(), 2) + math.pow(method1.getMethodLOC(), 2) + \
                               math.pow(method2.getTotalparameter(), 2) + math.pow(method2.getMethodLOC(), 2) + 1)
        distance = np.zeros(4)
        dimensions = 0.0
        if(method1.getReturntype() == method2.getReturntype()):
            distance[0] = 0.0/donominator
        else:
            distance[0] = 1.0/donominator

        distance[1] = abs(method1.getTotalparameter() - method2.getTotalparameter())/donominator
        distance[2] = calculateparameter(method1, method2)/donominator
        distance[3] = abs(method1.getMethodLOC() - method2.getMethodLOC())/donominator
        sum = 0
        for i in range(4):
            sum = distance[i] + sum
            if(distance[i] != 0):
                dimensions = dimensions + 1

        sum = sum * dimensions
        return (sum + result)


def calculateparameter(m1, m2):
    para1 = apartparameter(m1.getParatype()[1: -1])
    para2 = apartparameter(m2.getParatype()[1: -1])

    mark = np.zeros(m2.getTotalparameter())
    if(para1 == None):
        if(para2 == None):
            return 0.0
        else:
            return len(para2)
    else:
        if(para2 == None):
            return len(para1)
        else:
            count = 0
            for i in range(len(para1)):
                for j in range(len(para2)):
                    if(mark[j] != 1 and para1[i] == para2[j]):
                        count = count + 1
                        mark[j] = 1
            return (len(para1) + len(para2) - 2 * count)


def apartparameter(p1):
    if(p1 == ""):
        return None
    else:
        para = []
        tmplist = p1.split(",")
        if(len(tmplist) == 1):
            tmp = tmplist[0]
            record = -1
            for i in range(len(tmp)):
                if(RecordClass.isBasictype(tmp[i]) != None):
                    para.append(chr)
                elif(tmp[i] == 'L'):
                    record = i
                    break
            if(record != -1):
                para.append(tmp[record:])
        else:
            for list in tmplist:
                para = para + apartparameter(list)
        return para



def getMapping(classinfo1, classinfo2):
    commonlen = min(len(classinfo1), len(classinfo2))
    distance = np.zeros((len(classinfo1), len(classinfo2)))
    for i in range(len(classinfo1)):
        for j in range(len(classinfo2)):
            distance[i][j] = calculateClass(classinfo1[i], classinfo2[j])

    minNum = 10000
    point = np.zeros((commonlen, 2))

    for m in range(commonlen):
        for i in range(len(classinfo1)):
            for j in range(len(classinfo2)):
                if(minNum > distance[i][j] and distance[i][j] != -1):
                    minNum = distance[i][j]
                    point[m][0] = i
                    point[m][1] = j

        for j in range(len(classinfo2)):
            distance[int(point[m][0])][j] = float(-1.0)
        for i in range(len(classinfo1)):
            distance[i][int(point[m][1])] = float(-1.0)
        minNum = 10000

    mappingInfo = []
    for m in range(commonlen):
        origin = classinfo1[int(point[m][0])].getClassname()
        target = classinfo2[int(point[m][1])].getClassname()
        classInfo = MappingSingle(origin, target)
        distance3 = calculatedistance3(classinfo1[int(point[m][0])], classinfo2[int(point[m][1])])
        methods, distance1_list = getMethodsMapping(classinfo1[int(point[m][0])], classinfo2[int(point[m][1])])
        distance1 = calculateClassdistance1(classinfo1[int(point[m][0])], classinfo2[int(point[m][1])])/2
        for i in distance1_list:
            distance1 = distance1 + i/(2*(len(distance1_list)))

        mappingInfo.append(MappingInfo(classInfo, methods, distance1, distance3))

    # for m in range(commonlen):
    #     print(mappingInfo[m])

    return mappingInfo

def calculatedistance3(classinfo1, classinfo2):
    ins1 = [0 for i in range(348)]
    ins2 = [0 for i in range(348)]

    methods = classinfo1.getmethods()

    #######################################
    # pay attention to array cross border #
    #######################################
    for method in methods:
        for i in range(348):
            ins1[i] = ins1[i] + method.getInstruction()[i]

    methods = classinfo2.getmethods()

    for method in methods:
        for i in range(348):
            ins2[i] = ins2[i] + method.getInstruction()[i]

    distance3 = 0
    for i in range(348):
        if(ins1[i] != 0 or ins2[i] != 0):
            distance3 = distance3 + abs(ins1[i] - ins2[i])/(348 * (ins1[i] + ins2[i]))
        else:
            distance3 = distance3 + 1/348
    return distance3

def calculateClassdistance1(classinfo1, classinfo2):
        distance1_calsslist = []
        distance1_calsslist.append(Levenshtein.jaro(classinfo1.getClassname(), classinfo2.getClassname()))
        if(classinfo1.getStaticfieldssize() != 0):
            distance1_calsslist.append(abs(classinfo1.getStaticfieldssize() - classinfo2.getStaticfieldssize())/classinfo1.getStaticfieldssize())
        elif(classinfo2.getStaticfieldssize() == 0):
            distance1_calsslist.append(0)
        else:
            distance1_calsslist.append(1)

        if(classinfo1.getInstancefieldssize() != 0):
            distance1_calsslist.append(abs(classinfo1.getInstancefieldssize() - classinfo2.getInstancefieldssize()) / classinfo1.getInstancefieldssize())
        elif(classinfo2.getInstancefieldssize() == 0):
            distance1_calsslist.append(0)
        else:
            distance1_calsslist.append(1)

        if(classinfo1.getDirectmethodssize() != 0):
            distance1_calsslist.append(abs(classinfo1.getDirectmethodssize() - classinfo2.getDirectmethodssize()) / classinfo1.getDirectmethodssize())
        elif(classinfo2.getDirectmethodssize() == 0):
            distance1_calsslist.append(0)
        else:
            distance1_calsslist.append(1)

        if(classinfo1.getVirtualmethodssize() != 0):
            distance1_calsslist.append(abs(classinfo1.getVirtualmethodssize() - classinfo2.getVirtualmethodssize()) / classinfo1.getVirtualmethodssize())
        elif(classinfo2.getVirtualmethodssize() == 0):
            distance1_calsslist.append(0)
        else:
            distance1_calsslist.append(1)

        if(classinfo1.getInstructionsize() != 0):
            distance1_calsslist.append(abs(classinfo1.getInstructionsize() - classinfo2.getInstructionsize()) / classinfo1.getInstructionsize())
        elif(classinfo2.getInstructionsize() == 0):
            distance1_calsslist.append(0)
        else:
            distance1_calsslist.append(1)

        distance1_class = 0.0
        for i in distance1_calsslist:
            distance1_class = distance1_class + i/6
        return distance1_class


def getMethodsMapping(info1, info2):
    methods1 = info1.getmethods()
    methods2 = info2.getmethods()
    distance = np.zeros((len(methods1), len(methods2)))
    commonlen = min(len(methods1), len(methods2))

    maxNum = 0.0

    for i in range(len(methods1)):
        for j in range(len(methods2)):
            distance[i][j] = calculateMethod(methods1[i], methods2[j])
            if(maxNum < distance[i][j]):
                maxNum = distance[i][j]

    minNum = maxNum
    point = np.zeros((commonlen, 2))

    for m in range(commonlen):
        for i in range(len(methods1)):
            for j in range(len(methods2)):
                if(minNum > distance[i][j] and distance[i][j] != -1):
                    minNum = distance[i][j]
                    point[m][0] = i
                    point[m][1] = j

        for i in range(len(methods1)):
            distance[i][int(point[m][1])] = -1
        for j in range(len(methods2)):
            distance[int(point[m][0])][j] = -1
        minNum = maxNum
    methods = []
    distance1_methodlist = []
    for m in range(commonlen):
        origin = methods1[int(point[m][0])].getMethodname() + methods1[int(point[m][0])].getParatype()
        target = methods2[int(point[m][1])].getMethodname() + methods2[int(point[m][1])].getParatype()
        methodInfo = MappingSingle(origin, target)
        methods.append(methodInfo)
        distance1_methodlist.append(calculateMethoddistance1(methods1[int(point[m][0])], methods2[int(point[m][1])]))
    return methods, distance1_methodlist

def calculateMethoddistance1(methodinfo1, methodinfo2):
    distance1_singlemethodlist = []
    distance1_singlemethodlist.append(Levenshtein.jaro(methodinfo1.getMethodname(), methodinfo2.getMethodname()))
    distance1_singlemethodlist.append(Levenshtein.jaro(methodinfo1.getReturntype(), methodinfo2.getReturntype()))
    if(methodinfo1.getTotalparameter() != 0):
        distance1_singlemethodlist.append(abs(methodinfo1.getTotalparameter() - methodinfo2.getTotalparameter())/methodinfo1.getTotalparameter())
        distance1_singlemethodlist.append(calculateparameter(methodinfo1, methodinfo2) / (methodinfo1.getTotalparameter() + methodinfo2.getTotalparameter()))
    elif(methodinfo2.getTotalparameter() == 0):
        distance1_singlemethodlist.append(0)
        distance1_singlemethodlist.append(0)
    else:
        distance1_singlemethodlist.append(1)
        distance1_singlemethodlist.append(1)

    if(methodinfo1.getMethodLOC() != 0):
        distance1_singlemethodlist.append(abs(methodinfo1.getMethodLOC() - methodinfo2.getMethodLOC())/methodinfo1.getMethodLOC())
    elif(methodinfo2.getMethodLOC() == 0):
        distance1_singlemethodlist.append(0)
    else:
        distance1_singlemethodlist.append(1)

    distance1_method = 0.0
    for i in distance1_singlemethodlist:
        distance1_method = distance1_method + i/5
    return distance1_method

def evaluateClass(point, classinfo1, classinfo2):
    mapping = "../out/Tetrisr8.mapping"



if __name__ == "__main__":
    # r0 is the baseline we don't have to calculate it every time.
    GetR8Dex.getR8Dex(1, 1)   # 1 for randomly chosen
    #GetR8Dex.getR8Dex(2, 100)    # 2 for greedy chosen, this mode the latter integer takes no interest.
    #GetR8Dex.getR8Dex(3, 50)
    #callGraph.callGraph("../output/baseline/scimark0.txt", "../output/baseline/callgraph0.txt")


    # dump1 = "baseline/serial0.txt"
    # dump2 = "plaint1.txt"
    # callgraph1 = "baseline/callgraph0.txt"
    # callgraph2 = "callgraph1.txt"
    # callGraph.callGraph(dump1, callgraph1)
    #
    # getPerDump(dump2)
    # callGraph.callGraph(dump2, callgraph2)
    # classinfo1 = RecordClass.recordClass(dump1)
    # classinfo2 = RecordClass.recordClass(dump2)
    #
    # for i in range(len(classinfo1)):
    #     print(classinfo1[i])
    # for j in range(len(classinfo2)):
    #     print(classinfo2[j])
    #
    # mapping = getMapping(classinfo1, classinfo2)
    # score = GetDistance.getDistance(mapping, callgraph1, callgraph2)
    # print(score)

    # dump1 = "sample_show/plaint0.txt"
    # dump2 = "sample_show/plaint0.txt"
    # callgraph1 = "sample_show/callgraph0.txt"
    # callgraph2 = "sample_show/callgraph0.txt"
    # callGraph.callGraph(dump1, callgraph1)
    # callGraph.callGraph(dump2, callgraph2)
    # classinfo1 = RecordClass.recordClass(dump1)
    # classinfo2 = RecordClass.recordClass(dump2)
    # mapping = getMapping(classinfo1, classinfo2)
    # score = GetDistance.getDistance(mapping, callgraph1, callgraph2)
    # print(score)


    # a = []
    # a.append(1)
    # a.append(3)
    # a.append(5)
    # b = a
    # b[1] = 0
    # print(a)
    # print(b)
    # testarray = [0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1]
    # GetR8Dex.getScore(testarray)

