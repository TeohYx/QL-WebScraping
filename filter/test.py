# with open("filter/filter.txt", "r") as f:
#     i=0
#     for line in f:
#         print(i)
#         print(line.strip())
#         i+=1
#     # print(content)

location_temp = []
commercial_type = []
listing_type = []


with open("filter/filter_propertyguru.txt", "r") as file:
    line = file.readline()

    while line:
        if line.strip() == "LOCATION":
            while line.strip() !='':
                line = file.readline()

                location_temp.append(line.strip())
        elif line.strip() == "LISTING":
            while line.strip() !='':
                line = file.readline()

                commercial_type.append(line.strip())
        elif line.strip() == "PROPERTY":
            while line.strip() !='':
                line = file.readline()

                listing_type.append(line.strip())
        line = file.readline()
print(f"{location_temp[:-1]}\n{commercial_type[:-1]}\n{listing_type[:-1]}\n")