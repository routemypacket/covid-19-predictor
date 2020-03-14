# !/usr/bin/env/python3
import json
from decimal import Decimal
from numpy import mean

with open('./data/covid.json') as f:
  data = json.load(f)

# define a value of a to multiply with the first value of cases in for loop
a = 1
# define a calue to reduce decimals to two places
TWOPLACES = Decimal(10) ** -2
# define list to be used to stope all exp values (exponential values)
exp_list = []

#x = thisdict["model"]

#x = thisdict.get("model")

for x,y in data.items():
    curcases = y.get("cases")
    #calculate exponential value
    exp = curcases / a
    exp = (Decimal(exp)).quantize(TWOPLACES)
    exp = exp - 1
    exp = str(exp)
    exp = float(exp)
    exp_list.append(exp)
    a = curcases

#Store the value of last recorded cases:
cases_today = a
#pick the last 15 days exponential increase as usable data and remove all others
exp_list = exp_list[-15:]

#calculate the average exponentail from the last 15 days
avg = mean(exp_list)

# limit the output to two decimal places
avg = (Decimal(exp)).quantize(TWOPLACES)

#predict the expected increase in cases for the following day:
predicted_increase = avg * cases_today

#Calculate total number of cases for the next day
total_cases = cases_today + predicted_increase

print ("Total cases today : {0} :: Predicted increase tomorrow: {1} :: Total cases for tomorrow: {2}".format(cases_today,predicted_increase,total_cases))


