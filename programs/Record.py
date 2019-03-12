
class MethodInfo(object):

    def __init__(self, Methodtype, Methodname, Returntype, Totalparameter, Paratype, MethodLOC, Instruction):
        self.Methodtype = Methodtype # 0 for virtual methods and 1 for direct methods
        self.Methodname = Methodname
        self.Returntype = Returntype
        self.Totalparameter = Totalparameter
        self.Paratype = Paratype
        self.MethodLOC= MethodLOC
        self.Instruction = Instruction

    def __str__(self):
        if self.Methodtype == 0:
            type = "virtual method"
        else:
            type = "direct method"
        tmp = type + " " + self.Returntype + " " + self.Methodname + ":" + str(self.Totalparameter) \
                + "->" + self.Paratype + " " + str(self.MethodLOC) + " " + str(self.Instruction[92])
        return tmp + '\n'

    def getMethodtype(self):
        if self.Methodtype == 0:
            return "Virtual method"
        else:
            return "Direct method"

    def getMethodname(self):
        return self.Methodname

    def getReturntype(self):
        return self.Returntype

    def getTotalparameter(self):
        return self.Totalparameter

    def getParatype(self):
        return self.Paratype

    def getMethodLOC(self):
        return self.MethodLOC

    def getInstruction(self):
        return self.Instruction

    def setMethodtype(self, type):
        self.Methodtype = type

    def setMethodname(self, Methodname):
        self.Methodname = Methodname

    def setReturntype(self, Returntype):
        self.Returntype = Returntype

    def setTotalparameter(self, Totalparameter):
        self.Totalparameter = Totalparameter

    def setParatype(self, Paratype):
        self.Paratype = Paratype

    def setMethodLOC(self, MethodLOC):
        self.MethodLOC = MethodLOC

    def setInstruction(self, Instruction):
        self.Instruction = Instruction

    def increaseTotalparameter(self):
        self.Totalparameter = self.Totalparameter + 1

    def increaseMethodLOC(self):
        self.MethodLOC = self.MethodLOC + 1

class ClassInfo(object):
    def __init__(self, Classname, Staticfieldssize, Instancefieldssize, Directmethodssize, Virtualmethodssize, Instructionsize, methods):
        self.Classname = Classname
        self.Staticfieldssize = Staticfieldssize
        self.Instancefieldssize = Instancefieldssize
        self.Directmethodssize = Directmethodssize
        self.Virtualmethodssize = Virtualmethodssize
        self.Instructionsize = Instructionsize
        self.methods = methods

    def __str__(self):
        tmp = self.Classname + '\n' + str(self.Staticfieldssize) + " " + str(self.Instancefieldssize) + " " + str(self.Directmethodssize) \
                + " " + str(self.Virtualmethodssize) + " " + str(self.Instructionsize) + '\n'
        for method in self.methods:
            tmp = tmp + method.__str__()
        return tmp + str(len(self.methods))

    def getClassname(self):
        return self.Classname

    def getStaticfieldssize(self):
        return self.Staticfieldssize

    def getInstancefieldssize(self):
        return self.Instancefieldssize

    def getDirectmethodssize(self):
        return self.Directmethodssize

    def getVirtualmethodssize(self):
        return self.Virtualmethodssize

    def getInstructionsize(self):
        return self.Instructionsize

    def getmethods(self):
        return self.methods

class MappingSingle(object):
    def __init__(self, origin, target):           # for methods contain their name and parameters
        self.origin = origin
        self.target = target

    def getorigin(self):
        return self.origin

    def gettarget(self):
        return self.target


class MappingInfo(object):
    def __init__(self, classInfo, methods, distance1, distance3):
        self.classInfo = classInfo
        self.methods = methods
        self.distance1 = distance1
        self.distance3 = distance3

    def __str__(self):
        tmp = self.classInfo.getorigin() + " -> " + self.classInfo.gettarget() + ":\n"
        for i in range(len(self.methods)):
            tmp = tmp + self.methods[i].getorigin() + " -> " + self.methods[i].gettarget() + "\n"
        return tmp

    def getclassInfo(self):
        return self.classInfo

    def getmethods(self):
        return self.methods

    def getdistance1(self):
        return self.distance1

    def getdistance3(self):
        return self.distance3


class RandomInfo(object):
    def __init__(self, choices, score):
        self.choices = choices
        self.score = score

    def getchoices(self):
        return self.choices

    def getscores(self):
        return self.score

    def setchoicesInfo(self, choices):
        self.choices = choices