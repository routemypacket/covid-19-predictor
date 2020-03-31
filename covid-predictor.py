# !/usr/bin/env/python3
import json
import sys
import re
from decimal import *
from numpy import mean
from datetime import datetime
import clone_jh_repo
import csv_to_json

print ("Calculating expected cases rises in" + sys.argv[1] + "tomorrow, in two weeks and in one month")

# define a value of a to multiply with the first value of cases in for loop
a = 1
# define a value to reduce decimals to two places
TWOPLACES = Decimal(10) ** -2
# define list to be used to stope all exp values (exponential values)
exp_list = []
# define dictionary for incorporating all output in one place
countries_affected = {}
# define list for incorporating all output in one place that is huam readable
countries_data_list = []
#Save the value of user input for country in a variable
requested_country = sys.argv[1]
# Increase the precision of decimal value to avoid errors for computations with large 10^E50 type results
getcontext().prec = 1000


def main(a,TWOPLACES,exp_list,requested_country):
    with open('./data/covid.json') as f:
        val = json.load(f)

    if requested_country == 'all_countries':
        for x in val:
            calculate_exp(a,TWOPLACES,exp_list,x)
    else:
        for x in val:
            if x['Country/Region'] == requested_country:
                calculate_exp(a,TWOPLACES,exp_list,x)

    countries_affected_json = [{"Country": v} for v in countries_affected.items()]
    json.dumps(countries_affected_json, indent=4)
    
    # save json and readable list in a file
    with open('./prediction/prediction_human_readable/' + str(datetime.now()), 'w') as filehandle:
        for line in countries_data_list:
            filehandle.write('%s\n' % line)

    with open('./prediction/prediction_json/' + str(datetime.now()), 'w') as filehandle:
        for line in countries_affected_json:
            filehandle.write('%s' % line)
    
    print ("Output saves in ./prediction/prediction_huamn_readable/<date_time_stamp> & ./prediction/prediction_json/<date_time_stamp> for output in json")

def calculate_exp(a,TWOPLACES,exp_list,x):
    # Store current country's name
    country = x['Country/Region']
    province = x['Province/State']
    for dates, curcases in x.items():
        # pick fields with dates only
        q = re.findall(r'\d+\/\d+\/\d+', dates)
        if q:
           curcases = int(curcases)
           #calculate exponential value
           exp = curcases / a
           exp = (Decimal(exp)).quantize(TWOPLACES)
           # store the 1.x value seperately
           exp = exp - 1
           exp = str(exp)
           exp = float(exp)
           exp_list.append(exp)
           if curcases != 0:
               a = curcases
    # Run Prediction Algorithm
    predict(exp_list,a,country,province)


def predict (exp_list,a,country,province):
    TWOPLACES = Decimal(10) ** -2
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

    #convert avg to 1.xx value
    avg_a = avg + 1

    #calculate one week prediction
    avg_power_seven = avg_a ** 7
    avg_one_week = cases_today * avg_power_seven
    avg_one_week = int(avg_one_week)

    #calculate two weeks prediction
    avg_power_fourteen = avg_a ** 14
    avg_two_weeks = cases_today * avg_power_fourteen
    avg_two_weeks = int(avg_two_weeks)

    #calculate one month prediction
    avg_power_thirty = avg_a ** 30
    avg_power_thirty = (Decimal(avg_power_thirty)).quantize(TWOPLACES)
    avg_one_month = cases_today * avg_power_thirty
    avg_one_month = int(avg_one_month)

    #remove decimal values
    avg_exp_percentage = (Decimal(avg_exp_percentage)).quantize(TWOPLACES)
    avg_exp_percentage = avg_exp_percentage // 1
    avg_exp_percentage = int(avg_exp_percentage)

    predicted_increase = (Decimal(predicted_increase)).quantize(TWOPLACES)
    predicted_increase = predicted_increase // 1
    predicted_increase = int(predicted_increase)

    total_cases = (Decimal(total_cases)).quantize(TWOPLACES)
    total_cases = total_cases // 1
    total_cases = int(total_cases)

    avg_one_week = (Decimal(avg_one_week)).quantize(TWOPLACES)
    avg_one_week = avg_one_week // 1
    avg_one_week = int(avg_one_week)

    avg_two_weeks = (Decimal(avg_two_weeks)).quantize(TWOPLACES)
    avg_two_weeks = avg_two_weeks // 1
    avg_two_weeks = int(avg_two_weeks)

    avg_one_month = (Decimal(avg_one_month)).quantize(TWOPLACES)
    avg_one_month = avg_one_month // 1
    avg_one_month = int(avg_one_month)
    
    country_data = {}
    country_data["cases_today"] = cases_today
    country_data["predicted_increase_tomorrow"] = predicted_increase 
    country_data["predicted_confirmed_cases_tomorrow"] = total_cases
    country_data["avg_exponential_increase"] = avg_exp_percentage
    country_data["predited_cases_one_week"] = avg_one_week
    country_data["predited_cases_two_weeks"] = avg_two_weeks
    country_data["predited_cases_one_month"] = avg_one_month
#   country_affected["country"] = country
    countries_affected[country] = country_data

    # Append to list for human readable data
    if province:
        countries_data_list.append("*****Country: " + province + ", " + country + "*****")
    else:
        countries_data_list.append("*****Country: " + country + "*****")
    countries_data_list.append("Total cases today: " + str(cases_today))
    countries_data_list.append("Predicted increase tomorrow: " + str(predicted_increase))
    countries_data_list.append("Total predicted confirmed cases for tomorrow: " + str(total_cases))
    countries_data_list.append("Average exponential increase: " + str(avg_exp_percentage))
    countries_data_list.append("Predicted cases in one week: " + str(avg_one_week))
    countries_data_list.append("Predicted cases in two weeks: " + str(avg_two_weeks))
    countries_data_list.append("Predicted cases in one month: " + str(avg_one_month))

#    print ("\n***************{0}***************".format(country))
#    print ("Total cases today: {0}".format(cases_today))
#    print ("Predicted increase tomorrow: {0}".format(predicted_increase))
#    print ("Total predicted confirmed cases for tomorrow: {0}".format(total_cases))
#    print ("Avergae exponential increase: {0} percent".format(avg_exp_percentage))
#    print ("Predicted cases in a week: {0}".format(avg_one_week))
#    print ("Predicted cases in two weeks: {0}".format(avg_two_weeks))
#    print ("Predicted cases in one month: {0}".format(avg_one_month))


main(a,TWOPLACES,exp_list,requested_country)
