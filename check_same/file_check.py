
line1 = []
line2 = []

with open("fam.txt", "r") as f:
    line1 = [line.rstrip() for line in f]

# print(line1)

with open("script_result.txt", "r") as f2:
    line2 = [line.rstrip() for line in f2]

# print(line1, line2)
for i in range(len(line1)):
    for j in range(len(line2)):
        if line1[i] in line2[j]:
            # print(f"{line1[i]} is exists in script")
            break
        if j == len(line2)-1:
            print(f"Line {i+2}, {line1[i]} in main is missing in script")
