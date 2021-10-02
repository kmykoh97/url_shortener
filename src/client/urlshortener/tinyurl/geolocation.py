import requests



def get_client_ip(request):
   x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
   
   if x_forwarded_for:
       ip = x_forwarded_for.split(',')[0]
   else:
       ip = request.META.get('REMOTE_ADDR')
       
   return ip

def get_geolocation_for_ip(ip):
    url = f"http://api.ipstack.com/{ip}?access_key=f0d1a8c5ed948812f2e85f28428b82a8&fields=country_code"
    response = requests.get(url)
    response.raise_for_status()
    
    return response.json()
    
def geo_result(request):
    geo_info = get_geolocation_for_ip(get_client_ip(request))    
    # print(geo_info.get('country_code'))
    
    return geo_info
