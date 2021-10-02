from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from tinyurl.models import Url, UrlAnalytics
from .lib.tiny import UrlHandler
from django.db.models import Count
from django.contrib.humanize.templatetags.humanize import naturalday, naturaltime
from .lib.parser import parser
import time
import requests
# from .forms import UrlForm



# global view variables
ORIGINAL_URL = 'originalurl'
TINY_URL = 'tinyurl'
TITLETAG = 'title'
TINY_ANALYTICS_URL = 'analytics'

# main page
def index(request):
    originalurldata = request.POST.get('name')
    
    if originalurldata:
        tinyurl = UrlHandler.get_tinyurl(originalurldata)
        titletag = parser(originalurldata)
        analyticsurl = get_full_url(request, tinyurl)+'/a'
        context = {ORIGINAL_URL: originalurldata, TINY_URL: get_full_url(request, tinyurl), TINY_ANALYTICS_URL: analyticsurl, TITLETAG: titletag}
    else:
        context = {ORIGINAL_URL: originalurldata, TINY_URL: '', TITLETAG: ''}
    
    return render(request, 'index.html', context)
    
# test view
def url_detail_view(request):
    url = Url.objects.get(id=1)
    context = {ORIGINAL_URL: url.originalurl}
    
    return render(request, "detail.html", context)

# set shortened url
def url_set(request, url=None):
    if url:
        tinyurl = UrlHandler.get_tinyurl(url)
        titletag = parser(url)
        context = {ORIGINAL_URL: url, TINY_URL: get_full_url(request, tinyurl), TITLETAG: titletag}
    else:
        context = {ORIGINAL_URL: url, TINY_URL: '', TITLETAG: ''}

    return render(request, "maketiny.json", context)
  
# get original url
def url_get(request, hashcode=None):
    context = {}
    context[TINY_URL] = ''
    context[ORIGINAL_URL] = ''

    if hashcode:
        tinyurl = get_full_url(request, hashcode)
        if hashcode:
            context[TINY_URL] = tinyurl if tinyurl else ''
            original_url = UrlHandler.get_originalurl(hashcode)
            context[ORIGINAL_URL] = original_url if original_url else ''
        else:
            print("Invalid url code")
    else:
        print ("Missing url code")

    return render(request, "geturl.json", context)

def redirect_analytics(request, hashcode):
    # tinyurl = get_full_url(request, hashcode)
    urlparent = Url.objects.get(shorturl=hashcode)
    requestgeo = geo_result(request).get('country_code')
    if requestgeo == None:
        requestgeo = 'private'
    new_analytics = UrlAnalytics(url=urlparent, countrycode=requestgeo)
    new_analytics.save()
    
    # if Geo.objects.filter(countrycode=requestgeo).exists():
    #     old_geo = Geo.objects.get(countrycode=requestgeo)
    #     old_geo.noclicks = old_geo.noclicks + 1
    #     old_geo.save()
    #     new_analytics = UrlAnalytics(url=urlparent, geo=oldgeo)
    #     new_analytics.save()
    # else:
    #     new_geo = Geo(countrycode=requestgeo)
    #     new_geo.save()
    #     new_analytics = UrlAnalytics(url=urlparent, geo=newgeo)
    #     new_analytics.save()
        
    print('redirection record completed')

def url_redirect(request, hashcode=None):
    if hashcode:
        original_url = UrlHandler.get_originalurl(hashcode)
        if original_url:
            redirect_analytics(request, hashcode)
            return HttpResponseRedirect(original_url) # emit '//' if force http header
        else:
            print("Invalid short code")
    else:
        print ("Missing short code")
    
    return JsonResponse({'error': 'some error occur'})

# helper function
def get_full_url(request, path):
    return  request.scheme + "://" +  request.get_host() + "/" + path

# helper function
def get_param_from_request(request, key):
    print ("getParamFromRequest. GET = {} \n POST {} \n".format(request.GET, request.POST) )
    ret = None
    
    if key in request.GET:
        ret = request.GET[key]
    else:
        if key in request.POST:
            ret = request.POST[key]

    return ret

def geo_result(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
   
    if x_forwarded_for:
        p = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    url = f"http://api.ipstack.com/{ip}?access_key=f0d1a8c5ed948812f2e85f28428b82a8&fields=country_code"
    response = requests.get(url)
    response.raise_for_status()
    
    geo_info = response.json()
    # print(geo_info.get('country_code'))
    
    return geo_info
    
def view_analytics(request, hashcode):
    old_url = Url.objects.get(shorturl=hashcode)
    noofclicks = UrlAnalytics.objects.filter(url=old_url).count()
    if noofclicks == 0:
        return JsonResponse({'noofclicks': noofclicks, 'detail': 'link never used'})
    lastcountrycode = UrlAnalytics.objects.filter(url=old_url).latest('timestamp').countrycode
    lastcountrycodetime = UrlAnalytics.objects.filter(url=old_url).latest('timestamp').timestamp
    most_common_country = UrlAnalytics.objects.annotate(mc=Count('countrycode')).order_by('-mc')[0].countrycode
    
    return JsonResponse({'clicks': noofclicks, 'last used country': lastcountrycode, 'most frequently use country': most_common_country, 'last used time': naturaltime(lastcountrycodetime)})
    
# def test(request):
#     form = UrlForm()
    
#     return "test"

def test_geo(request):
    return JsonResponse(geo_result(request))



