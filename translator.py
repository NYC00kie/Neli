import translators as ts

files_path = ["./logic.py", "./draw.py"]

for file in files_path:
    file1 = open(file, 'r+')
    Lines = file1.read().split("\n")

    Lineslist = []

    for line in Lines:
        result = line
        if "#" in line:
            templine = line.split("#")
            print("# in line")
            result = templine[0] + "# " + \
                ts.google(templine[-1], to_language='de')
        print(result)
        Lineslist.append(result+"\n")

    file1 = open(file, 'w')
    file1.writelines(Lineslist)
    file1.close()
