import re
import csv

def get_postcode():
    number = "No.33, Jalan USJ 10/1, UEP Subang Jaya, 47620 Selangor."
    addresses = []

    with open("sheets/FMStore.csv", "r") as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            addresses.append(row[2])

    address = []
    pattern_string = r'\b\d{5}\b'

    pattern = re.compile(pattern_string)

    for address in addresses:
        match2 = pattern.search(address)
        if not match2:
            continue

        print(match2.group())

# num = number.split(",")

# for index, n in enumerate(num):
#     if match2.group() in n:
#         address = num[index-1] + ", " + num[index]
#         break
def test():
    add = "aas,s,s,s,s,s,s"
    print(add.split(",")[2])


# print(match2.group())

if __name__ == "__main__":
    # get_postcode()
    test()