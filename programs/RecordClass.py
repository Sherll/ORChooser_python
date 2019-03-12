from Record import MethodInfo
from Record import ClassInfo

def isBasictype(chr):
    if(chr == 'Z'):
        result = "boolean"
    elif(chr == 'B'):
        result = "byte"
    elif(chr == 'S'):
        result = "short"
    elif(chr == 'C'):
        result = "char"
    elif(chr == 'I'):
        result = "int"
    elif(chr == 'J'):
        result = "long"
    elif(chr == 'F'):
        result = "float"
    elif(chr == 'D'):
        result = "double"
    elif(chr == 'V'):
        result = "void"
    else:
        result = None
    return result

def calculate(Paratype):
    if(len(Paratype) == 0):
        return 0
    else:
        sum = 0
        lists = Paratype.split(',')
        if(len(lists) == 1):
            tmp = lists[0]
            for chr in tmp:
                if(isBasictype(chr) != None):
                    sum = sum + 1
                elif(chr == 'L'):
                    sum = sum + 1
                    break
        else:
            for list in lists:
                sum = sum + calculate(list)
        return sum

def collectClass(lists):
    flag = -1 #0 for class header field to record Staticfieldssize, Instancefieldssize, Directmethodssize
                #and Virtualmethodssize; 1 for class fields, class description to record classname; 2 for
                  #methods fields to record Instructionsize and instruction fields while the line contains
                    #'|' .
    Classinfo = []
    # Class field
    Classname = ""
    Staticfieldssize = 0
    Instancefieldssize = 0
    Directmethodssize = 0
    Virtualmethodssize = 0
    Instructionsize = 0
    methods = []

    #Method field
    Methodtype = -1
    Methodname = ""
    Returntype = ""
    Totalparameter = 0
    Paratype = ""
    MethodLOC = 0
    Instruction = [0 for i in range(348)]
    for i in range(348):
        Instruction[i] = 0

    count = 0
    Isthefirst = -1
    for list in lists:
        count = count + 1
        if(list.find("Class #") != -1 and list.find("header:") != -1):
            flag = 0
            if (Methodname != ""):
                method = MethodInfo(Methodtype, Methodname, Returntype, Totalparameter, Paratype, MethodLOC,
                                    Instruction)
                methods.append(method)
                # print(Methodname)

                #######################Method
                Methodtype = -1
                Methodname = ""
                Returntype = ""
                Totalparameter = 0
                Paratype = ""
                MethodLOC = 0
                Instruction = [0 for i in range(348)]
                for i in range(348):
                    Instruction[i] = 0

            if(Classname != ""):
                classinfo = ClassInfo(Classname, Staticfieldssize, Instancefieldssize, Directmethodssize, Virtualmethodssize, Instructionsize, methods)
                Classinfo.append(classinfo)

                Classname = ""
                Staticfieldssize = 0
                Instancefieldssize = 0
                Directmethodssize = 0
                Virtualmethodssize = 0
                Instructionsize = 0
                methods = []

        if(flag == 0 and list.find("static_fields_size") != -1):
            tmplist = list.split(": ")
            Staticfieldssize = int(tmplist[1])
        if(flag == 0 and list.find("instance_fields_size") != -1):
            tmplist = list.split(": ")
            Instancefieldssize = int(tmplist[1])
        if(flag == 0 and list.find("direct_methods_size") != -1):
            tmplist = list.split(": ")
            Directmethodssize = int(tmplist[1])
        if(flag == 0 and list.find("virtual_methods_size") != -1):
            tmplist = list.split(": ")
            Virtualmethodssize = int(tmplist[1])
        if(list.find("Class #") != -1 and list.find("-") != -1):
            flag = 1
        if(flag == 1 and list.find("Class descriptor") != -1):
            tmplist = list.split(": ")
            Classname = tmplist[1][2: -2]
        if(list.find("Direct methods") != -1 or list.find("Virtual methods") != -1):
            if(Methodname != ""):
                method = MethodInfo(Methodtype, Methodname, Returntype, Totalparameter, Paratype, MethodLOC,
                                    Instruction)
                methods.append(method)

                #######################Method
                # Methodtype = -1##########################manage it
                Methodname = ""
                Returntype = ""
                Totalparameter = 0
                Paratype = ""
                MethodLOC = 0
                Instruction = [0 for i in range(348)]
                for i in range(348):
                    Instruction[i] = 0

            flag = 2
            if(list.find("Direct methods") != -1):
                Methodtype = 1
            else:
                Methodtype = 0
        if(flag == 2 and list.find("name") != -1 and list.find("|") == -1):
            if(Methodname != ""):
                method = MethodInfo(Methodtype, Methodname, Returntype, Totalparameter, Paratype, MethodLOC, Instruction)
                methods.append(method)

                #######################Method
                #Methodtype = -1##########################manage it
                Methodname = ""
                Returntype = ""
                Totalparameter = 0
                Paratype = ""
                MethodLOC = 0
                Instruction = [0 for i in range(348)]
                for i in range(348):
                    Instruction[i] = 0
            tmplist = list.split(": ")
            Methodname = tmplist[1][1: -1]

        if(flag == 2 and list.find("type") != -1 and list.find('|') == -1):
            tmplist = list.split(": ")
            tmplist = tmplist[1].split(")")
            Returntype = tmplist[1][0: -1]
            if(Returntype[-1:] == ';'):
                Returntype = Returntype[0: -1]
            if(len(tmplist[0]) == 2):
                Paratype = "()"
            else:
               if(tmplist[0][-1: ] == ";"):
                   tmp = tmplist[0][1: -1] + ')'
                   tmp = tmp.replace(';', ',')
                   Paratype = tmp
               else:
                   tmp = tmplist[0][1:] + ')'
                   tmp = tmp.replace(';', ',')
                   Paratype = tmp
            Totalparameter = calculate(Paratype[1:-1])
        if(flag == 2 and list.find("insns size") != -1):
            tmplist = list.split(": ")
            tmplist = tmplist[1].split(" ")
            Instructionsize = Instructionsize + int(tmplist[0])
        if(flag == 2 and list.find("|") != -1 and list.find(" units)") == -1):
            MethodLOC = MethodLOC + 1
            fillInstruction(Instruction, list)
        if(len(lists) == count):
            method = MethodInfo(Methodtype, Methodname, Returntype, Totalparameter, Paratype, MethodLOC, Instruction)
            methods.append(method)

            classinfo = ClassInfo(Classname, Staticfieldssize, Instancefieldssize, Directmethodssize, Virtualmethodssize, Instructionsize, methods)
            Classinfo.append(classinfo)
    return Classinfo


def fillInstruction(Instruction, list):
    dex = returndex(list)
    if(dex == -1):
        return
    Instruction[dex] = Instruction[dex] + 1

def returndex(list):
    tmplist = list.split("|")
    if(tmplist[1].find(": ") == -1):
        return -1
    tmplist = tmplist[1].split(": ")
    tmplist = tmplist[1].split(" ")
    tmp = tmplist[0]
    if(tmp == "nop"):
        return 0
    elif(tmp == "move"):
        return 1
    elif(tmp == "move/from16"):
        return 2
    elif(tmp == "move/16"):
        return 3
    elif(tmp == "move-wide"):
        return 4
    elif(tmp == "move-wide/from16"):
        return 5
    elif(tmp == "move-object"):
        return 6
    elif(tmp == "move-object/from16"):
        return 7
    elif(tmp == "move-object/16"):
        return 8
    elif(tmp == "move-result"):
        return 9
    elif(tmp == "move-result-wide"):
        return 10
    elif(tmp == "move-result-object"):
        return 11
    elif(tmp == "move-exception"):
        return 12
    elif(tmp == "return-void"):
        return 13
    elif(tmp == "return"):
        return 14
    elif(tmp == "return-wide"):
        return 15
    elif(tmp == "return-object"):
        return 16
    elif(tmp == "const/4"):
        return 17
    elif(tmp == "const/16"):
        return 18
    elif(tmp == "const"):
        return 19
    elif(tmp == "const/high16"):
        return 20
    elif(tmp == "const-wide/16"):
        return 21
    elif(tmp == "const-wide/32"):
        return 22
    elif(tmp == "const-wide"):
        return 23
    elif(tmp == "const-wide/high16"):
        return 24
    elif(tmp == "const-string"):
        return 25
    elif(tmp == "const-string/jumbo"):
        return 26
    elif(tmp == "const-class"):
        return 27
    elif(tmp == "const-class/jumbo"):
        return 28
    elif(tmp == "monitor-enter"):
        return 29
    elif(tmp == "monitor-exit"):
        return 30
    elif(tmp == "check-cast"):
        return 31
    elif(tmp == "instance-of"):
        return 32
    elif(tmp == "new-instance"):
        return 33
    elif(tmp == "check-cast/jumbo"):
        return 34
    elif(tmp == "instance-of/jumbo"):
        return 35
    elif(tmp == "new-instance/jumbo"):
        return 36
    elif(tmp == "array-length"):
        return 37
    elif(tmp == "new-array"):
        return 38
    elif(tmp == "filled-new-array"):
        return 39
    elif(tmp == "filled-new-array/range"):
        return 40
    elif(tmp == "fill-array-data"):
        return 41
    elif(tmp == "new-array/jumbo"):
        return 42
    elif(tmp == "filled-new-array/jumbo"):
        return 43
    elif(tmp == "aget"):
        return 44
    elif(tmp == "aget-wide"):
        return 45
    elif(tmp == "aget-object"):
        return 46
    elif(tmp == "aget-boolean"):
        return 47
    elif(tmp == "aget-byte"):
        return 48
    elif(tmp == "aget-char"):
        return 49
    elif(tmp == "aget-short"):
        return 50
    elif(tmp == "aput"):
        return 51
    elif(tmp == "aput-wide"):
        return 52
    elif(tmp == "aput-object"):
        return 53
    elif(tmp == "aput-boolean"):
        return 54
    elif(tmp == "aput-byte"):
        return 55
    elif(tmp == "aput-char"):
        return 56
    elif(tmp == "aput-short"):
        return 57
    elif(tmp == "throw"):
        return 58
    elif(tmp == "goto"):
        return 59
    elif(tmp == "goto/16"):
        return 60
    elif(tmp == "goto/32"):
        return 61
    elif(tmp == "packed-switch"):
        return 62
    elif(tmp == "sparse-switch"):
        return 63
    elif(tmp == "if-test"):
        return 64
    elif(tmp == "if-eq"):
        return 65
    elif(tmp == "if-ne"):
        return 66
    elif(tmp == "if-lt"):
        return 67
    elif(tmp == "if-ge"):
        return 68
    elif(tmp == "if-gt"):
        return 69
    elif(tmp == "if-le"):
        return 70
    elif(tmp == "if-testz"):
        return 71
    elif(tmp == "if-eqz"):
        return 72
    elif(tmp == "if-nez"):
        return 73
    elif(tmp == "if-ltz"):
        return 74
    elif(tmp == "if-gez"):
        return 75
    elif(tmp == "if-gtz"):
        return 76
    elif(tmp == "if-lez"):
        return 77
    elif(tmp == "cmpl-float"):
        return 78
    elif(tmp == "cmpg-float"):
        return 79
    elif(tmp == "cmpl-double"):
        return 80
    elif(tmp == "cmpg-double"):
        return 81
    elif(tmp == "cmp-long"):
        return 82
    elif(tmp == "iget"):
        return 83
    elif(tmp == "iget-wide"):
        return 84
    elif(tmp == "iget-object"):
        return 85
    elif(tmp == "iget-boolean"):
        return 86
    elif(tmp == "iget-byte"):
        return 87
    elif(tmp == "iget-char"):
        return 88
    elif(tmp == "iget-short"):
        return 89
    elif(tmp == "iput"):
        return 90
    elif(tmp == "iput-wide"):
        return 91
    elif(tmp == "iput-object"):
        return 92
    elif(tmp == "iput-boolean"):
        return 93
    elif(tmp == "iput-byte"):
        return 94
    elif(tmp == "iput-char"):
        return 95
    elif(tmp == "iput-short"):
        return 96
    elif (tmp == "sget"):
        return 97
    elif (tmp == "sget-wide"):
        return 98
    elif (tmp == "sget-object"):
        return 99
    elif (tmp == "sget-boolean"):
        return 100
    elif (tmp == "sget-byte"):
        return 101
    elif (tmp == "sget-char"):
        return 102
    elif (tmp == "sget-short"):
        return 103
    elif (tmp == "sput"):
        return 104
    elif (tmp == "sput-wide"):
        return 105
    elif (tmp == "sput-object"):
        return 106
    elif (tmp == "sput-boolean"):
        return 107
    elif (tmp == "sput-byte"):
        return 108
    elif (tmp == "sput-char"):
        return 109
    elif (tmp == "sput-short"):
        return 110
    elif (tmp == "iget/jumbo"):
        return 111
    elif (tmp == "iget-wide/jumbo"):
        return 112
    elif (tmp == "iget-object/jumbo"):
        return 113
    elif (tmp == "iget-boolean/jumbo"):
        return 114
    elif (tmp == "iget-byte/jumbo"):
        return 115
    elif (tmp == "iget-char/jumbo"):
        return 116
    elif (tmp == "iget-short/jumbo"):
        return 117
    elif (tmp == "iput/jumbo"):
        return 118
    elif (tmp == "iput-wide/jumbo"):
        return 119
    elif (tmp == "iput-object/jumbo"):
        return 120
    elif (tmp == "iput-boolean/jumbo"):
        return 121
    elif (tmp == "iput-byte/jumbo"):
        return 122
    elif (tmp == "iput-char/jumbo"):
        return 123
    elif (tmp == "iput-short/jumbo"):
        return 124
    elif (tmp == "sget/jumbo"):
        return 125
    elif (tmp == "sget-wide/jumbo"):
        return 126
    elif (tmp == "sget-object/jumbo"):
        return 127
    elif (tmp == "sget-boolean/jumbo"):
        return 128
    elif (tmp == "sget-byte/jumbo"):
        return 129
    elif (tmp == "sget-char/jumbo"):
        return 130
    elif (tmp == "sget-short/jumbo"):
        return 131
    elif (tmp == "sput/jumbo"):
        return 132
    elif (tmp == "sput-wide/jumbo"):
        return 133
    elif (tmp == "sput-object/jumbo"):
        return 134
    elif (tmp == "sput-boolean/jumbo"):
        return 135
    elif (tmp == "sput-byte/jumbo"):
        return 136
    elif (tmp == "sput-char/jumbo"):
        return 137
    elif (tmp == "sput-short/jumbo"):
        return 138
    elif(tmp == "invoke-virtual" or tmp == "invoke-virtual/range"):
        return 139
    elif(tmp == "invoke-super" or tmp == "invoke-super/range"):
        return 140
    elif(tmp == "invoke-direct" or tmp == "invoke-direct/range"):
        return 141
    elif(tmp == "invoke-static" or tmp == "invoke-static/range"):
        return 142
    elif(tmp == "invoke-interface" or tmp == "invoke-interface/range"):
        return 143
    elif (tmp == "invoke-virtual/jumbo"):
        return 144
    elif (tmp == "invoke-super/jumbo"):
        return 145
    elif (tmp == "invoke-direct/jumbo"):
        return 146
    elif (tmp == "invoke-static/jumbo"):
        return 147
    elif (tmp == "invoke-interface/jumbo"):
        return 148
    elif(tmp == "neg-int"):
        return 149
    elif(tmp == "not-int"):
        return 150
    elif(tmp == "neg-long"):
        return 151
    elif(tmp == "not-long"):
        return 152
    elif(tmp == "neg-float"):
        return 153
    elif(tmp == "neg-double"):
        return 154
    elif(tmp == "int-to-long"):
        return 155
    elif(tmp == "int-to-float"):
        return 156
    elif(tmp == "int-to-double"):
        return 157
    elif(tmp == "long-to-int"):
        return 158
    elif(tmp == "long-to-float"):
        return 159
    elif(tmp == "long-to-double"):
        return 160
    elif(tmp == "float-to-int"):
        return 161
    elif(tmp == "float-to-long"):
        return 162
    elif(tmp == "float-to-double"):
        return 163
    elif(tmp == "double-to-int"):
        return 164
    elif(tmp == "double-to-long"):
        return 165
    elif(tmp == "double-to-float"):
        return 166
    elif(tmp == "int-to-byte"):
        return 167
    elif(tmp == "int-to-char"):
        return 168
    elif(tmp == "int-to-short"):
        return 169
    elif(tmp == "add-int"):
        return 170
    elif(tmp == "sub-int"):
        return 171
    elif(tmp == "mul-int"):
        return 172
    elif(tmp == "div-int"):
        return 173
    elif(tmp == "rem-int"):
        return 174
    elif(tmp == "and-int"):
        return 175
    elif(tmp == "or-int"):
        return 176
    elif(tmp == "xor-int"):
        return 177
    elif(tmp == "shl-int"):
        return 178
    elif(tmp == "shr-int"):
        return 179
    elif(tmp == "ushr-int"):
        return 180
    elif (tmp == "add-long"):
        return 181
    elif (tmp == "sub-long"):
        return 182
    elif (tmp == "mul-long"):
        return 183
    elif (tmp == "div-long"):
        return 184
    elif (tmp == "rem-long"):
        return 185
    elif (tmp == "and-long"):
        return 186
    elif (tmp == "or-long"):
        return 187
    elif (tmp == "xor-long"):
        return 188
    elif (tmp == "shl-long"):
        return 189
    elif (tmp == "shr-long"):
        return 190
    elif (tmp == "ushr-long"):
        return 191
    elif (tmp == "add-float"):
        return 192
    elif (tmp == "sub-float"):
        return 193
    elif (tmp == "mul-float"):
        return 194
    elif (tmp == "div-float"):
        return 195
    elif (tmp == "rem-float"):
        return 196
    elif (tmp == "and-float"):
        return 197
    elif (tmp == "or-float"):
        return 198
    elif (tmp == "xor-float"):
        return 199
    elif (tmp == "shl-float"):
        return 200
    elif (tmp == "shr-float"):
        return 201
    elif (tmp == "ushr-float"):
        return 202
    elif (tmp == "add-double"):
        return 203
    elif (tmp == "sub-double"):
        return 204
    elif (tmp == "mul-double"):
        return 205
    elif (tmp == "div-double"):
        return 206
    elif (tmp == "rem-double"):
        return 207
    elif (tmp == "and-double"):
        return 208
    elif (tmp == "or-double"):
        return 209
    elif (tmp == "xor-double"):
        return 210
    elif (tmp == "shl-double"):
        return 211
    elif (tmp == "shr-double"):
        return 212
    elif (tmp == "ushr-double"):
        return 213
    elif (tmp == "add-int/2addr"):
        return 214
    elif (tmp == "sub-int/2addr"):
        return 215
    elif (tmp == "mul-int/2addr"):
        return 216
    elif (tmp == "div-int/2addr"):
        return 217
    elif (tmp == "rem-int/2addr"):
        return 218
    elif (tmp == "and-int/2addr"):
        return 219
    elif (tmp == "or-int/2addr"):
        return 220
    elif (tmp == "xor-int/2addr"):
        return 221
    elif (tmp == "shl-int/2addr"):
        return 222
    elif (tmp == "shr-int/2addr"):
        return 223
    elif (tmp == "ushr-int/2addr"):
        return 224
    elif (tmp == "add-long/2addr"):
        return 225
    elif (tmp == "sub-long/2addr"):
        return 226
    elif (tmp == "mul-long/2addr"):
        return 227
    elif (tmp == "div-long/2addr"):
        return 228
    elif (tmp == "rem-long/2addr"):
        return 229
    elif (tmp == "and-long/2addr"):
        return 230
    elif (tmp == "or-long/2addr"):
        return 231
    elif (tmp == "xor-long/2addr"):
        return 232
    elif (tmp == "shl-long/2addr"):
        return 233
    elif (tmp == "shr-long/2addr"):
        return 234
    elif (tmp == "ushr-long/2addr"):
        return 235
    elif (tmp == "add-float/2addr"):
        return 236
    elif (tmp == "sub-float/2addr"):
        return 237
    elif (tmp == "mul-float/2addr"):
        return 238
    elif (tmp == "div-float/2addr"):
        return 239
    elif (tmp == "rem-float/2addr"):
        return 240
    elif (tmp == "and-float/2addr"):
        return 241
    elif (tmp == "or-float/2addr"):
        return 242
    elif (tmp == "xor-float/2addr"):
        return 243
    elif (tmp == "shl-float/2addr"):
        return 244
    elif (tmp == "shr-float/2addr"):
        return 245
    elif (tmp == "ushr-float/2addr"):
        return 246
    elif (tmp == "add-double/2addr"):
        return 247
    elif (tmp == "sub-double/2addr"):
        return 248
    elif (tmp == "mul-double/2addr"):
        return 249
    elif (tmp == "div-double/2addr"):
        return 250
    elif (tmp == "rem-double/2addr"):
        return 251
    elif (tmp == "and-double/2addr"):
        return 252
    elif (tmp == "or-double/2addr"):
        return 253
    elif (tmp == "xor-double/2addr"):
        return 254
    elif (tmp == "shl-double/2addr"):
        return 255
    elif (tmp == "shr-double/2addr"):
        return 256
    elif (tmp == "ushr-double/2addr"):
        return 257
    elif (tmp == "add-int/lit16"):
        return 258
    elif (tmp == "sub-int/lit16"):
        return 259
    elif (tmp == "mul-int/lit16"):
        return 260
    elif (tmp == "div-int/lit16"):
        return 261
    elif (tmp == "rem-int/lit16"):
        return 262
    elif (tmp == "and-int/lit16"):
        return 263
    elif (tmp == "or-int/lit16"):
        return 264
    elif (tmp == "xor-int/lit16"):
        return 265
    elif (tmp == "shl-int/lit16"):
        return 266
    elif (tmp == "shr-int/lit16"):
        return 267
    elif (tmp == "ushr-int/lit16"):
        return 268
    elif (tmp == "add-long/lit16"):
        return 269
    elif (tmp == "sub-long/lit16"):
        return 270
    elif (tmp == "mul-long/lit16"):
        return 271
    elif (tmp == "div-long/lit16"):
        return 272
    elif (tmp == "rem-long/lit16"):
        return 273
    elif (tmp == "and-long/lit16"):
        return 274
    elif (tmp == "or-long/lit16"):
        return 275
    elif (tmp == "xor-long/lit16"):
        return 276
    elif (tmp == "shl-long/lit16"):
        return 277
    elif (tmp == "shr-long/lit16"):
        return 278
    elif (tmp == "ushr-long/lit16"):
        return 279
    elif (tmp == "add-float/lit16"):
        return 280
    elif (tmp == "sub-float/lit16"):
        return 281
    elif (tmp == "mul-float/lit16"):
        return 282
    elif (tmp == "div-float/lit16"):
        return 283
    elif (tmp == "rem-float/lit16"):
        return 284
    elif (tmp == "and-float/lit16"):
        return 285
    elif (tmp == "or-float/lit16"):
        return 286
    elif (tmp == "xor-float/lit16"):
        return 287
    elif (tmp == "shl-float/lit16"):
        return 288
    elif (tmp == "shr-float/lit16"):
        return 289
    elif (tmp == "ushr-float/lit16"):
        return 290
    elif (tmp == "add-double/lit16"):
        return 291
    elif (tmp == "sub-double/lit16"):
        return 292
    elif (tmp == "mul-double/lit16"):
        return 293
    elif (tmp == "div-double/lit16"):
        return 294
    elif (tmp == "rem-double/lit16"):
        return 295
    elif (tmp == "and-double/lit16"):
        return 296
    elif (tmp == "or-double/lit16"):
        return 297
    elif (tmp == "xor-double/lit16"):
        return 298
    elif (tmp == "shl-double/lit16"):
        return 299
    elif (tmp == "shr-double/lit16"):
        return 300
    elif (tmp == "ushr-double/lit16"):
        return 301
    elif (tmp == "add-int/lit8"):
        return 302
    elif (tmp == "sub-int/lit8"):
        return 303
    elif (tmp == "mul-int/lit8"):
        return 304
    elif (tmp == "div-int/lit8"):
        return 305
    elif (tmp == "rem-int/lit8"):
        return 306
    elif (tmp == "and-int"):
        return 307
    elif (tmp == "or-int/lit8"):
        return 308
    elif (tmp == "xor-int/lit8"):
        return 309
    elif (tmp == "shl-int/lit8"):
        return 310
    elif (tmp == "shr-int/lit8"):
        return 311
    elif (tmp == "ushr-int/lit8"):
        return 312
    elif (tmp == "add-long/lit8"):
        return 313
    elif (tmp == "sub-long/lit8"):
        return 314
    elif (tmp == "mul-long/lit8"):
        return 315
    elif (tmp == "div-long/lit8"):
        return 316
    elif (tmp == "rem-long/lit8"):
        return 317
    elif (tmp == "and-long/lit8"):
        return 318
    elif (tmp == "or-long/lit8"):
        return 319
    elif (tmp == "xor-long/lit8"):
        return 320
    elif (tmp == "shl-long/lit8"):
        return 321
    elif (tmp == "shr-long/lit8"):
        return 322
    elif (tmp == "ushr-long/lit8"):
        return 323
    elif (tmp == "add-float/lit8"):
        return 324
    elif (tmp == "sub-float/lit8"):
        return 325
    elif (tmp == "mul-float/lit8"):
        return 326
    elif (tmp == "div-float/lit8"):
        return 327
    elif (tmp == "rem-float/lit8"):
        return 328
    elif (tmp == "and-float/lit8"):
        return 329
    elif (tmp == "or-float/lit8"):
        return 330
    elif (tmp == "xor-float/lit8"):
        return 331
    elif (tmp == "shl-float/lit8"):
        return 332
    elif (tmp == "shr-float/lit8"):
        return 333
    elif (tmp == "ushr-float/lit8"):
        return 334
    elif (tmp == "add-double/lit8"):
        return 335
    elif (tmp == "sub-double/lit8"):
        return 336
    elif (tmp == "mul-double/lit8"):
        return 337
    elif (tmp == "div-double/lit8"):
        return 338
    elif (tmp == "rem-double/lit8"):
        return 339
    elif (tmp == "and-double/lit8"):
        return 340
    elif (tmp == "or-double/lit8"):
        return 341
    elif (tmp == "xor-double/lit8"):
        return 342
    elif (tmp == "shl-double/lit8"):
        return 343
    elif (tmp == "shr-double/lit8"):
        return 344
    elif (tmp == "ushr-double/lit8"):
        return 345
    elif(tmp == "rsub-int/lit8"):
        return 346
    elif(tmp == "and-int/lit8"):
        return 347
    # elif(tmp == "packed-switch-data"):
    #     return 346
    else:
        print(tmp)
        return -1





def recordClass(inputfile):
    with open(inputfile, 'r') as f:
        lines = f.readlines()
    lists = []
    for line in lines:
        lists.append(line[0: -1])
    return collectClass(lists)

