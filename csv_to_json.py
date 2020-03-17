# !/usr/bin/env/python3
import csv
import json

print ("Converting John Hopkin's latest data from csv to json")
x = []
csvFilePath = "./COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
jsonFilePath = "./data/covid.json"
with open (csvFilePath) as csvFile:
    csvReader = csv.DictReader(csvFile)
    for csvRow in csvReader:
        x.append(csvRow)


# write the data to a json file
with open(jsonFilePath, "w") as jsonFile:
    jsonFile.write(json.dumps(x, indent = 4))





