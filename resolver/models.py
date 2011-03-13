from django.db import models

class Prefix(models.Model):
    prefix = models.CharField(max_length=255, unique=True)
    redirect_url = models.CharField(max_length=255, blank=True)
    redirect_on_miss = models.BooleanField(default=False)
    mint = models.BooleanField(default=False)
    next_id = models.IntegerField(default=1)
    allow_feed = models.BooleanField(default=True)

    def __unicode__(self):
        return self.prefix


FEED_TYPE_CHOICES = (
        ('OAIPMH', 'OAI-PMH'),
        ('AFEED', 'Atom Feed')
    )

FEED_STATUS_CHOICES = (
        ('IDLE', 'Idle'),
        ('RUNNING', 'Running'),
        ('ERROR', 'Error')
    )

class Feed(models.Model):
    prefix = models.ForeignKey(Prefix)
    type = models.CharField(max_length=32, choices=FEED_TYPE_CHOICES)
    status = models.CharField(max_length=32, choices=FEED_STATUS_CHOICES)
    status_message = models.TextField(blank=True)
    refresh_rate = models.IntegerField(default=10*60)
    base_url = models.CharField(max_length=255)
    extra_url_parameters=models.CharField(max_length=255)
    latest_timestamp = models.DateTimeField(blank=True, null=True)
    next_harvest = models.DateTimeField(blank=True, null=True)
    last_harvest = models.DateTimeField(blank=True, null=True)
    xslt_transform = models.TextField(blank=True)
    n_retries = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.prefix) + '(' + self.type + ')'


class Identifier(models.Model):
#    prefix = models.ForeignKey(Prefix, blank=True, null=True) # Django 1.3 only ..., on_delete=models.SET_NULL)
#    feed = models.ForeignKey(Feed, blank=True, null=True) # Django 1.3 only ..., on_delete=models.SET_NULL)
    identifier = models.CharField(max_length=255, unique=True)
#    reload_check = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.identifier


class URL(models.Model):
    identifier = models.ForeignKey(Identifier)
    feed = models.ForeignKey(Feed)
    url = models.CharField(max_length=255)
    content_type = models.CharField(max_length=64, blank=True)
    default = models.BooleanField(default=True)
    url_check = models.BooleanField(default=False)
    last_ok = models.DateTimeField(blank=True)
    n_retries = models.IntegerField(default=0)

    def __unicode__(self):
        return self.url + ", default=" + str(self.default) + ", content-type='" + self.content_type + "'"


class Schema(models.Model):
    name = models.CharField(max_length=128)
    schema_uri = models.CharField(max_length=255, blank=True)
    namespace_uri = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name


class Metadata(models.Model):
    identifier = models.ForeignKey(Identifier)
    schema = models.ForeignKey(Schema)
    data = models.TextField()

    def __unicode__(self):
        return str(self.identifier) + ' (' + str(self.schema) + ')'
