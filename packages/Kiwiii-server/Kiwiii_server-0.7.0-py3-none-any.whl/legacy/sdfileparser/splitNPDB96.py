# coding: UTF-8

fileInput = '../temp/NPDepoB96.sdf'

query = ""
queryText = ""
ids = []
i = 0
j = 0
content = ""
isRecord = True
repositID = ""
molName = ""
plateID = ""
wellID = ""
isRepositID = False
isMolName = False
isPlateID = False
isWellID = False

for line in open(fileInput, 'rU'):
    if line.startswith('> <repositID>'):
        isRepositID = True
        isRecord = False
        continue
    elif line.startswith('> <MOL_NAME>'):
        isMolName = True
        continue
    elif line.startswith('> <PlateID>'):
        isPlateID = True
        continue
    elif line.startswith('> <WellID>'):
        isWellID = True
        continue
    if isRecord:
        content = content + line
        continue
    elif isRepositID:
        repositID = line.rstrip()
        isRepositID = False
        continue
    elif isMolName:
        molName = line.rstrip()
        isMolName = False
        continue
    elif isPlateID:
        plateID = line.rstrip()
        isPlateID = False
        continue
    elif isWellID:
        content = content + "$$$$\n"
        wellID = line.rstrip()
        queryText = "INSERT INTO NPD (id, reposit_id, mol_name, molecule) VALUES ('" \
            + plateID + wellID + "' , '" + repositID + "' , '" + molName + "' , '" + content + "');"
        query = query + queryText.replace("\n", "\\n") + "\n"
        content = ""
        repositID = ""
        molName = ""
        plateID = ""
        wellID = ""
        isWellID = False
        i += 1
    if line.startswith('$$$$'):
        isRecord = True
    if i == 5200:
        break
f = open("NPD_Query_B96.txt", "w")
f.write(query)
f.close