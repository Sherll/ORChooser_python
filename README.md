# ORChooser_new：A simple tool for obfuscation recommandation
ORChooser is a tool for recommending obfuscation rules for bytecode obfuscators. Bytecode obfuscation is an essential technique for protecting intellectual property and defending against Man-At-The-End(MATE) attacks 
to Java/Android applications. **ProGuard** is the most widely used Java bytecode obfuscator. **Android R8** is a newly launched Java 
obfuscator to replace ProGuard while developing Android application. By now, ORChooser works will for the two.
***
## Functions & Usage

ORChooser takes original program as input, finally give out the most proper configuration file for corresponding Java obfuscator. This tool can be used with two modes and the specific command can be got with '-h':

>python3 programs/ORChooser.py -h 

>python3 programs/ORChooser.py -j Result/ -d ../benchmarks/Compress.jar

>python3 programs/ORChooser.py -o Test.cfg -d ../benchmarks/Compress.jar

'-j' means the final file is obfuscated dalvik bytecode and it will be stored into a directory.
'-o' means the final file is the obfuscated configuration file
'-d' is used to indicate the source file and it must be a '.jar' file.
