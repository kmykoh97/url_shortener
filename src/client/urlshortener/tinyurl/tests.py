from django.test import TestCase
from tinyurl.models import Url
from .lib.tiny import UrlHandler
from .lib.parser import parser
from .lib.urlvalidator import urlvalidator



class CustomTestCase(TestCase):
    def setUp(self):
        testlongurl = "https://www.coingecko.com/en/coins/deez-nuts"
        Url.objects.create(shorturl="f1db86", originalurl=testlongurl)
        testlongurl = "https://github.com/kmykoh97"
        Url.objects.create(shorturl="exshorturl", originalurl=testlongurl)
        
    # to test if db workable
    def test_db(self):
        testobject = Url.objects.get(shorturl="f1db86")
        # self.assertEqual(getattr(testobject, "originalurl"), "https://www.coingecko.com/en/coins/deez-nuts")
        self.assertEqual(testobject.originalurl, "https://www.coingecko.com/en/coins/deez-nuts")
        testobject = Url.objects.get(shorturl="exshorturl")
        self.assertEqual(testobject.originalurl, "https://github.com/kmykoh97")
    
    # to test if core url shortener algorithm is correct
    def test_core_cal_tiny(self):
        # basic case for long url
        originalurldata = "https://www.google.com/search?q=ibm&oq=ibm&aqs=chrome..69i57j35i39l2j69i60l5.552j0j7&sourceid=chrome&ie=UTF-8"
        tinyurl = UrlHandler.get_tinyurl(originalurldata) # shorten url
        reversegetoriginalurl = UrlHandler.get_originalurl(tinyurl) # revert to original url
        self.assertEqual(reversegetoriginalurl, originalurldata) # checks if core function can return correct original url from shortened url
        
        # basic case for short url
        originalurldata = "https://www.youtube.com/"
        tinyurl = UrlHandler.get_tinyurl(originalurldata)
        reversegetoriginalurl = UrlHandler.get_originalurl(tinyurl)
        self.assertEqual(reversegetoriginalurl, originalurldata)
        
        # dirty db case
        originalurldata = "https://github.com/kmykoh97"
        tinyurl = UrlHandler.get_tinyurl(originalurldata)
        reversegetoriginalurl = UrlHandler.get_originalurl(tinyurl)
        self.assertEqual(reversegetoriginalurl, originalurldata)
        originalurldata = "https://www.coingecko.com/en/coins/deez-nuts"
        tinyurl = UrlHandler.get_tinyurl(originalurldata)
        reversegetoriginalurl = UrlHandler.get_originalurl(tinyurl)
        self.assertEqual(reversegetoriginalurl, originalurldata) 
        
        # repeated db case(cache hit)
        # let's try for 10 repetitions, result shouldn't change
        # we check for cache hit details in log(logging need to be enabled in lib/tiny.py)
        for x in range(10):
            originalurldata = "https://www.coingecko.com/en"
            tinyurl = UrlHandler.get_tinyurl(originalurldata)
            reversegetoriginalurl = UrlHandler.get_originalurl(tinyurl)
            self.assertEqual(reversegetoriginalurl, originalurldata)
        
        # giving random string
        # it should be correct, because we don't check using validator here. We will check using validator later
        originalurldata = "example string"
        tinyurl = UrlHandler.get_tinyurl(originalurldata)
        reversegetoriginalurl = UrlHandler.get_originalurl(tinyurl)
        self.assertEqual(reversegetoriginalurl, originalurldata)
        
    # to test if website content scraper is correct
    def test_title_parser(self):
        # website without header check
        originalurl = "https://www.google.com/"
        titletag = parser(originalurl)
        self.assertEqual(titletag, "Google") # checks if bs4 scraper is working
        
        # website with header check
        originalurl = "https://www.coingecko.com/en"
        titletag = parser(originalurl)
        self.assertEqual(titletag, "CoinGecko: Cryptocurrency Prices and Market Capitalization")
        
    # to test if url validator is working
    def test_validator(self):
        # correct case
        url = "https://github.com/kmykoh97"
        validatorresult = urlvalidator(url)
        self.assertEqual(validatorresult, True) # checks if our lib returns true for correct url
        url = "https://www.google.com/search?q=ibm&oq=ibm&aqs=chrome..69i57j35i39l2j69i60l5.552j0j7&sourceid=chrome&ie=UTF-8"
        validatorresult = urlvalidator(url)
        self.assertEqual(validatorresult, True)
        
        # wrong case
        url = "www.google.com/"
        validatorresult = urlvalidator(url)
        self.assertEqual(validatorresult, False) # checks if our lib returns false for incorrect url
        url = "coingecko is good"
        validatorresult = urlvalidator(url)
        self.assertEqual(validatorresult, False)
        url = "helloworld.com"
        validatorresult = urlvalidator(url)
        self.assertEqual(validatorresult, False)

    # note that we do not need to check location service because it is api provided by ipstack
