from LeadsRx import web_request_interfaces as web_request
import copy
from pandas import DataFrame


class AttributionResult:

    def __init__(self,non_conversion_json):
        __non_conversion_json=copy.deepcopy(non_conversion_json)
        self.__flattened_json = self.__gen_flattened_json(__non_conversion_json)

    def __gen_flattened_json(self,json_input):
        output_list=[]
        for item in json_input['results']:

            item['Campaign_ID']=item.pop('id')
            item['Conversion_Total']=item.pop('count')
            item['Conversion_Value']=item.pop('value')
            item['Conversion_Cost']=item.pop('cost')
            output_list.append(item)

        return output_list

    @property
    def dataframe(self):
        return DataFrame(self.__flattened_json)

    @property
    def json(self):
        return self.__flattened_json



class NonConversionResult:

    def __init__(self,non_conversion_json):
        __non_conversion_json=copy.deepcopy(non_conversion_json)
        self.__flattened_json = self.__gen_flattened_json(__non_conversion_json)

    def __gen_flattened_json(self,json_input):

        return json_input

    @property
    def dataframe(self):
        return DataFrame(self.__flattened_json)

    @property
    def json(self):
        return self.__flattened_json


class ConversionResult:

    def __init__(self, conversion_json):
        __conversion_json = copy.deepcopy(conversion_json)
        self.__flattened_json = self.__gen_flattened_json(__conversion_json)

    def __gen_flattened_json(self, raw_json):
        # geodata fields change depending on the country
        # they have not documented geodata schema per country FFS
        # It's late and I'm tired. I have just removed geodata_dict for now
        results_list = raw_json['results']
        result_output = []
        for result in results_list:

            conversion_data = {'ID': result['ID'], 'conversionID': result['conversionID'],
                               'conversionTSUnix': result['conversionTS'],
                               'conversionLocalTSUnix': result['conversionLocalTS'],
                               'conversionDateTime': result['conversionDateTime'],
                               'conversionLocalDateTime': result['conversionLocalDateTime']}

            profile_data = {'profile.firstName': result['profile']["0"]["firstName"],
                            'profile.lastName': result['profile']["0"]["lastName"], 'lrxID': result['profile']['lrxID']}

            if 'landingPage' in result.keys():
                conversion_data['landingPage'] = result['landingPage']
            touchpoint_data = []

            for count, item in enumerate(result['attributionPath']):
                touch_point_dict = {'attribution_path_id': result['attributionPath'][count],
                                    'touchpointDateTime': result['touchpointDateTimes'][count]}

                extracted_results = {**conversion_data, **profile_data, **touch_point_dict}
                touchpoint_data.append(extracted_results)

            result_output.extend(touchpoint_data)

        return result_output

    @property
    def dataframe(self):
        return DataFrame(self.__flattened_json)

    @property
    def json(self):
        return self.__flattened_json


class ConversionIDResult:

    def __init__(self, conversion_id_json):
        __conversion_json = copy.deepcopy(conversion_id_json)
        self.__flattened_json = self.__gen_flattened_json(__conversion_json)

    def __gen_flattened_json(self, raw_json):
        results_list = raw_json['results']
        extracted_results = []
        for result in results_list:
            extracted_results.append(
                {'conversionID': result['conversionID'], 'conversionName': result['conversionName']})

        return extracted_results

    @property
    def dataframe(self):
        return DataFrame(self.__flattened_json)

    @property
    def json(self):
        return self.__flattened_json


class GroupingsResult:

    def __init__(self, conversion_id_json):
        __conversion_json = copy.deepcopy(conversion_id_json)
        self.__flattened_json = self.__gen_flattened_json(__conversion_json)

    def __gen_flattened_json(self, raw_json):
        results_list = raw_json['results']
        extracted_results = []
        for result in results_list:
            row_dict = {'groupingID': result['groupingID'], 'groupingName': result['groupingName']}
            if "touchpoints" not in result.keys():
                row_dict['touchpoints'] = None
            else:
                row_dict['touchpoints'] = result['touchpoints']

            extracted_results.append(row_dict)

        return extracted_results

    @property
    def dataframe(self):
        return DataFrame(self.__flattened_json)

    @property
    def json(self):
        return self.__flattened_json


class DomainResults:

    def __init__(self, conversion_id_json):
        __conversion_json = copy.deepcopy(conversion_id_json)
        self.__flattened_json = self.__gen_flattened_json(__conversion_json)

    def __gen_flattened_json(self, raw_json):
        results_list = raw_json['results']
        extracted_results = []
        for result in results_list:
            extracted_results.append(
                {'domain': result['domain']})

        return extracted_results

    @property
    def dataframe(self):
        return DataFrame(self.__flattened_json)

    @property
    def json(self):
        return self.__flattened_json


class CampaignIDResult:

    def __init__(self, conversion_id_json):
        __conversion_json = copy.deepcopy(conversion_id_json)
        self.__flattened_json = self.__gen_flattened_json(__conversion_json)

    def __gen_flattened_json(self, raw_json):
        results_list = raw_json['results']
        extracted_results = []
        for result in results_list:
            extracted_results.append(
                {'campaignID': result['campaignID'], 'campaignName': result['campaignName']})

        return extracted_results

    @property
    def dataframe(self):
        return DataFrame(self.__flattened_json)

    @property
    def json(self):
        return self.__flattened_json


class TouchPointResult:

    def __init__(self, touchpoint_json, campaign_id: str):
        __conversion_json = copy.deepcopy(touchpoint_json)
        self.__total_results_flattened_json = None
        self.__by_day_results_flattend_json = None
        self.__gen_flattened_json(__conversion_json, campaign_id)

    def __gen_flattened_json(self, raw_json, campaign_id):
        results = raw_json['results']
        results_total_conversions = results['total']['conversions']
        results_total_revenue = results['total']['revenue']

        self.__total_results_flattened_json = [{'results.total.conversions': results_total_conversions,
                                                'results.total.revenue': results_total_revenue,
                                                'campaignID': campaign_id}]

        by_day_results = []
        for count, day in enumerate(results["byDay"]["conversions"]):
            date = day
            conversion_count = results["byDay"]["conversions"][date]
            revenue_value = results['byDay']['revenue'][date]

            by_day_results.append(
                {'Date': date, 'results.byDay.conversions': conversion_count, 'results.byDay.revenue': revenue_value,
                 'campaignID': campaign_id})

        self.__by_day_results_flattend_json = by_day_results

    @property
    def total_results_dataframe(self):
        return DataFrame(self.__total_results_flattened_json)

    @property
    def total_results_json(self):
        return self.__total_results_flattened_json

    @property
    def by_day_results_dataframe(self):
        return DataFrame(self.__by_day_results_flattend_json)

    @property
    def by_day_results_json(self):
        return self.__by_day_results_flattend_json


class InteractionResult:

    def __init__(self, interaction_json, campaign_id: str):
        __interaction_json = copy.deepcopy(interaction_json)
        self.__by_day_of_week_results_flattened_json = []
        self.__by_day_results_flattend_json = []
        self.__by_hour_results_flattened_json = []
        self.__gen_flattened_json(interaction_json, campaign_id)

    def __gen_flattened_json(self, raw_json, campaign_id):
        results = raw_json['results']

        if type(results['byDay']) == dict:
            for key, value in results['byDay'].items():
                self.__by_day_results_flattend_json.append({'Date': key, 'Interactions': value, 'CampaignID': campaign_id})

        else:
            self.__by_day_results_flattend_json.append([{'Date':'','Interactions':'','CampaignID':''}])

        if type(results['byDOW']) == dict:
            for key, value in results['byDOW'].items():
                self.__by_day_of_week_results_flattened_json.append(
                    {'Day_Of_Week': key, 'Interactions': value, 'CampaignID': campaign_id})
        else:
            self.__by_day_of_week_results_flattened_json.append([])

        for count,value in enumerate(results['byHour']):
            self.__by_hour_results_flattened_json.append(
                {'Hour_Of_Day': count, 'Interactions': value, 'CampaignID': campaign_id})

    @property
    def by_day_results_json(self):
        return self.__by_day_results_flattend_json

    @property
    def day_of_week_json(self):
        return self.__by_day_of_week_results_flattened_json

    @property
    def hour_of_day_json(self):
        return self.__by_hour_results_flattened_json

    @property
    def by_day_results_dataframe(self):
        return DataFrame(self.__by_day_results_flattend_json)

    @property
    def day_of_week_dataframe(self):
        return DataFrame(self.__by_day_of_week_results_flattened_json)

    @property
    def hour_of_day_dataframe(self):
        return DataFrame(self.__by_hour_results_flattened_json)


class LeadRXRequestError(Exception):

    def __init__(self, status_code, message):
        error_message = f'LeadRX Error Message Found In Response. Status value was {status_code}. Error message was {message}'
        super().__init__(error_message)


def handle_response_status(result_json):
    # LeadRX have not bothered to detail error codes in their documentation!
    # These are the error codes we have seen so far
    # {status:3,message:'Missing required data fields'}
    # {status:10,message:'Account credentials did not validate}

    valid_success_messages=['ok','success']
    status = result_json['status']
    message = result_json['message'].lower()

    if int(status) == 0 and message in valid_success_messages:
        return True

    else:
        raise LeadRXRequestError(status, message)


class client:

    def __init__(self, secret_key: str, account_tag: str):
        self.__secret_key = secret_key
        self.__account_tag = account_tag
        self.__get_request = web_request.requestMachine(web_request.getRequest)

    def pull_attribution(self,aModel:str,startDateTimeStr:str,endDateTimeStr:str,conversion_id="*",lead_type="all",usePacific=1):

        # setting usePacfic to 1 will force the api to return results in the pacific timeZone for startDateTime and endDatetime
        # otherwise these values will reflect the local timezones of visitors (who wants that..?)
        querystring = {"aModel": aModel, "startDateTime": startDateTimeStr, "endDateTime": endDateTimeStr,
                       "conversionID": conversion_id, "acctTag": self.__account_tag,
                       "apiSecret": self.__secret_key,'leadType':lead_type,"usePacific":usePacific}

        result_json = self.__get_request.send_request(base_url='https://api.leadsrx.com/v1/',
                                                      resource_uri='attribution.php',
                                                      url_params=querystring)

        handle_response_status(result_json)

        results_object = AttributionResult(result_json)
        return results_object


    def pull_interactions(self, campaignID: str, startDateTimeStr: str, endDateTimeStr: str, conversion_id="*",usePacific=1):

        # setting usePacfic to 1 will force the api to return results in the pacific timeZone for startDateTime and endDatetime
        # otherwise these values will reflect the local timezones of visitors (who wants that..?)
        querystring = {"campaignID": campaignID, "startDateTime": startDateTimeStr, "endDateTime": endDateTimeStr,
                       "conversionID": conversion_id, "acctTag": self.__account_tag,
                       "apiSecret": self.__secret_key,"usePacific":usePacific}


        result_json = self.__get_request.send_request(base_url='https://api.leadsrx.com/v1/',
                                                      resource_uri='interactions.php',
                                                      url_params=querystring)

        handle_response_status(result_json)
        results_object = InteractionResult(interaction_json=result_json, campaign_id=campaignID)

        return results_object

    def pull_campaign_ids(self):
        querystring = {"acctTag": self.__account_tag, "apiSecret": self.__secret_key}
        result_json = self.__get_request.send_request(base_url='https://api.leadsrx.com/v1/',
                                                      resource_uri='campaignIDs.php',
                                                      url_params=querystring)

        handle_response_status(result_json)
        results_object = CampaignIDResult(conversion_id_json=result_json)
        return results_object

    def pull_grouping_ids(self, with_touchpoints=True):
        querystring = {"acctTag": self.__account_tag, "apiSecret": self.__secret_key,
                       "withTouchpoints": with_touchpoints}
        result_json = self.__get_request.send_request(base_url='https://api.leadsrx.com/v1/',
                                                      resource_uri='groupIDs.php',
                                                      url_params=querystring)

        handle_response_status(result_json)
        results_object = GroupingsResult(conversion_id_json=result_json)
        return results_object

    def pull_domains(self):
        querystring = {"acctTag": self.__account_tag, "apiSecret": self.__secret_key}
        result_json = self.__get_request.send_request(base_url='https://api.leadsrx.com/v1/',
                                                      resource_uri='getDomains.php',
                                                      url_params=querystring)

        handle_response_status(result_json)
        results_object = DomainResults(conversion_id_json=result_json)
        return results_object

    def pull_non_conversions(self,startDateTimeStr: str, endDateTimeStr: str,usePacific=1):

        # setting usePacfic to 1 will force the api to return results in the pacific timeZone for startDateTime and endDatetime
        # otherwise these values will reflect the local timezones of visitors (who wants that..?)
        querystring = {"startDateTime": startDateTimeStr, "endDateTime": endDateTimeStr,
                       "acctTag": self.__account_tag, "apiSecret": self.__secret_key,
                        "includePages":"yes","usePacific":usePacific}

        result_json = self.__get_request.send_request(base_url='https://api.leadsrx.com/v1/',
                                                      resource_uri='non-conversions.php',
                                                      url_params=querystring)

        handle_response_status(result_json)
        results_object= NonConversionResult(non_conversion_json=result_json)
        return results_object


    def pull_conversions(self, startDateTimeStr: str, endDateTimeStr: str, conversion_id="*", landingPage="yes",
                         visitorID=None,usePacific=1):

        #setting usePacfic to 1 will force the api to return results in the pacific timeZone for startDateTime and endDatetime
        #otherwise these values will reflect the local timezones of visitors (who wants that..?)
        querystring = {"startDateTime": startDateTimeStr, "endDateTime": endDateTimeStr,
                       "conversionID": conversion_id, "acctTag": self.__account_tag, "apiSecret": self.__secret_key,
                       "landingPage": landingPage,'usePacific':usePacific}

        if visitorID is not None:
            querystring['visitorID'] = visitorID

        result_json = self.__get_request.send_request(base_url='https://api.leadsrx.com/v1/',
                                                      resource_uri='conversions.php',
                                                      url_params=querystring)

        handle_response_status(result_json)
        results_object = ConversionResult(conversion_json=result_json)

        return results_object

    def pull_touchpoints(self, campaignID, startDateTimeStr: str, endDateTimeStr: str, conversion_id="*",
                         lead_type="all",usePacific=1):
        valid_lead_types = ["new", "repeat", "all"]

        if lead_type.lower() not in valid_lead_types:
            raise TypeError(
                f'lead_type value "{lead_type}" is not a valid lead_type. Valid lead types are {valid_lead_types}')

        # setting usePacfic to 1 will force the api to return results in the pacific timeZone for startDateTime and endDatetime
        # otherwise these values will reflect the local timezones of visitors (who wants that..?)
        querystring = {"campaignID": campaignID, "startDateTime": startDateTimeStr, "endDateTime": endDateTimeStr,
                       "conversionID": conversion_id, "leadType": lead_type, "acctTag": self.__account_tag,
                       "apiSecret": self.__secret_key,"usePacific":usePacific}

        result_json = self.__get_request.send_request(base_url='https://api.leadsrx.com/v1/',
                                                      resource_uri='touchpoints.php',
                                                      url_params=querystring)

        handle_response_status(result_json)
        results_object = TouchPointResult(touchpoint_json=result_json, campaign_id=campaignID)

        return results_object

    def pull_conversion_ids(self):
        querystring = {"acctTag": self.__account_tag, "apiSecret": self.__secret_key}
        result_json = self.__get_request.send_request(base_url='https://api.leadsrx.com/v1/',
                                                      resource_uri='conversionIDs.php',
                                                      url_params=querystring)

        handle_response_status(result_json)
        results_object = ConversionIDResult(conversion_id_json=result_json)
        return results_object



