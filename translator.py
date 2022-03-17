import translators as ts

files_path = ["./logic.py", "./draw.py", "./main.py"]

for file in files_path:
    file1 = open(file, 'r+')
    Lines = file1.read().split("\n")

    Lineslist = []

    for index, line in enumerate(Lines):
        result = line
        if "#" in line:
            templine = line.split("#")
            print(type(templine[-1]))
            try:
                result = templine[0] + "# " + \
                    ts.google(templine[-1], to_language='de')
            except Exception as e:
                print(f"In Line{index} in File {file}")
                raise e

        Lineslist.append(result+"\n")

    file1 = open(file, 'w')
    file1.writelines(Lineslist)
    file1.close()
