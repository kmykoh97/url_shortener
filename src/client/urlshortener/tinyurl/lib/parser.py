from urllib.request import urlopen, Request
from bs4 import BeautifulSoup



def parser(external_sites_url):
    # we need to pecify our own header because some websites eg. CoinGecko implements security checks
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    reg_url = external_sites_url
    req = Request(url=reg_url, headers=headers) 
    external_sites_html = urlopen(req).read()
    soup = BeautifulSoup(external_sites_html, "html.parser")
    
    # some website's title is embedded very deep resulting in bs4 not able to scrap them ie: https://www.youtube.com/
    # we need to do exception for them manually
    try:
        title = soup.title.string
    except (IOError, AttributeError):
        title = "this url's title cannot be read because it is using complex framework"
        
    return title
    
# print(parser('https://www.coingecko.com/en'))
