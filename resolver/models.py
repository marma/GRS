from django.db import models
from tinyarchive.models import Resource

class Prefix(models.Model):
    prefix = models.CharField(max_length=255, unique=True)
    redirect_url = models.CharField(max_length=255, blank=True)
    redirect_on_miss = models.BooleanField(default=False)
    mint = models.BooleanField(default=False)
    next_id = models.IntegerField(default=0)

    def __unicode__(self):
        return self.prefix


FEED_CHOICES = (
        ('OAIPMH', 'OAI-PMH'),
        ('AFEED', 'Atom Feed')
    )

class Feed(models.Model):
    prefix = models.ForeignKey(Prefix)
    type = models.CharField(max_length=32, choices=FEED_CHOICES)
    refresh_rate = models.IntegerField(default=10*60)
    base_url = models.CharField(max_length=255)
    archive_objects = models.BooleanField(default=False)
    default = models.BooleanField(default=True)
    xslt_transform = models.TextField(blank=True)

    def __unicode__(self):
        return "prefix=" + self.prefix.prefix + "', type=" + self.type + ", base_url=" + self.base_url + ", archive_objects=" + str(self.archive_objects)


class Identifier(models.Model):
    prefix = models.ForeignKey(Prefix, blank=True, null=True) # Django 1.3 only ..., on_delete=models.SET_NULL)
    feed = models.ForeignKey(Feed, blank=True, null=True) # Django 1.3 only ..., on_delete=models.SET_NULL)
    identifier = models.CharField(max_length=255, unique=True)
    reload_check = models.BooleanField(default=False)
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


class Namespace(models.Model):
    name = models.CharField(max_length=128)
    uri = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Schema(models.Model):
    name = models.CharField(max_length=128)
    uri = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Metadata(models.Model):
    identifier = models.ForeignKey(Identifier)
    schema = models.ForeignKey(Schema)
    data = models.TextField()

