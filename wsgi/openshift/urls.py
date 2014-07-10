from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'views.home', name='home'),
    url(r'^api/', include('schema_kernel.urls')),
    url(r'^upload/', include('upload_kernel.urls')),
    url(r'^diff/', include('diff_kernel.urls')),
    url(r'^pci_ids/', include('pci_ids.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
