# LeadsRX Python Client

A python client for querying the LeadsRX API. Created in my spare time to help out our analytics team.

https://developers.leadsrx.com/reference#conversions


#### Written by Josh Hatfield @Semetrical


#### About Semetrical

Semetrical are a global top 40 digital agency offering a full suite of services. Bespoke technology forms a key part of what we do.

We won Best Small SEO Agency at the EU Search Awards in 2019 and Best Small Biddable Agency at the UK Search Awards 2020.

Our website can be found [here](http://bit.ly/3aMWIMd). If you want to chat, get in touch [here](http://bit.ly/3keCf5Y).

## Key Features


### Fetch Data From These Endpoints

* Conversions | https://developers.leadsrx.com/reference#conversions
* Touchpoints | https://developers.leadsrx.com/reference#touchpoints
* Interactions | https://developers.leadsrx.com/reference#interactions
* Conversion IDs | https://developers.leadsrx.com/reference#conversion-ids
* Campaign IDs | https://developers.leadsrx.com/reference#campaign-ids
* Grouping IDs | https://developers.leadsrx.com/reference#grouping-ids
* Domains | https://developers.leadsrx.com/reference#domains

### Access Results In These Formats

* Access Results As A Json Object ([{},{},{}])
* Access Results As A Pandas Dataframe


## Getting Started

### Installation
Download Files As Zip

Install These Libraries
* Requests
* Pandas

## Code Examples

Import Required Libraries
```python
import LeadsRx
import logging
import json

#Setup Log Handler
logging.basicConfig(level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
```
Authenticate And Create Client
```python
#read in client_scret and account tag from a json file 
json_file=open('auth.json')
auth_dict=json.load(json_file)

##create client -- must pass in secret key and account tag as strings
secret_key=auth_dict['secret_key']
account_tag=auth_dict['account_tag']

client = LeadRx.client(secret_key=secret_key, account_tag=account_tag)


#You could also just pass the key and tag in directly. Using a file is preferable as this way no sensitive information ends up in our gitrepo
client = LeadRx.client(secret_key="Your Client Secret", account_tag="Your Account Tag")

```

Accessing The Conversion ID Endpoint
```python
# get contents of conversion ID endpoint for the account tag given to client
conversion_ids = client.pull_conversion_ids()

# get result as json
conversion_id_json = conversion_ids.json

# get result as dataframe
conversion_id_dataframe = conversion_ids.dataframe
```
Accessing The Campaign ID Endpoint
```python
# get campaign IDs for the account tag given to client
# campaignIDs are also called touchpoint ids
campaign_ids = client.pull_campaign_ids()

# get results as json
campaign_ids_json = campaign_ids.json

# get result as dataframe
campaign_ids_dataframe = campaign_ids.dataframe
```
Accessing The Domains Endpoint
```python
# get domains for the account tag given to client
domains = client.pull_domains()

# get result as json
domains_json = domains.json

# get result as dataframe
domains_dataframe = domains.dataframe
```

Accessing The Groupings ID Endpoint
```python

# get grouping ids for the account tag given to client
groupings = client.pull_grouping_ids()

# get result as json
groupings = groupings.json
```
Accessing The Touchpoint Endpoint
```python
# get contents of touchpoint endpoint for the account tag given to client
    #Expects a startDateTime and endDateTime in "YYYY-MM-DD HH-MM-SS" format
    #leadType can be set to "new","repeat" or "all".This filters touchpoint results based on first time,repeat or all conversions for a customer
    #Function pulls all conversion_ids by default. If you want to fetch conversions for a single conversion then pass it's conversion_id as a string

touchpoints = client.pull_touchpoints(campaignID="554588", startDateTimeStr="2021-01 00:00:00",
                                      endDateTimeStr="2021-01-01 11:00:00", conversion_id='13697', lead_type="new")
# get result for entire time period as json
touchpoints_json = touchpoints.total_results_json

# get result for entire time period as dataframe
touchpoints_dataframe = touchpoints.total_results_dataframe

# get result for entire period split by day as json
touchpoints_json = touchpoints.by_day_results_json

# get result for entire period split by day as dataframe
touchpoints_dataframe = touchpoints.by_day_results_dataframe
```
Accessing The Interactions Endpoint
```python

# get contents of interactions endpoing for the account tag given to client
   #Expects a startDateTime and endDateTime in "YYYY-MM-DD HH-MM-SS" format
   #LeadRX campaignID should be supplied as a string.Campaign ID is the ID of the touchpoint you want to query
   #Campaign IDS can be found by calling the campaigns ID Endpoint

interactions = client.pull_interactions(campaignID="554588", startDateTimeStr="2021-01 00:00:00",
                                        endDateTimeStr="2021-01-01 11:00:00")
                                        
#get result for the entire time period split by date as JSON
interactions_by_date_json = interactions.by_day_results_json

#get results by hour_of_day for the entire time period as JSON
interactions_by_hour_of_day_json = interactions.hour_of_day_json

#get results by day_of_week for the entire time period as JSON
interactions_by_day_of_week_json = interactions.day_of_week_json

#get result for the entire time period split by date as a Dataframe
interactions_by_date_dataframe = interactions.by_day_results_dataframe

#get results by hour_of_day for the entire time period as Dataframe
interactions_by_hour_of_day_dataframe = interactions.hour_of_day_dataframe

#get results by day_of_week for the entire time period as JSON
interactions_by_day_of_week_dataframe = interactions.day_of_week_json
```
Accessing The Conversions Endpoint
```python

# get contents of conversions endpoint for the account tag given to client
    #Expects a startDateTime and endDateTime in "YYYY-MM-DD HH-MM-SS" format
    #landingPage can be set to False to avoid pulling the landingPage field
    #Function pulls all conversion_ids by default. If you want to fetch conversions for a single conversion then pass it's conversion_id as a string
    #visitorId can be set to get conversions for a single visitor.To pull data for all visitors do not pass the visitorID parameter to the function
   
conversions = client.pull_conversions(startDateTimeStr="2021-01-01 00:00:00", endDateTimeStr="2021-01-01 11:00:00",
                                      visitorID="1522653355",landingPage=True,conversion_id='13697')
                                      
# get result for the entire period split by day as json
conversions_json = conversions.json

# get result for the entire period split by day as dataframe
conversions_dataframe = conversions.dataframe
```
