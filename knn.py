import csv

with open("iris.csv", newline='', encoding='utf-8') as f:
    leitor = csv.reader(f)
    for linha in leitor:
        print(linha[-1])
