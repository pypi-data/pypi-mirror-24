# coding: UTF-8

fileInput = '../temp/NPDepoLib_100507.sdf'

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
    if line.startswith('>  <PlateID>'):
        isPlateID = True
        isRecord = False
        continue
    elif line.startswith('>  <WellID>'):
        isWellID = True
        continue
    elif line.startswith('>  <RepositID>'):
        isRepositID = True
        continue
    elif line.startswith('>  <Molname>'):
        isMolName = True
        continue
    if isRecord:
        content = content + line
        continue
    elif isPlateID:
        plateID = line.rstrip()
        isPlateID = False
        continue
    elif isWellID:
        wellID = line.rstrip()
        isWellID = False
        continue
    elif isRepositID:
        repositID = line.rstrip()
        isRepositID = False
        continue
    elif isMolName:
        if i >= 12500:
            content = content + "$$$$\n"
            molName = line.rstrip()
            molName = molName.replace("\'", "\\'")
            molName = molName.replace("\"", "")
            queryText = "INSERT INTO NPD (id, reposit_id, mol_name, molecule) VALUES ('" \
                + plateID + wellID + "' , '" + repositID + "' , '" + molName + "' , '" + content + "');"
            query = query + queryText.replace("\n", "\\n") + "\n"
        content = ""
        repositID = ""
        molName = ""
        plateID = ""
        wellID = ""
        isMolName = False
        i += 1
    if line.startswith('$$$$'):
        isRecord = True
    if i == 15000:
        break
f = open("NPD_Query_Lib.txt", "w")
f.write(query)
f.close