#!/usr/bin/env python3 
'''
A Python based wrapper over Indeed Job Search API
By: Kashif Aziz (http://www.kashifaziz.me)
'''

from bs4 import BeautifulSoup
import requests
import os 
import os.path
import csv 
import time
import json
from random import uniform, choice
from datetime import datetime


def writerows(rows, filename, heading=None):
    with open(filename, 'a', encoding='utf-8', newline='\n') as toWrite:
        writer = csv.writer(toWrite)
        if heading:
            writer.writerow(heading)
        else:    
            writer.writerows(rows)


def get_indeed_jobs(**params):
    '''
    get jobs from indeed using the API
    pass number of days and location
    '''

    # Set CSV and log file names and server path
    base_path = ""

    jobs_csv = base_path+"indeedjobs.csv"

    # remove csv files, if exist
    if os.path.exists(jobs_csv):
        os.remove(jobs_csv)

    indeed_url = prepare_params(**params)

    flag = ""

    # get total jobs found for number of days and location
    total_jobs = get_total_jobs(indeed_url)
    if total_jobs:
        print("total jobs {}".format(total_jobs))

        # build api links with start and end range
        api_links = build_api_links(indeed_url, total_jobs)

        if api_links:
            heading = ["Employer", "City", "State", "Zipcode", "Jobtitle", "Joblink", "Jobdate", "Description"]            
            writerows("", "indeedjobs.csv", heading=heading)
            
            for link in api_links:
                get_indeed_job_listings(link)
            
            flag = "Jobs fetched successfully."

    else:
        flag = "Jobs not found. Please use a valid Publisher Id along with query keyword or location."

    return flag


def prepare_params(**params):
    # prepare parameters for Indeed API, returned prepared url

    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)"

    # number of job days should not be more than 7
    if not params["days"] or int(params["days"]) > 7:
        params["days"] = "1"

    # if value for query is not available, location and country must be present, else set default values
    if not params["q"]:
        if not (params["l"] and params["co"]):
            params["l"] = "Karachi"
            params["co"] = "pk"

    indeed_api_params = {
     'publisher': params["publisher"],
     'q': params["q"],
     'l': params["l"],
     'co': params["co"],
     'sort': params["sort"],
     'format': "json",
     'fromage': params["days"],
     'v': "2",
     'useragent': user_agent
    }

    api_arguments = "&".join([key+"="+value for key, value in indeed_api_params.items()])
        
    return "http://api.indeed.com/ads/apisearch?"+api_arguments


def get_total_jobs(indeed_url):
    total_jobs = 0
    try:
        response = requests.get(indeed_url)
        if response.status_code == 200:
            json_data = response.json()
            total_jobs = json_data["totalResults"]
    except Exception as e:
        print("Error getting total jobs! {}".format(e)) 

    return total_jobs


def build_api_links(indeed_url, total_jobs):
    api_links = []
    start = 0
    limit = 25

    while start < total_jobs:
        api_links.append([indeed_url+"&start="+str(start)+"&limit="+str(limit)])
        start = start + limit

    return api_links


def get_indeed_job_listings(indeed_url):
    '''
    get jobs from indeed api link and save to csv
    '''
    indeed_url = indeed_url[0]
    # print(indeed_url)

    jobs = []   
    try:
        response = requests.get(indeed_url)
        if response.status_code == 200:
            json_data = response.json()
            for x in json_data["results"]:
                jobtitle = x["jobtitle"]
                employer = x["company"]
                job_snippet = x["snippet"]

                location = x["formattedLocationFull"]
                city = state = zipcode = joblink = jobdate = ""

                try:
                    city = location.split(",")[0].strip()
                    state_and_zip = location.split(",")[1].strip()
                    state = state_and_zip[:2]
                    zipcode = state_and_zip[2:].strip()
                except Exception as e:
                    pass
                                                            
                try:
                    joblink = x["url"].split("&")[0]
                except Exception as e:
                    pass

                try:
                    jobdate = x["date"].split(",")[1][:12].strip() 
                except Exception as e:
                    pass

                print(jobtitle)
                jobs.append([employer, city, state, zipcode, jobtitle, joblink, jobdate, job_snippet])
                        
            writerows(jobs, "indeedjobs.csv")

    except Exception as e:
        print("Error! {}".format(e))

    # take a break .. make this random
    time.sleep(uniform(0.5, 2.0))  # sleep randomly

    return


if __name__ == "__main__":
    # Parameters to fetch job listings through Indeed API
    # Publisher Id is required
    # To search jobs, either provide query string or combination of location and country code.

    params = {
        'publisher': "",    # publisher ID (Required)
        'q': "",            # Job search query
        'l': "",            # location (city / state)
        'co': "",           # Country Code
        'sort': "",         # Sort order, date or relevance
        'days': ""          # number of days to fetch jobs, maximum is 7 days
        }   
    
    get_jobs = get_indeed_jobs(**params)
    print(get_jobs)
