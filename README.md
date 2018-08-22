# indeed-python-wrapper
A Python wrapper for Indeed Job Search API. 

### Prerequisites

- Indeed Publisher API ID, available for free from [here](https://ads.indeed.com/jobroll/xmlfeed?target=_blank)
- Python 3.x
- BeautifulSoup and Requests library. Use the enclosed requirements.txt to install them.


### Usage

Open indeedapiwrapper.py, add following parameters to fetch job listings through Indeed Job Search API:
- Publisher Id is required
- To search jobs, either provide query string or combination of location and country code.

```python
    params = {
        'publisher': "",    # publisher ID (Required)
        'q': "",            # Job search query
        'l': "",            # location (city / state)
        'co': "",           # Country Code
        'sort': "",         # Sort order, date or relevance
        'days': ""          # number of days to fetch jobs, maximum is 7 days
        }   
```

### Output

The list of jobs will be saved in a CSV file "indeedjobs.csv" in the same directory where the script resides.

### More Information
More details in the [blog post here](http://www.kashifaziz.me/indeed-api-python-wrapper.html/).
