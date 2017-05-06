from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    pass


class Dyname(models.Model):
    prefix = models.CharField('domain prefix', max_length=15, unique=True)
    zone = models.URLField("DNS zone", default='ddns.aszabados.eu')
    primary_dns_host = models.URLField(
        "Primary DNS server hostname",
        default='ns1.aszabados.eu'
    )
    primary_dns_ip = models.GenericIPAddressField(
        'Primary DNS server IP',
        default='188.213.166.188'
    )
    ip = models.GenericIPAddressField('current ip')
    mod = models.DateTimeField('last modified', auto_now=True)
    token = models.CharField('renewal token', max_length=50, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.prefix
