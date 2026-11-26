import csv

with open("data/registrations.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        print(row["id"])
        print(row["entry"])