import LeadRx
import logging
import json

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[
                        logging.StreamHandler()
                    ]
                    )

# read in leadsRX API secret key and leadsRX account_tag.
# Instructions to find these values can be found here https://developers.leadsrx.com/reference#authentication-1
json_file = open('auth.json')
auth_dict = json.load(json_file)

##create client -- must pass in secret key and account tag as strings
secret_key = auth_dict['secret_key']
account_tag = auth_dict['account_tag']
client = LeadRx.client(secret_key=secret_key, account_tag=account_tag)


# get contents of conversion ID endpoint for the account tag https://developers.leadsrx.com/reference#conversion-ids
conversion_ids = client.pull_conversion_ids()
# get result as json
conversion_id_json = conversion_ids.json
# get result as dataframe
conversion_id_dataframe = conversion_ids.dataframe

# get campaign IDs for the account tag https://developers.leadsrx.com/reference#campaign-ids
# campaignIDs are also called touchpoint ids
campaign_ids = client.pull_campaign_ids()
# get results as json
campaign_ids_json = campaign_ids.json
# get result as dataframe
campaign_ids_dataframe = campaign_ids.dataframe

# get domains for the account tag https://developers.leadsrx.com/reference#domains
domains = client.pull_domains()
# get result as json
domains_json = domains.json
# get result as dataframe
domains_dataframe = domains.dataframe

# get grouping ids for the account tag https://developers.leadsrx.com/reference#grouping-ids
groupings = client.pull_grouping_ids()
# get result as json
groupings = groupings.json

# get contents of touchpoint endpoint for the account tag with a given startDateTime and endDateTime https://developers.leadsrx.com/reference#touchpoints
# conversionID to use can be set by passing the conversionID for desired conversion as a str. Function pulls results for all conversions by default
# leadType can be set to "new","repeat" or "all". This filters touchpoint results based on first time,repeat or all conversions for a customer
touchpoints = client.pull_touchpoints(campaignID="554589", startDateTimeStr="2021-01 00:00:00",
                                      endDateTimeStr="2021-01-01 12:00:00", conversion_id='13697', lead_type="new")
# get result for entire time period as json
touchpoints_json = touchpoints.total_results_json
# get result for entire time period as dataframe
touchpoints_dataframe = touchpoints.total_results_dataframe
# get result for entire period split by day as json
touchpoints_json = touchpoints.by_day_results_json
# get result for entire period split by day as dataframe
touchpoints_dataframe = touchpoints.by_day_results_dataframe

# get contents of interactions endpoing for the account tag with a given startDateTime and endDateTime https://developers.leadsrx.com/reference#interactions
# campaignID should be supplied as a string. Campaign ID is the ID of the touchpoint you want to query
interactions = client.pull_interactions(campaignID="554589", startDateTimeStr="2021-01 00:00:00",
                                        endDateTimeStr="2021-01-01 11:00:00")
interactions_by_date_json = interactions.by_day_results_json
interactions_by_hour_of_day_json = interactions.hour_of_day_json
interactions_by_day_of_week_json = interactions.day_of_week_json

interactions_by_date_dataframe = interactions.by_day_results_dataframe
interactions_by_hour_of_day_dataframe = interactions.hour_of_day_dataframe
interactions_by_day_of_week_dataframe = interactions.day_of_week_json

# get contents of conversions endpoint for the account tag. https://developers.leadsrx.com/reference#conversions
# conversionID to use can be set by passing the conversionID for desired conversion as a str. Function pulls results for all conversions by default
# landingPage can be set to false to avoid pulling the landingPage field
# visitorId can be set to get conversions for a single visitor
conversions = client.pull_conversions(startDateTimeStr="2021-01-01 00:00:00", endDateTimeStr="2021-01-01 11:00:00",
                                      visitorID="1522653355")
# get result for the entire period split by day as json
conversions_json = conversions.json
# get result for the entire period split by day as dataframe
conversions_dataframe = conversions.dataframe

#get contents of non conversions endpoint for the account tag specified in client
non_conversions = client.pull_non_conversions(startDateTimeStr="2021-01-01 00:0:00",
                                              endDateTimeStr="2021-01-01 06:00:00")
#get results as json
results = non_conversions.json

#get results as dataframe
results=non_conversions.dataframe

#get contents of attribution endpoint for the account tag specific in client
attributions = client.pull_attribution(aModel="special", startDateTimeStr="2021-01-01 00:0:00",
                                       endDateTimeStr="2021-01-01 06:00:00")
#get results as json
results = attributions.json

#get results as dataframe
df_results = attributions.dataframe