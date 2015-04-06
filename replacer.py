import os

rulesFile = "rules.txt"
startPath = "D:\\Docs\\Docs\\Source\\14_2"
printrules = False

debug = True
tempdir = "temp"

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
if nRules != len(tgtRules): print("Not all lines has a pair. Watch out!"); exit()

if printrules:
    for i in range(nRules):
        print(srcRules[i])
        print(tgtRules[i])
        print()

#************** Let's go replacing! **************

hash = 0
batFileName = "!!!Compare.bat"
batFile = open(os.path.join(tempdir, batFileName), "w")
for root, dirs, files in os.walk(startPath):
    for name in files:
        path = os.path.join(root, name)
        type = name.split(".")[-1]
        if type in {'desc', 'md', 'htm'}:
            with open(path, "r") as f: source = f.read()
            temp = source
            for i in range(nRules): # Check each rule
                if temp.find(srcRules[i]) > 0:
                    temp = temp.replace(srcRules[i], tgtRules[i])

            if temp != source:
                target = temp
                hash += 1
                if debug:
                    tmpSrcPath = os.path.join(tempdir, name.replace(".", "_src"+str(hash)+"."))
                    with open(tmpSrcPath, "w") as f: f.write(source)

                    tmpTgtPath = os.path.join(tempdir, name.replace(".", "_tgt"+str(hash)+"."))
                    with open(tmpTgtPath, "w") as f: f.write(target)

                    batFile.write('start "" "C:\\Program Files (x86)\\WinMerge\\WinMergeU.exe" /s "' + tmpSrcPath + '" "' + tmpTgtPath + '"\n')

                #else: with open(path, "w") as f: f.write(target)  # !!! BEWARE ERRORS !!!!

                print("[OK] " + name)
print("[FINISH] " + str(hash) + " files processed")
batFile.close()
