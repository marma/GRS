from django.db import models

def get_key():
    return hashlib.sha1(str(random.random())).hexdigest()

def upload_f(instance, filename):
    if not instance.key:
        instance.key = get_key()

    return 'archive/' + '/'.join([ instance.key[2*i:2*i+2] for i in range(0,4) ]) + '/' + instance.key[8:] + '/' + filename

class Resource(models.Model):
    key = models.CharField(editable=False, max_length=40, unique=True)
    content_type = models.CharField(max_length=64, blank=True, editable=False)
    file = models.FileField(upload_to=upload_f)

    def save(self):
        if not self.key:
            self.key = get_key()

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

