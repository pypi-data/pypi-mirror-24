# coding: UTF-8

fileInput = '../OCDD_DB_ver6.00.sdf'
query = ""
queryText = ""
ids = []
i = 0
content = ""
IsRecord = True
IsID = False
for line in open(fileInput, 'rU'):
    if (i == 220000):
        break
    if line.startswith('> <UT_ID>'):
        IsID = True
        IsRecord = False
        continue
    if IsRecord:
        content = content + line
        continue
    if IsID:
        if i >= 200000:
            content = content + "$$$$\n"
            moleculeId = line.rstrip()
            queryText = "INSERT INTO OCDD (id, molecule) VALUES ('" \
            + moleculeId + "' , '" + content + "');"
            query = query + queryText.replace("\n", "\\n") + "\n"
        content = ""
        IsID = False
        i += 1
    if line.startswith('$$$$'):
        IsRecord = True
f = open("OCDD_Query.txt", "w")
f.write(query)
f.close