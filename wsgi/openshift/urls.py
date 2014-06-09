from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'views.home', name='home'),
    # url(r'^openshift/', include('foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # Upload stuff
    (r'^upload/', include('upload_kernel.urls')),
    (r'^$', RedirectView.as_view(url='/upload/list/')), # Just for ease of use.
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
