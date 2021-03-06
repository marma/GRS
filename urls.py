from django.conf.urls.defaults import *
from settings import STATIC_DOC_ROOT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^GRS/', include('GRS.foo.urls')),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': STATIC_DOC_ROOT }),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
