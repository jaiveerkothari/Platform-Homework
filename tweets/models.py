from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.

@python_2_unicode_compatible  # only if you need to support Python 2
class TwitterAccounts(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    twitter_id = models.BigIntegerField(unique=True)
    oauth_token = models.CharField(max_length=60)
    oauth_secret = models.CharField(max_length=60)

    def __str__(self):
        return str(self.twitter_id)

    class Meta:
        db_table = 'twitter_accounts'
