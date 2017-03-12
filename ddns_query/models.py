from django.db import models

# Create your models here.


class Dyname(models.Model):
    prefix = models.CharField('domain prefix', max_length=15, unique=True)
    ip = models.GenericIPAddressField('current ip')
    mod = models.DateTimeField('last modified', auto_now=True)

    def __str__(self):
        return self.prefix
