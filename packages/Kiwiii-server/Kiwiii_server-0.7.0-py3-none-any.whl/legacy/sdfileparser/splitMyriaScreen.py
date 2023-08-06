# coding: UTF-8

fileInput = 'MyriaScreenII_PO3007566324.sdf'

query = ""
queryText = ""
content = ""
i = 0
isRecord = True
id_ = ""
name = ""
isID = False
isname = False
isnoname = False
finish = False

for line in open(fileInput, 'rU'):
    if line.startswith('>  <SALTDATA>'):
        isRecord = False
        continue
    if line.startswith('>  <IDNUMBER>'):
        isRecord = False
        isID = True
        continue
    if line.startswith('>  <IUPACNAME>'):
        isname = True
        continue
    if line.startswith('>  <Library>') and not finish:
        isnoname = True
        continue
    if isRecord:
        content = content + line
        continue
    elif isID:
        id_ = line.rstrip()
        isID = False
        continue
    elif isname or isnoname:
        content = content + "$$$$\n"
        name = line.rstrip().replace("'", "''")
        if isnoname:
            name = ""
        queryText = "INSERT INTO MYRIA (id, name, structure) VALUES ('" \
            + id_ + "' , '" + name + "' , '" + content + "');"
        query = query + queryText.replace("\n", "\\n") + "\n"
        content = ""
        id_ = ""
        name = ""
        isname = False
        isnoname = False
        finish = True
        i += 1
    if line.startswith('$$$$'):
        isRecord = True
        finish = False
    #if i == 10:
    #    break
f = open("MyriaScreen.txt", "w")
f.write(query)
f.close
