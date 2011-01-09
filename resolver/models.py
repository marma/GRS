from django.db import models

class Prefix(models.Model):
    prefix = models.CharField(max_length=255, unique=True)
    redirect_url = models.CharField(max_length=255, blank=True)
    redirect_on_miss = models.BooleanField(default=False)

    def __unicode__(self):
        return self.prefix


FEED_CHOICES = (
        ('OAIPMH', 'OAI-PMH'),
        ('AFEED', 'Atom Feed')
    )

class Feed(models.Model):
    prefix = models.ForeignKey(Prefix)
    type = models.CharField(max_length=32, choices=FEED_CHOICES)
    base_url = models.CharField(max_length=255)
    archive_objects = models.BooleanField(default=False)
    xslt_transform = models.TextField(blank=True)

    def __unicode__(self):
        return "prefix=" + self.prefix.prefix + "', type=" + self.type + ", base_url=" + self.base_url + ", archive_objects=" + str(self.archive_objects)


class Identifier(models.Model):
    prefix = models.ForeignKey(Prefix)
    feed = models.ForeignKey(Feed)
    identifier = models.CharField(max_length=255, unique=True)
    
    def __unicode__(self):
        return self.identifier


class URL(models.Model):
    identifier = models.ForeignKey(Identifier)
    url = models.CharField(max_length=255)
    content_type = models.CharField(max_length=64, blank=True)
    default = models.BooleanField(default=True)

    def __unicode__(self):
        return self.url + ", default=" + str(self.default) + ", content-type='" + self.content_type + "'"


class Metadata(models.Model):
    identifier = models.ForeignKey(Identifier)
    schema = models.CharField(max_length=32)
    data = models.TextField()
