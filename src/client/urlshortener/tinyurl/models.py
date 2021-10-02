from django.db import models
from django.utils.timezone import now



# table to store Url mappings
class Url(models.Model):
    shorturl = models.CharField(max_length=15, primary_key=True)
    originalurl = models.CharField(max_length=500)

# table to record each redirection used
# foreign key to Url for more efficient analytics
class UrlAnalytics(models.Model):
    url = models.ForeignKey(Url, on_delete=models.CASCADE)
    countrycode = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    
# this table uses to store Title Tag to prevent application from running scraper all the time for same urls
# we create a new model in DB because of scaling consideration
# this TitleTag table might become huge and impose serious problems over time
# with a separate table(horizontal sharding), we can freely delete the whole table(or partial) if ever this table becomes our performance bottleneck
class TitleTag(models.Model):
    longurl = models.CharField(max_length=500)
    titletag = models.CharField(max_length=150)
