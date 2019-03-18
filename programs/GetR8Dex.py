import os
import random
from subprocess import Popen
import GetMapping
import callGraph
import RecordClass
import GetDistance
from Record import RandomInfo
import csv
from GA import GA

def getInstruction():
    instructor = ["" for i in range(19)]

    ##################need to be changed###################################
    instructor[0] = "-injars benchmarks/serial.jar\n"
    instructor[1] = "-outjars out/serial_out.jar\n"
    #####################################################

    instructor[2] = "-libraryjars lib/rt.jar\n-libraryjars lib/charsets.jar\n-libraryjars lib/jce.jar\n-libraryjars lib/jfr.jar\n-libraryjars lib/jsse.jar\n-libraryjars lib/resources.jar\n"
    instructor[7] = "-dontshrink\n"
    instructor[4] = "-dontoptimize\n"
    instructor[5] = "-dontobfuscate\n"
    instructor[6] = "-dontskipnonpubliclibraryclasses\n"
    instructor[3] = "-keepclasseswithmembers class * {\npublic static void main(java.lang.String[]);\n}\n"
    instructor[8] = "-dontskipnonpubliclibraryclassmembers\n"
    instructor[9] = "-target 1.8\n"# use 1.7 for testing temporarily.
    instructor[10] = "-forceprocessing\n"
    instructor[11] = "-keep class ErsBlock {*; }\n"
    instructor[12] = "-dontpreverify\n"
    instructor[13] = "-allowaccessmodification\n"
    instructor[14] = "-mergeinterfacesaggressively\n"   #no interfaces in dexfile.
    instructor[15] = "-useuniqueclassmembernames\n"
    instructor[16] = "-overloadaggressively\n"
    instructor[17] = "-repackageclasses ''\n"
    instructor[18] = "-keepparameternames\n"
    return instructor

def isDone(mark):
    for i in range(len(mark)):
        if(mark[i] == 0):
            return False
    return True


def generateCfg1(length, mark):
    stringCfg = "../Tetris.cfg"
    choices = ""
    if(os.path.exists(stringCfg)):
        os.remove(stringCfg)
    ins = getInstruction()

    for i in range(19):
        mark[i] = 0

    result = ins[0]  + ins[2] + ins[3] + "-ignorewarnings\n"
    mark[0] = mark[1] = mark[2] = mark[3] = 1
    for i in range(length):
        index = random.randint(4, 18)
        while(mark[index] == 1 and (not isDone(mark))):
            index = random.randint(4, 18)
        mark[index] = 1;
    if(mark[4] != 1):
        result = result + ins[4]
    if(mark[5] != 1):
        result = result + ins[5]
    if(mark[6] != 1):
        result = result + ins[6]
    if(mark[7] != 1):
        result = result + ins[7]
    if(mark[8] != 1):
        result = result + ins[8]
    for i in range(15):
        i1 = i + 4
        if(mark[i1] == 1):
            choices = choices + str(i1) + " ";
            if(i1 != 4 and i1 != 5 and i1 != 6 and i1 != 7 and i1 != 8):
                result = result + ins[i1]

    with open(stringCfg, 'w') as config:
        config.write(result)

    return choices

def generateCfg2(iteration):
    stringCfg = "../Tetris.cfg"
    result = ""
    dump1 = "baseline/ErsBlocks0.txt"
    dump2 = "plaint1.txt"
    callgraph1 = "baseline/callgraph0.txt"
    callgraph2 = "callgraph1.txt"
    source = "../out/classes.dex"
    ins = getInstruction()
    choices = 0
    if(iteration == 0):
        if(os.path.exists(stringCfg)):
            os.remove(stringCfg)
        oldresult = ins[0]  + ins[2] + ins[3] + "-ignorewarnings\n" + ins[4] + ins[5] + ins[6] + ins[7] + ins[8]

    else:
        with open(stringCfg, "r") as f:
            lines = f.read()
        oldresult = lines
    record = [0 for i in range(15)]
    for i in range(15):
        i1 = i + 4
        if(i1 == 4 or i1 == 5 or i1 == 6 or i1 == 7 or i1 == 8):
            result = oldresult.replace(ins[i1], "")
        else:
            result = oldresult + ins[i1]

        with open(stringCfg, 'w') as config:
            config.write(result)

        cmd = "java -jar ../r8.jar --release --output ../out --pg-conf " + stringCfg
        p = Popen(cmd, shell=True)
        p.wait()
        if p.returncode != 0:
            print("Error")
            return -1
        p.kill()
        GetMapping.getPerDump(source, dump2)
        # callGraph.callGraph(dump1, callgraph1)
        callGraph.callGraph(dump2, callgraph2)
        classinfo1 = RecordClass.recordClass(dump1)
        classinfo2 = RecordClass.recordClass(dump2)
        mapping = GetMapping.getMapping(classinfo1, classinfo2)
        record[i] = GetDistance.getDistance(mapping, callgraph1, callgraph2)

    Minnum = 100
    Minindex = 0
    for i in range(15):
        if(Minnum > record[i]):
            Minnum = record[i]
            Minindex = i
    i1 = Minindex + 4
    if (i1 == 4 or i1 == 5 or i1 == 6 or i1 == 7 or i1 == 8):
        result = oldresult.replace(ins[i1], "")
    else:
        result = oldresult + ins[i1]
    with open(stringCfg, 'w') as config:
        config.write(result)
    return Minindex + 4

def getScore(tmp, source):
    ####################need to be changed#####################################
    stringCfg = "../Tetris.cfg"
    dump1 = "baseline/dump0.txt"
    dump2 = "plain1.txt"
    callgraph1 = "baseline/callgraph0.txt"
    callgraph2 = "callgraph1.txt"
    log = "trabish.txt"
    source = source[3:]
    ins = getInstruction()
    ins[0] = "-injars " + source + "\n"
    result = ins[0]  + ins[2] + ins[3] + "-ignorewarnings\n" + ins[4] + ins[5] + ins[6] + ins[7] + ins[8]

    for i in range(15):
        i1 = i + 4
        if(tmp[i] == 1):
            if(i1 == 4 or i1 == 5 or i1 == 6 or i1 == 7 or i1 == 8):
                result = result.replace(ins[i1], "")
            else:
                result = result + ins[i1]

    with open(stringCfg, "w") as f:
        f.write(result)

    cmd = "java -jar ../r8.jar --release --output ../out --pg-conf " + stringCfg + ">" + log
    p = Popen(cmd, shell=True)
    p.wait()
    source="../out/classes.dex"
    if p.returncode != 0:
        print("Error")
        return -1
    p.kill()
    GetMapping.getPerDump(source, dump2)
    # callGraph.callGraph(dump1, callgraph1)
    callGraph.callGraph(dump2, callgraph2)
    classinfo1 = RecordClass.recordClass(dump1)
    classinfo2 = RecordClass.recordClass(dump2)
    mapping = GetMapping.getMapping(classinfo1, classinfo2)
    score1, score2, score3 = GetDistance.getDistance(mapping, callgraph1, callgraph2)
    score = score1 + score2 + score3
    return score


def getR8Dex(model, iteration, source, target):
    stringCfg =  "../Tetris.cfg"
    ########################need to be modified when the sample is changed.#################################
    dump1 = "baseline/serial0.txt";
    dump2 = "plaint1.txt";
    callgraph1 = "baseline/callgraph0.txt";
    callgraph2 = "callgraph1.txt";
    source2 = ""

    ###################
    # randomly chosen #
    ###################
    if(model == 1):
        mark = [0 for i in range(19)]  # 0 for unvisited and 1 for visited
        randinfo = [];
        for i in range(iteration):
            source2 = "../out/classes.dex"
            length = random.randint(1, 15)
            choices = generateCfg1(length, mark)
            print(choices)
            cmd = "java -jar ../r8.jar --release --output ../out/" + "/ --pg-conf " + stringCfg
            p = Popen(cmd, shell=True)
            p.wait()
            if p.returncode != 0:
                print("Error")
                return -1
            p.kill()

            GetMapping.getPerDump(source2, dump2)
            callGraph.callGraph(dump2, callgraph2)
            classinfo1 = RecordClass.recordClass(dump1)
            classinfo2 = RecordClass.recordClass(dump2)
            mapping = GetMapping.getMapping(classinfo1, classinfo2)
            score1, score2, score3 = GetDistance.getDistance(mapping, callgraph1, callgraph2)
            print(str(score1) + " " + str(score2) + " " + str(score3))
            randsingle = RandomInfo(choices, score2)
            randinfo.append(randsingle)

        with open("random.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["choices","scores"])
            for i in range(len(randinfo)):
                writer.writerow([randinfo[i].getchoices(), randinfo[i].getscores()])

    #################
    # greedy chosen #
    #################
    elif(model == 2):
        selectioninfo = []
        scores = []
        source = "../out/classes.dex"
        for i in range(10):
            score = 0.0
            selectioninfo.append(generateCfg2(i))
            cmd = "java -jar ../r8.jar --release --output ../out/ --pg-conf " + stringCfg
            p = Popen(cmd, shell=True)
            p.wait()
            if p.returncode != 0:
                print("Error")
                return -1
            p.kill()
            GetMapping.getPerDump(source, dump2)
            # callGraph.callGraph(dump1, callgraph1)
            callGraph.callGraph(dump2, callgraph2)
            classinfo1 = RecordClass.recordClass(dump1)
            classinfo2 = RecordClass.recordClass(dump2)
            mapping = GetMapping.getMapping(classinfo1, classinfo2)
            score = GetDistance.getDistance(mapping, callgraph1, callgraph2)
            scores.append(score)

        with open("greedy.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["choices","scores"])
            for i in range(len(selectioninfo)):
                writer.writerow([selectioninfo[i], scores[i]])
    elif(model == 3):  # ga
        population_size = 20               #default population size is 20 and iteration is 10.
        chromosome_length = 15
        pc = 0.6
        pm = 0.01
        ga = GA(population_size, chromosome_length, pc, pm)
        ga.run(iteration, source, target)
    else:
        print("To be expected")

# def test(testarray):
#
#     classinfo1 = RecordClass.recordClass(dump1)
#     classinfo2 = RecordClass.recordClass(dump2)
#     mapping = GetMapping.getMapping(classinfo1, classinfo2)
#     GetDistance.getDistance(mapping, callgraph1, callgraph2)

def generateBaseline(source):
    # get baseline directory

    # get origin configuration file
    target = "../R80.cfg"
    callgraph = "baseline/callgraph0.txt"
    classfile = "baseline/classes.dex"
    dumpfile = "baseline/dump0.txt"

    instruction = getInstruction()
    source = source[3:]
    instruction[0] = "-injars " + source + "\n"
    cfg_content = instruction[0] + instruction[2] + instruction[3] + instruction[4] + instruction[5] + instruction[6] + \
                  instruction[7] + instruction[8] + instruction[12]
    with open(target, 'w') as originConfig:
        originConfig.write(cfg_content)

    cmd = "java -jar ../r8.jar --release --output baseline" + "/ --pg-conf " + target
    p = Popen(cmd, shell=True)
    p.wait()
    if p.returncode != 0:
        print("Error")
        return -1
    p.kill()

    GetMapping.getPerDump(classfile, dumpfile)
    callGraph.callGraph(dumpfile, callgraph)


def generateCfg(source, target):
    # 1. get baseline directory!
    generateBaseline(source)
    getR8Dex(3, 10, source, target)
    # 2. call main function to get the proper configuration file
    # default number of generation iteration  is 10 and populaiton is 20.

def getCfg(source, tmp, target):
    ins = getInstruction()
    source = source[3:]
    ins[0] = "-injars " + source + "\n"
    result = ins[0] + ins[2] + ins[3] + "-ignorewarnings\n" + ins[4] + ins[5] + ins[6] + ins[7] + ins[8]

    for i in range(15):
        i1 = i + 4
        if (tmp[i] == 1):
            if (i1 == 4 or i1 == 5 or i1 == 6 or i1 == 7 or i1 == 8):
                result = result.replace(ins[i1], "")
            else:
                result = result + ins[i1]

    with open(target, "w") as f:
        f.write(result)



