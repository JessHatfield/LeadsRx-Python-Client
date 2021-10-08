import unittest
from src.LeadsRx.client import ConversionResult, ConversionIDResult, TouchPointResult, handle_response_status, \
    LeadRXRequestError, DomainResults, GroupingsResult, InteractionResult, AttributionResult
from pandas import DataFrame
import pandas.testing as pd_testing


class ConversionIdResultTest(unittest.TestCase):

    def assertDataframeEqual(self, a, b, msg):
        try:
            ##ignores order of column and rows
            pd_testing.assert_frame_equal(a, b, check_like=True, check_dtype=False, check_exact=False)
        except AssertionError as e:
            raise self.failureException(msg) from e

    def test_Extract_Single_Result_DataFrame(self):

        self.addTypeEqualityFunc(DataFrame, self.assertDataframeEqual)
        single_result = {
            "status": 0,
            "message": "ok",
            "resultCount": 3,
            "results": [
                {
                    "campaignID": "306",
                    "campaignName": "Retargeting ads"
                },
                {
                    "campaignID": "314",
                    "campaignName": "Direct Visits"
                },
                {
                    "campaignID": "315",
                    "campaignName": "Referral Visit"
                }
            ]
        }

        expected_results = DataFrame(
            [{'campaignID': "306", "campaignName": "Retargeting ads"},
             {'campaignID': "314", "campaignName": "Direct Visits"},
             {'campaignID': "315", "campaignName": "Referral Visit"}])

        result_object = ConversionIDResult(single_result)

        dataframe_result = result_object.dataframe

        self.assertEqual(dataframe_result, expected_results)

    def test_Extract_Single_Result_JSON(self):
        single_result = {
            "status": 0,
            "message": "ok",
            "resultCount": 3,
            "results": [
                {
                    "conversionID": "24",
                    "conversionName": "Signed up for free trial"
                },
                {
                    "conversionID": "25",
                    "conversionName": "Submitted Contact Form"
                },
                {
                    "conversionID": "221",
                    "conversionName": "Requested a demo"
                }
            ]
        }

        expected_results = [{"conversionID": "24", "conversionName": "Signed up for free trial"},
                            {"conversionID": "25", "conversionName": "Submitted Contact Form"},
                            {"conversionID": "221", "conversionName": "Requested a demo"}]

        result_object = ConversionIDResult(single_result)
        json_result = result_object.json

        self.assertEqual(json_result, expected_results)


class InteractionsResultTest(unittest.TestCase):

    def assertDataframeEqual(self, a, b, msg):
        try:
            ##ignores order of column and rows
            pd_testing.assert_frame_equal(a, b, check_like=True, check_dtype=False, check_exact=False)
        except AssertionError as e:
            raise self.failureException(msg) from e

    def test_no_results(self):
        self.addTypeEqualityFunc(DataFrame, self.assertDataframeEqual)
        single_result={'status': '0', 'message': 'ok', 'results': {'totalInteractions': 0, 'byDay': {'2021-01-01': 0}, 'byDOW': [], 'byHour': []}}

        result=InteractionResult(single_result,campaign_id="123")

        self.assertEqual(result.by_day_results_json,[{'Date':'2021-01-01','Interactions':0,'CampaignID':'123'}])

        expected_by_day_dataframe=DataFrame([{'Date':'2021-01-01','Interactions':0,"CampaignID":"123"}])
        results_by_day=result.by_day_results_dataframe
        self.assertEqual(expected_by_day_dataframe,results_by_day)


    def test_extract_single_result_json_and_dataframe(self):
        self.addTypeEqualityFunc(DataFrame, self.assertDataframeEqual)
        single_result = {
            "status": "0",
            "message": "ok",
            "results": {
                "totalInteractions": 17,
                "byDay": {
                    "2020-04-24": 4,
                    "2020-04-25": 0,
                    "2020-04-26": 1,
                    "2020-04-27": 2,
                    "2020-04-28": 4,
                    "2020-04-29": 1,
                    "2020-04-30": 2,
                    "2020-05-01": 1,
                    "2020-05-02": 1,
                    "2020-05-03": 1
                },
                "byDOW": {
                    "Friday": 5,
                    "Saturday": 1,
                    "Sunday": 2,
                    "Monday": 2,
                    "Tuesday": 4,
                    "Wednesday": 1,
                    "Thursday": 2
                },
                "byHour": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
            }
        }

        expected_by_day = [{'Date': "2020-04-24", 'Interactions': 4, 'CampaignID': '123'},
                           {'Date': "2020-04-25", 'Interactions': 0, 'CampaignID': '123'},
                           {'Date': "2020-04-26", 'Interactions': 1, 'CampaignID': '123'},
                           {'Date': "2020-04-27", 'Interactions': 2, 'CampaignID': '123'},
                           {'Date': "2020-04-28", 'Interactions': 4, 'CampaignID': '123'},
                           {'Date': "2020-04-29", 'Interactions': 1, 'CampaignID': '123'},
                           {'Date': "2020-04-30", 'Interactions': 2, 'CampaignID': '123'},
                           {'Date': "2020-05-01", 'Interactions': 1, 'CampaignID': '123'},
                           {'Date': "2020-05-02", 'Interactions': 1, 'CampaignID': '123'},
                           {'Date': "2020-05-03", 'Interactions': 1, 'CampaignID': '123'}]

        expected_by_DOW = [{'Day_Of_Week': 'Friday', 'Interactions': 5, 'CampaignID': '123'},
                           {'Day_Of_Week': 'Saturday', 'Interactions': 1, 'CampaignID': '123'},
                           {'Day_Of_Week': 'Sunday', 'Interactions': 2, 'CampaignID': '123'},
                           {'Day_Of_Week': 'Monday', 'Interactions': 2, 'CampaignID': '123'},
                           {'Day_Of_Week': 'Tuesday', 'Interactions': 4, 'CampaignID': '123'},
                           {'Day_Of_Week': 'Wednesday', 'Interactions': 1, 'CampaignID': '123'},
                           {'Day_Of_Week': 'Thursday', 'Interactions': 2, 'CampaignID': '123'},

                           ]

        expected_by_hour = [{'Hour_Of_Day': 0, 'Interactions': 0, 'CampaignID': '123'},
                            {'Hour_Of_Day': 1, 'Interactions': 1, 'CampaignID': '123'},
                            {'Hour_Of_Day': 2, 'Interactions': 2, 'CampaignID': '123'},
                            {'Hour_Of_Day': 3, 'Interactions': 3, 'CampaignID': '123'},
                            {'Hour_Of_Day': 4, 'Interactions': 4, 'CampaignID': '123'},
                            {'Hour_Of_Day': 5, 'Interactions': 5, 'CampaignID': '123'},
                            {'Hour_Of_Day': 6, 'Interactions': 6, 'CampaignID': '123'},
                            {'Hour_Of_Day': 7, 'Interactions': 7, 'CampaignID': '123'},
                            {'Hour_Of_Day': 8, 'Interactions': 8, 'CampaignID': '123'},
                            {'Hour_Of_Day': 9, 'Interactions': 9, 'CampaignID': '123'},
                            {'Hour_Of_Day': 10, 'Interactions': 10, 'CampaignID': '123'},
                            {'Hour_Of_Day': 11, 'Interactions': 11, 'CampaignID': '123'},
                            {'Hour_Of_Day': 12, 'Interactions': 12, 'CampaignID': '123'},
                            {'Hour_Of_Day': 13, 'Interactions': 13, 'CampaignID': '123'},
                            {'Hour_Of_Day': 14, 'Interactions': 14, 'CampaignID': '123'},
                            {'Hour_Of_Day': 15, 'Interactions': 15, 'CampaignID': '123'},
                            {'Hour_Of_Day': 16, 'Interactions': 16, 'CampaignID': '123'},
                            {'Hour_Of_Day': 17, 'Interactions': 17, 'CampaignID': '123'},
                            {'Hour_Of_Day': 18, 'Interactions': 18, 'CampaignID': '123'},
                            {'Hour_Of_Day': 19, 'Interactions': 19, 'CampaignID': '123'},
                            {'Hour_Of_Day': 20, 'Interactions': 20, 'CampaignID': '123'},
                            {'Hour_Of_Day': 21, 'Interactions': 21, 'CampaignID': '123'},
                            {'Hour_Of_Day': 22, 'Interactions': 22, 'CampaignID': '123'},
                            {'Hour_Of_Day': 23, 'Interactions': 23, 'CampaignID': '123'},

                            ]
        results_object = InteractionResult(single_result, campaign_id='123')
        by_day = results_object.by_day_results_json
        by_day_of_week = results_object.day_of_week_json
        by_hour_of_day = results_object.hour_of_day_json

        self.assertEqual(by_day, expected_by_day)
        self.assertEqual(by_day_of_week, expected_by_DOW)
        self.assertEqual(by_hour_of_day, expected_by_hour)


class TouchPointResultTest(unittest.TestCase):

    def assertDataframeEqual(self, a, b, msg):
        try:
            ##ignores order of column and rows
            pd_testing.assert_frame_equal(a, b, check_like=True, check_dtype=False, check_exact=False)
        except AssertionError as e:
            raise self.failureException(msg) from e

    def test_extract_single_result_json_and_dataframe(self):
        self.addTypeEqualityFunc(DataFrame, self.assertDataframeEqual)
        single_result = {
            "status": 0,
            "message": "ok",
            "results": {
                "total": {
                    "conversions": 4,
                    "revenue": 0
                },
                "byDay": {
                    "conversions": {
                        "2019-03-05": 1,
                        "2019-03-06": 3
                    },
                    "revenue": {
                        "2019-03-05": 0,
                        "2019-03-06": 10
                    }
                }
            }
        }

        expected_by_total = [{'results.total.conversions': 4, 'results.total.revenue': 0, 'campaignID': '123'}]
        expected_by_day = [
            {'Date': "2019-03-05", 'results.byDay.conversions': 1, 'results.byDay.revenue': 0, 'campaignID': '123'},
            {'Date': "2019-03-06", 'results.byDay.conversions': 3, 'results.byDay.revenue': 10, 'campaignID': '123'}
        ]
        results_object = TouchPointResult(single_result, campaign_id='123')
        by_day = results_object.by_day_results_json
        by_total = results_object.total_results_json

        self.assertEqual(by_day, expected_by_day)
        self.assertEqual(results_object.by_day_results_dataframe, DataFrame(expected_by_day))
        self.assertEqual(by_total, expected_by_total)
        self.assertEqual(results_object.total_results_dataframe, DataFrame(expected_by_total))


class AttributionResultTests(unittest.TestCase):

    def assertDataframeEqual(self, a, b, msg):
        try:
            ##ignores order of column and rows
            pd_testing.assert_frame_equal(a, b, check_like=True, check_dtype=False, check_exact=False)
        except AssertionError as e:
            raise self.failureException(msg) from e

    def test_extract_two_results_json_and_dataframe(self):

        self.addTypeEqualityFunc(DataFrame, self.assertDataframeEqual)
        api_response = {'status': '0', 'results': [{'id': '555986', 'count': 22.42, 'value': 519.55, 'cost': 154.12},
                                                   {'id': '554588', 'count': 18, 'value': 479.7, 'cost': 0}],
                        'resultCount': 2, 'totalConversions': 40.42, 'totalValue': 999.25, 'message': 'ok'}
        result_object = AttributionResult(api_response)

        result_json = result_object.json
        expected_json = [
            {'Campaign_ID': '555986', 'Conversion_Total': 22.42, 'Conversion_Value': 519.55, 'Conversion_Cost': 154.12},
            {'Campaign_ID': '554588', 'Conversion_Total': 18, 'Conversion_Value': 479.7, 'Conversion_Cost': 0}]

        self.assertEqual(result_json, expected_json)

        self.assertEqual(result_object.dataframe,DataFrame(expected_json))




class ConversionResultTests(unittest.TestCase):

    def assertDataframeEqual(self, a, b, msg):
        try:
            ##ignores order of column and rows
            pd_testing.assert_frame_equal(a, b, check_like=True, check_dtype=False, check_exact=False)
        except AssertionError as e:
            raise self.failureException(msg) from e

    def test_extract_single_result_landingPage_json(self):

        single_result = {"status": 0, "message": "ok", "resultCount": 1, 'results': [
            {'ID': '624760', 'conversionID': '13697', 'conversionTS': 1609459687, 'conversionLocalTS': 1609488487,
             'conversionDateTime': '2020-12-31 16:08:07', 'conversionLocalDateTime': '2021-01-01 00:08:07',
             'attributionPathCount': 1, 'attributionPath': ['555986'], 'touchpointDateTimes': ['2021-01-01 0:05:56'],
             'profile': {'0': {'orderID': 658427, 'leadValue': '6.95', 'firstName': 'Laura', 'lastName': 'Garcia',
                               'email': 'laura.ggracia@gmail.com', 'phone': '07435360757', 'city': 'Coventry',
                               'state': None, 'zipcode': 'CV3 5EQ', 'status': 'paid'}, 'lrxID': '1522653355'},
             'profileID': '49372545', 'geoData': [
                {'country_code': 'GB', 'country_name': 'United Kingdom of Great Britain and Northern Ireland',
                 'region_name': 'England', 'city': 'Birmingham', 'isp': 'Vodafone Ltd', 'zip': 'B3', 'metro': None}],
             'conversionValue': '6.95',
             'landingPage': 'https://www.vitabiotics.com/products/wellkid-peppa-pig-vitamin-d?variant=29084141027397&gclid=CjwKCAiAirb_BRBNEiwALHlnDyv-zhYhxyy46pKNCpquemVzdLsINht7tWfFb2G1yOsgS0P1sZ3_jRoCGOoQAvD_BwE'}]}

        result_object = ConversionResult(single_result)

        expected_result = [
            {'ID': '624760', 'conversionID': '13697', 'conversionTSUnix': 1609459687,
             'conversionLocalTSUnix': 1609488487,
             'conversionDateTime': '2020-12-31 16:08:07', 'conversionLocalDateTime': '2021-01-01 00:08:07',
             'profile.firstName': 'Laura', 'profile.lastName': 'Garcia', 'lrxID': '1522653355',
             'attribution_path_id': '555986', 'touchpointDateTime': '2021-01-01 0:05:56',
             'landingPage': 'https://www.vitabiotics.com/products/wellkid-peppa-pig-vitamin-d?variant=29084141027397&gclid=CjwKCAiAirb_BRBNEiwALHlnDyv-zhYhxyy46pKNCpquemVzdLsINht7tWfFb2G1yOsgS0P1sZ3_jRoCGOoQAvD_BwE'}]

        self.assertEqual(result_object.json, expected_result)

    def test_Extract_Single_Result_JSON_And_Dataframe(self):

        self.addTypeEqualityFunc(DataFrame, self.assertDataframeEqual)
        single_result = {"status": 0,
                         "message": "ok",
                         'results': [{'ID': '624760', 'conversionID': '13697', 'conversionTS': 1609459687,
                                      'conversionLocalTS': 1609488487,
                                      'conversionDateTime': '2020-12-31 16:08:07',
                                      'conversionLocalDateTime': '2021-01-01 00:08:07',
                                      'attributionPathCount': 1, 'attributionPath': ['555986'],
                                      'touchpointDateTimes': ['2021-01-01 0:05:56'],
                                      'profile': {
                                          '0': {'orderID': 658427, 'leadValue': '6.95', 'firstName': 'Laura',
                                                'lastName': 'Garcia',
                                                'email': 'laura.ggracia@gmail.com', 'phone': '07435360757',
                                                'city': 'Coventry',
                                                'state': None, 'zipcode': 'CV3 5EQ', 'status': 'paid'},
                                          'lrxID': '1522653355'},
                                      'profileID': '49372545', 'geoData': [
                                 {'country_code': 'GB',
                                  'country_name': 'United Kingdom of Great Britain and Northern Ireland',
                                  'region_name': 'England', 'city': 'Birmingham', 'isp': 'Vodafone Ltd', 'zip': 'B3',
                                  'metro': None}],
                                      'conversionValue': '6.95'}],

                         'resultCount': 1

                         }
        result_object = ConversionResult(single_result)
        expected_result = [
            {'ID': 12345, 'conversionID': 24, 'conversionTSUnix': 1569874534, 'conversionLocalTSUnix': 1569874534,
             'conversionDateTime': '2019-09-30 22:59:59', 'conversionLocalDateTime': '2019-09-30 20:59:59',
             'profile.firstName': 'Jane', 'profile.lastName': 'Doe', 'lrxID': '123', 'geoData.country': 'United States',
             'geoData.state': 'Oregon', 'geoData.city': 'Portland', 'geoData.region': 'Northwest',
             'attribution_path_id': 129, 'touchpointDateTime': '2019-09-30 22:59:59'},
            {'ID': 12345, 'conversionID': 24, 'conversionTSUnix': 1569874534, 'conversionLocalTSUnix': 1569874534,
             'conversionDateTime': '2019-09-30 22:59:59', 'conversionLocalDateTime': '2019-09-30 20:59:59',
             'profile.firstName': 'Jane', 'profile.lastName': 'Doe', 'lrxID': '123', 'geoData.country': 'United States',
             'geoData.state': 'Oregon', 'geoData.city': 'Portland', 'geoData.region': 'Northwest',
             'attribution_path_id': 192, 'touchpointDateTime': '2019-09-27 20:39:19'},
            {'ID': 12345, 'conversionID': 24, 'conversionTSUnix': 1569874534, 'conversionLocalTSUnix': 1569874534,
             'conversionDateTime': '2019-09-30 22:59:59', 'conversionLocalDateTime': '2019-09-30 20:59:59',
             'profile.firstName': 'Jane', 'profile.lastName': 'Doe', 'lrxID': '123', 'geoData.country': 'United States',
             'geoData.state': 'Oregon', 'geoData.city': 'Portland', 'geoData.region': 'Northwest',
             'attribution_path_id': 341, 'touchpointDateTime': '2019-09-26 19:44:07'}]

        expected_dataframe = DataFrame(expected_result)

        self.assertEqual(result_object.json, expected_result)
        self.assertEqual(result_object.dataframe, expected_dataframe)


class DomainsResultTest(unittest.TestCase):

    def test_extract_domains_json(self):
        single_results = {
            "status": 0,
            "message": "ok",
            "resultCount": 2,
            "results": [
                {
                    "domain": "leadsrx.com"
                },
                {
                    "domain": "app2.leadsrx.com"
                }
            ]
        }

        expected_results = [{"domain": "leadsrx.com"}, {'domain': 'app2.leadsrx.com'}]

        result_object = DomainResults(single_results).json

        self.assertEqual(result_object, expected_results)


class GroupingsIDTests(unittest.TestCase):

    def test_extract_grouping_ids_json(self):
        single_result = {
            "status": 0,
            "message": "ok",
            "resultCount": 2,
            "results": [
                {
                    "groupingID": "11",
                    "groupingName": "Digital Ads",
                    "touchpoints": "221,431,574"
                },
                {
                    "groupingID": "49",
                    "groupingName": "Social marketing",
                    "touchpoints": None
                }
            ]
        }

        expected_results = [{"groupingID": "11", "groupingName": "Digital Ads", "touchpoints": '221,431,574'},
                            {'groupingID': "49", 'groupingName': 'Social marketing', "touchpoints": None}]

        result_object = GroupingsResult(single_result).json

        self.assertEqual(result_object, expected_results)


class ConversionIdResultTest(unittest.TestCase):

    def assertDataframeEqual(self, a, b, msg):
        try:
            ##ignores order of column and rows
            pd_testing.assert_frame_equal(a, b, check_like=True, check_dtype=False, check_exact=False)
        except AssertionError as e:
            raise self.failureException(msg) from e

    def test_Extract_Single_Result_DataFrame(self):

        self.addTypeEqualityFunc(DataFrame, self.assertDataframeEqual)
        single_result = {
            "status": 0,
            "message": "ok",
            "resultCount": 3,
            "results": [
                {
                    "conversionID": "24",
                    "conversionName": "Signed up for free trial"
                },
                {
                    "conversionID": "25",
                    "conversionName": "Submitted Contact Form"
                },
                {
                    "conversionID": "221",
                    "conversionName": "Requested a demo"
                }
            ]
        }

        expected_results = DataFrame([{"conversionID": "24", "conversionName": "Signed up for free trial"},
                                      {"conversionID": "25", "conversionName": "Submitted Contact Form"},
                                      {"conversionID": "221", "conversionName": "Requested a demo"}])

        result_object = ConversionIDResult(single_result)
        dataframe_result = result_object.dataframe

        self.assertEqual(dataframe_result, expected_results)

    def test_Extract_Single_Result_JSON(self):
        single_result = {
            "status": 0,
            "message": "ok",
            "resultCount": 3,
            "results": [
                {
                    "conversionID": "24",
                    "conversionName": "Signed up for free trial"
                },
                {
                    "conversionID": "25",
                    "conversionName": "Submitted Contact Form"
                },
                {
                    "conversionID": "221",
                    "conversionName": "Requested a demo"
                }
            ]
        }

        expected_results = [{"conversionID": "24", "conversionName": "Signed up for free trial"},
                            {"conversionID": "25", "conversionName": "Submitted Contact Form"},
                            {"conversionID": "221", "conversionName": "Requested a demo"}]

        result_object = ConversionIDResult(single_result)
        json_result = result_object.json

        self.assertEqual(json_result, expected_results)


class StatusHandler(unittest.TestCase):

    def test_succcess_message(self):
        result_json = {'status': 0, 'message': 'ok'}
        passbool = handle_response_status(result_json)
        self.assertEqual(True, passbool)

    def test_success_message_string(self):
        result_json = {'status': '0', 'message': 'ok'}
        passbool = handle_response_status(result_json)
        self.assertEqual(True, passbool)

    def test_error_message(self):
        result_json = {'status': 3, 'message': 'Missing required data fields'}
        with self.assertRaises(LeadRXRequestError):
            handle_response_status(result_json)


if __name__ == '__main__':
    unittest.main()
