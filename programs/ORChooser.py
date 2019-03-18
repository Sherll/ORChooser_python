import GetR8Dex
import sys,getopt,optparse
import os
from subprocess import Popen

def getargvdic(argv):
    optd = {}
    while argv:
        if argv[0][0] == '-':
            if len(argv) != 1:
                optd[argv[0]] = argv[1]
                argv = argv[2:]
            else:
                optd[argv[0]] = ""
                argv = argv[1:]
        else:
            argv = argv[1:]
    return optd

def printUsage():
    print("Usage: ORChooser [options] -d <input-files>")
    print(" where <input-files> is the program waiting to be obfuscated and it must be jar files and options are:")
    print("-j <file>        #The output file is obfuscated dalvik bytecode.")
    print("-o <file>        #The output file is obfuscationg configuration file with .cfg as the form.")

def generateJars(source, target):
    #target should be a directory.
    cfgfileName = "../proper.cfg"
    generateCfg(source, cfgfileName)
    cmd = "java -jar ../r8.jar --release --output " + target + " --pg-conf " + cfgfileName
    p = Popen(cmd, shell=True)
    p.wait()
    if p.returncode != 0:
        print("Error")
        return -1
    p.kill()
    print("The final program has written to " + os.path.abspath(target))

def generateCfg(source, target):
    if '.jar' not in source:
        print("Error! Input file must be jar files!")
        return
    else:
        GetR8Dex.generateCfg(source, target)
        print("The final file has written to " + os.path.abspath(target))

def inputError(type, target):
    if type == 0:
        print("Ilegal input!")
    else:
        print("Wrong format of output file " + target + "!")

if __name__ == "__main__":
    # r0 is the baseline we don't have to calculate it every time.
    argv = sys.argv
    mydic = getargvdic(argv)
    if '-h' in mydic.keys():
        printUsage()
    elif '-j' in mydic.keys():
        source = mydic['-d']
        target = mydic['-j']
        generateJars(source, target)
    elif '-o' in mydic.keys():
        source = mydic['-d']
        target = mydic['-o']
        if '.cfg' not in target:
            inputError(2, target)
        else:
            generateCfg(source, target)
    else:
        inputError(0, "error1")




#    GetR8Dex.getR8Dex(1, 1)   # 1 for randomly chosen
