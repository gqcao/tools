from translate import Translator

FILE_PATH = "sub_en.txt"
idx = 0
translator= Translator(to_lang="zh", provider="mymemory", email="ytsyify@yts.mx")
new_doc = []
with open(FILE_PATH, 'r') as file:
    for line in file:
        if line == "\n":
            new_doc.append(line)
            idx = 0
            continue
        idx = idx + 1
        if idx > 2:
            translated_line = translator.translate(line)
            new_doc.append(translated_line + "\n")
        else:
            new_doc.append(line)

with open(FILE_PATH.split(".")[0] + "_cn" + ".txt", 'w') as file:
    for item in new_doc:
        file.write(item)
