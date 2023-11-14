
line1 = []
line2 = []

with open("fam.txt", "r") as f:
    line1 = [line.rstrip() for line in f]

with open("script_result.txt", "r") as f2:
    line2 = [line.rstrip() for line in f2]


for i in range(len(line1)):
    if line1[i] == line2[i]:
        continue
    else:
        print(f"Line {i+2} in main is not tally with Line {i+3} in script")