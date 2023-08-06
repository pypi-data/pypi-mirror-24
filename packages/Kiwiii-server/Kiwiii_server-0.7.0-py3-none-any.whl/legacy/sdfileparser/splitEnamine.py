# coding: UTF-8

fileInput = '../temp/Enamine1190.sdf'

query = ""
queryText = ""
content = ""
i = 0
isRecord = True
repositID = ""
molName = ""
isRepositID = False
isMolName = False

for line in open(fileInput, 'rU'):
    if line.startswith('>  <IDNUMBER>'):
        isMolName = True
        isRecord = False
        continue
    elif line.startswith('>  <repositID>'):
        isRepositID = True
        continue
    if isRecord:
        content = content + line
        continue
    elif isMolName:
        molName = line.rstrip()
        isMolName = False
        continue
    elif isRepositID:
        content = content + "$$$$\n"
        repositID = line.rstrip()
        queryText = "INSERT INTO FRAGMENT (reposit_id, mol_name, molecule) VALUES ('" \
            + repositID + "' , '" + molName + "' , '" + content + "');"
        query = query + queryText.replace("\n", "\\n") + "\n"
        content = ""
        repositID = ""
        molName = ""
        isRepositID = False
        i += 1
    if line.startswith('$$$$'):
        isRecord = True
    if i == 2000:
        break
f = open("Enamine.txt", "w")
f.write(query)
f.close