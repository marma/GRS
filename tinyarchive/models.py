from django.db import models

def upload_f(instance, filename):
    return 'uploads/' + '/'.join([ instance.key[2*i:2*i+2] for i in range(0,len(instance.key)/2) ]) + '/' + filename


class Resource(models.Model):
    url = models.ForeignKey(URL)
    identifier = models.ForeignKey(Identifier)
    key = models.CharField(editable=False, max_length=40, unique=True)
    content_type = models.CharField(max_length=64, blank=True, editable=False)
    file = models.FileField(upload_to=upload_f)

    def save(self):
        if not self.key:
            self.key = hashlib.sha1(str(random.random())).hexdigest()

            super(Resource, self).save()

    def delete(self):
        path = '/'.join(str(self.file.name).split('/')[:-1])

        super(Resource, self).delete()

        # remove directories
        try:
            os.removedirs(os.path.join(MEDIA_ROOT, path))
        except:
            pass

        def __unicode__(self):
            return self.file.name
