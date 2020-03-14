# !/usr/bin/env/python3
import json
import sys
from decimal import Decimal
from numpy import mean

with open('./data/'+ sys.argv[1] +'.json') as f:
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

#store the value of last recorded cases:
cases_today = a
#pick the last 15 days exponential increase as usable data and remove all others
exp_list = exp_list[-10:]

#calculate the average exponentail from the last 15 days
avg = mean(exp_list)

#predict the expected increase in cases for the following day:
predicted_increase = avg * cases_today

#calculate total number of cases for the next day
total_cases = cases_today + predicted_increase

#convert average exponential increase into readable percentable
avg_exp_percentage = avg * 100

#remove decimal values
avg_exp_percentage = (Decimal(avg_exp_percentage)).quantize(TWOPLACES)
avg_exp_percentage = avg_exp_percentage // 1

predicted_increase = (Decimal(predicted_increase)).quantize(TWOPLACES)
predicted_increase = predicted_increase // 1

total_cases = (Decimal(total_cases)).quantize(TWOPLACES)
total_cases = total_cases // 1

print ("Country: {0}".format(sys.argv[1]))
print ("Total cases today: {0}".format(cases_today))
print ("Predicted increase tomorrow: {0}".format(predicted_increase))
print ("Total predicted confirmed cases for tomorrow: {0}".format(total_cases))
print ("Exponential increase: {0} percent".format(avg_exp_percentage))

