from django.test import TestCase
from tinyurl.models import Url
from .lib.tiny import UrlHandler
from .lib.parser import parser



class CustomTestCase(TestCase):
    def setUp(self):
        testlongurl = "https://www.coingecko.com/en/coins/deez-nuts"
        Url.objects.create(shorturl="f1db86", originalurl=testlongurl)
        
    # to test if db workable
    def test_db(self):
        testobject = Url.objects.get(shorturl="f1db86")
        # self.assertEqual(getattr(testobject, "originalurl"), "https://www.coingecko.com/en/coins/deez-nuts")
        self.assertEqual(testobject.originalurl, "https://www.coingecko.com/en/coins/deez-nuts")
    
    # to test if core url shortener algorithm is correct
    def test_core_cal_tiny(self):
        originalurldata = "https://www.google.com/search?q=ibm&oq=ibm&aqs=chrome..69i57j35i39l2j69i60l5.552j0j7&sourceid=chrome&ie=UTF-8"
        tinyurl = UrlHandler.get_tinyurl(originalurldata)
        reversegetoriginalurl = UrlHandler.get_originalurl(tinyurl)
        self.assertEqual(reversegetoriginalurl, originalurldata) # checks if core function can return correct original url from shortened url
        
    # to test if website content scraper is correct
    def test_title_parser(self):
        originalurl = "https://www.google.com/"
        titletag = parser(originalurl)
        self.assertEqual(titletag, "Google") # checks if bs4 scraper is working

    # note that we do not need to check location service because it is api provided by ipstack
