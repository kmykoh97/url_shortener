from django.db import models
from django.utils.timezone import now

# Create your models here.
class Url(models.Model):
    shorturl = models.CharField(max_length=15, primary_key=True)
    originalurl = models.CharField(max_length=500)

class UrlAnalytics(models.Model):
    url = models.ForeignKey(Url, on_delete=models.CASCADE)
    countrycode = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
