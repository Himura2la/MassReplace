import os
import sys

rulesFile = "Rules\\rules_cdn.txt"
startPath = "D:\\Docs\\Docs\\Source"
include = {'desc', 'md', 'htm'}
exclude = { }

debug = True
debugDir = "Debug"
winMergePath = "C:\\Program Files (x86)\\WinMerge"

#************** Reading rules **************

srcRules = []
tgtRules = []

with open(rulesFile, "r") as f: lines = f.readlines()
i = 0
for line in lines:
    if line[0] not in {'=', '-'} and len(line) > 3:
        line = line.split("\r")[0].split("\n")[0]
        if i % 2 == 0:
            srcRules.append(line)
        else:
            tgtRules.append(line)
        i += 1
nRules = len(srcRules)
if nRules != len(tgtRules): print("[ERROR!!!] Some lines have no pair. Watch out!"); exit()

print("Rules:")
for i in range(nRules):
    print(srcRules[i])
    print(tgtRules[i])
    print()

#************** Counting files **************

print("[INFO] Counting files...", end="", flush=True)
totalFiles = 0
for root, dirs, files in os.walk(startPath):
    for name in files:
        if name not in exclude:
            path = os.path.join(root, name)
            type = name.split(".")[-1]
            if type in include: 
                totalFiles += 1
print("\r[OK] Total files: ", totalFiles)
currentFile = 0

#************** Let's go replacing! **************

hash = 0
batFileName = "!!! Compare.bat"
batFile = open(os.path.join(debugDir, batFileName), "w")
for root, dirs, files in os.walk(startPath):
    for name in files:
        if name not in exclude:
            path = os.path.join(root, name)
            type = name.split(".")[-1]
            if type in include:
                try:
                    with open(path, "r") as f: source = f.read()
                    temp = source
                    for i in range(nRules): # Check each rule
                        if temp.find(srcRules[i]) > 0:
                            temp = temp.replace(srcRules[i], tgtRules[i])
    
                    if temp != source:
                        target = temp
                        hash += 1
                        if debug:
                            srcPath = name.replace(".", "_src["+str(hash)+"].")
                            tmpSrcPath = os.path.join(debugDir, srcPath)
                            with open(tmpSrcPath, "w") as f: f.write(source)
    
                            tgtPath = name.replace(".", "_tgt["+str(hash)+"].")
                            tmpTgtPath = os.path.join(debugDir, tgtPath)
                            with open(tmpTgtPath, "w") as f: f.write(target)
    
                            batFile.write('start "" ' + 
                                          os.path.join(winMergePath, "WinMergeU.exe") + 
                                          '" /s "' + srcPath + '" "' + tgtPath + '"\n')
                        else:
                            pass
                            #with open(path, "w") as f: f.write(target)  # !!! BEWARE ERRORS !!!!
                    currentFile += 1
                    percentage = currentFile / totalFiles * 100

                    progressString = "\r[" + str(round(percentage)) + "%] " + \
                                     name.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
                    print(progressString.ljust(80 - len(progressString)), end="", flush=True)
                    
                    if currentFile == 1000:
                        raise Exception("oops...")
                    
                except Exception as e:
                    print("\r[ERROR!!!] File: ", path)
                    print("-"*79)
                    print(e)
                    print("-"*79)
print("\r\n[FINISH] " + str(hash) + " files processed")
batFile.close()
