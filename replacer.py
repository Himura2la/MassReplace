import os

rulesFile = "rules_cdn.txt"
startPath = "D:\\Docs\\Docs\\Source"
exclude = { }

debug = True
debugDir = "Debug"

printRules = False
printFiles = False

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
if nRules != len(tgtRules): print("Some lines have no pair. Watch out!"); exit()

if printRules:
    for i in range(nRules):
        print(srcRules[i])
        print(tgtRules[i])
        print()

#************** Let's go replacing! **************

hash = 0
batFileName = "!!! Compare.bat"
batFile = open(os.path.join(debugDir, batFileName), "w")
for root, dirs, files in os.walk(startPath):
    for name in files:
        if name not in exclude:
            path = os.path.join(root, name)
            type = name.split(".")[-1]
            if type in {'desc', 'md', 'htm'}:
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
                            srcPath = name.replace(".", "_src"+str(hash)+".")
                            tmpSrcPath = os.path.join(debugDir, srcPath)
                            with open(tmpSrcPath, "w") as f: f.write(source)
    
                            tgtPath = name.replace(".", "_tgt"+str(hash)+".")
                            tmpTgtPath = os.path.join(debugDir, tgtPath)
                            with open(tmpTgtPath, "w") as f: f.write(target)
    
                            batFile.write('start "" "C:\\Program Files (x86)\\WinMerge\\WinMergeU.exe" /s "' + srcPath + '" "' + tgtPath + '"\n')
                        else:
                            pass
                            #with open(path, "w") as f: f.write(target)  # !!! BEWARE ERRORS !!!!
                    if printFiles: print("[OK] " + name)
                except Exception as e:
                    print("[ERROR!!!] File: ", path)
                    print(e)
print("[FINISH] " + str(hash) + " files processed")
batFile.close()
