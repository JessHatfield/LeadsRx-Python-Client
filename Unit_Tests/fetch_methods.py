import unittest
from LeadRx.client import client as LeadRXClient
import httpretty
import json
from re import compile
from requests import HTTPError


def groupings_request_callback(request, uri, response_headers):
    response = {
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
    expected_url='https://api.leadsrx.com/v1/groupIDs.php?acctTag=thisisafaketag12&apiSecret=thisisafakeid12&withTouchpoints=True'
    assert uri == expected_url, f'\n URL provided \n {uri} \n Did not match expected url \n {expected_url}'

    return [200, response_headers, json.dumps(response)]


def domains_request_callback(request, uri, response_headers):
    response = {
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
    expected_url = 'https://api.leadsrx.com/v1/getDomains.php?acctTag=thisisafaketag12&apiSecret=thisisafakeid12'
    assert uri == expected_url, f'\n URL provided \n {uri} \n Did not match expected url \n {expected_url}'

    return [200, response_headers, json.dumps(response)]


def conversionsid_request_callback(request, uri, response_headers):
    response = {
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
    expected_url = 'https://api.leadsrx.com/v1/conversionIDs.php?acctTag=thisisafaketag12&apiSecret=thisisafakeid12'
    assert uri == expected_url, f'\n URL provided \n {uri} \n Did not match expected url \n {expected_url}'

    return [200, response_headers, json.dumps(response)]


def conversions_request_callback(request, uri, response_headers):
    response = {
        "status": 0,
        "message": "ok",
        "resultCount": 1,
        "results": [
            {
                "ID": 12345,
                "conversionID": 24,
                "conversionTS": 1569874534,
                "conversionLocalTS": 1569874534,
                "conversionDateTime": "2019-09-30 22:59:59",
                "conversionLocalDateTime": "2019-09-30 20:59:59",
                "attributionPathCount": 3,
                "attributionPath": [
                    129,
                    192,
                    341
                ],
                "touchpointDateTimes": [
                    "2019-09-30 22:59:59",
                    "2019-09-27 20:39:19",
                    "2019-09-26 19:44:07"
                ],
                "profile": {
                    "0": {
                        "firstName": "Jane",
                        "lastName": "Doe"
                    },
                    "lrxID": "123"
                },
                "profileID": 474,
                "geoData": [
                    {
                        "country": "United States",
                        "state": "Oregon",
                        "city": "Portland",
                        "region": "Northwest"
                    }
                ]
            }
        ]
    }
    expected_url='https://api.leadsrx.com/v1/conversions.php?acctTag=thisisafaketag12&apiSecret=thisisafakeid12&conversionID=%2A&endDateTime=2021-01-30+00%3A00%3A00&landingPage=yes&startDateTime=2021-01-01+00%3A00%3A00&usePacific=1'
    assert uri == expected_url, f'\n URL provided \n {uri} \n Did not match expected url \n {expected_url}'

    return [200, response_headers, json.dumps(response)]


def conversions_request_callback_for_single_visitor_id(request, uri, response_headers):
    response = {
        "status": 0,
        "message": "ok",
        "resultCount": 1,
        "results": [
            {
                "ID": 12345,
                "conversionID": 24,
                "conversionTS": 1569874534,
                "conversionLocalTS": 1569874534,
                "conversionDateTime": "2019-09-30 22:59:59",
                "conversionLocalDateTime": "2019-09-30 20:59:59",
                "attributionPathCount": 3,
                "attributionPath": [
                    129,
                    192,
                    341
                ],
                "touchpointDateTimes": [
                    "2019-09-30 22:59:59",
                    "2019-09-27 20:39:19",
                    "2019-09-26 19:44:07"
                ],
                "profile": {
                    "0": {
                        "firstName": "Jane",
                        "lastName": "Doe"
                    },
                    "lrxID": "123"
                },
                "profileID": 474,
                "geoData": [
                    {
                        "country": "United States",
                        "state": "Oregon",
                        "city": "Portland",
                        "region": "Northwest"
                    }
                ]
            }
        ]
    }
    expected_url='https://api.leadsrx.com/v1/conversions.php?acctTag=thisisafaketag12&apiSecret=thisisafakeid12&conversionID=%2A&endDateTime=2021-01-30+00%3A00%3A00&landingPage=yes&startDateTime=2021-01-01+00%3A00%3A00&usePacific=1&visitorID=1522653355'
    assert uri == expected_url, f'\n URL provided \n {uri} \n Did not match expected url \n {expected_url}'

    return [200, response_headers, json.dumps(response)]


def touchpoint_request_callback(request, uri, response_headers):
    response = {
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
    expected_url = 'https://api.leadsrx.com/v1/touchpoints.php?acctTag=thisisafaketag12&apiSecret=thisisafakeid12&campaignID=123&conversionID=%2A&endDateTime=2021-01-30+00%3A00%3A00&leadType=all&startDateTime=2021-01-01+00%3A00%3A00&usePacific=1'
    assert uri == expected_url, f'\n URL provided \n {uri} \n Did not match expected url \n {expected_url}'

    return [200, response_headers, json.dumps(response)]

def error_in_response(request, uri, response_headers):
    response = 'We apologize, but there\'s been a system error.  Tech support has been notified.'


    return [200, response_headers, response]


def campaign_id_request_callback(request, uri, response_headers):
    response = {
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

    expected_url = 'https://api.leadsrx.com/v1/campaignIDs.php?acctTag=thisisafaketag12&apiSecret=thisisafakeid12'
    assert uri == expected_url, f'\n URL provided \n {uri} \n Did not match expected url \n {expected_url}'

    return [200, response_headers, json.dumps(response)]


class TestLeadRXErrorText(unittest.TestCase):
    #LeadsRX like to return 200 responses where the text is actually just an error string! -_-
    @httpretty.activate
    def test_error_handled(self):
        httpretty.register_uri(
            httpretty.GET, compile(r'https://'), body=error_in_response
        )

        client = LeadRXClient(secret_key="thisisafakeid12", account_tag="thisisafaketag12")
        self.assertRaises(HTTPError, client.pull_campaign_ids)


class TestCampaignID(unittest.TestCase):

    @httpretty.activate
    def test_api_request_is_valid(self):
        httpretty.register_uri(
            httpretty.GET, compile(r'https://'), body=campaign_id_request_callback
        )
        client = LeadRXClient(secret_key="thisisafakeid12", account_tag="thisisafaketag12")
        client.pull_campaign_ids()


class TestTouchPoints(unittest.TestCase):

    def test_invalid_lead_type(self):
        client = LeadRXClient(secret_key="thisisafakeid12", account_tag="thisisafaketag12")

        with self.assertRaises(TypeError):
            client.pull_touchpoints(startDateTimeStr="2021-01-01 00:00:00", endDateTimeStr="2021-01-30 00:00:00",
                                    lead_type="blooop")

    @httpretty.activate
    def test_api_request_is_valid(self):
        httpretty.register_uri(
            httpretty.GET, compile(r'https://'),
            body=touchpoint_request_callback

        )

        client = LeadRXClient(secret_key="thisisafakeid12", account_tag="thisisafaketag12")
        client.pull_touchpoints(campaignID='123', startDateTimeStr="2021-01-01 00:00:00",
                                endDateTimeStr="2021-01-30 00:00:00")


class TestFetchDomains(unittest.TestCase):

    @httpretty.activate
    def test_api_request_is_valid(self):
        httpretty.register_uri(
            httpretty.GET, compile(r'https://'),
            body=domains_request_callback

        )

        client = LeadRXClient(secret_key="thisisafakeid12", account_tag="thisisafaketag12")
        client.pull_domains()


class TestConversionsID(unittest.TestCase):

    @httpretty.activate
    def test_api_request_is_valid(self):
        httpretty.register_uri(
            httpretty.GET, compile(r'https://'),
            body=conversionsid_request_callback

        )

        client = LeadRXClient(secret_key="thisisafakeid12", account_tag="thisisafaketag12")
        client.pull_conversion_ids()


class TestGroupingsID(unittest.TestCase):

    @httpretty.activate
    def test_api_request_is_valid(self):
        httpretty.register_uri(
            httpretty.GET, compile(r'https://'),
            body=groupings_request_callback

        )

        client = LeadRXClient(secret_key="thisisafakeid12", account_tag="thisisafaketag12")
        client.pull_grouping_ids()


class TestConversions(unittest.TestCase):

    @httpretty.activate
    def test_api_request_is_valid_single_visitor_id(self):
        httpretty.register_uri(
            httpretty.GET, compile(r'https://'),
            body=conversions_request_callback_for_single_visitor_id

        )

        client = LeadRXClient(secret_key="thisisafakeid12", account_tag="thisisafaketag12")
        client.pull_conversions(startDateTimeStr="2021-01-01 00:00:00", endDateTimeStr="2021-01-30 00:00:00",
                                visitorID="1522653355")

    @httpretty.activate
    def test_api_request_is_valid(self):
        httpretty.register_uri(
            httpretty.GET, compile(r'https://'),
            body=conversions_request_callback

        )

        client = LeadRXClient(secret_key="thisisafakeid12", account_tag="thisisafaketag12")
        client.pull_conversions(startDateTimeStr="2021-01-01 00:00:00", endDateTimeStr="2021-01-30 00:00:00")


if __name__ == '__main__':
    unittest.main()
