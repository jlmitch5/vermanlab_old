from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from rest_framework import viewsets, routers
from schema_kernel.models import KernelVersion, PCIModule, PCIAliases
import django_filters

admin.autodiscover()

class KernelVersionFilter(django_filters.FilterSet):
    print "filter"
    name = django_filters.CharFilter(name="name",lookup_type="icontains")

# ViewSets define the view behavior.
class KernelVersionViewSet(viewsets.ModelViewSet):
    model = KernelVersion
    filter_class = KernelVersionFilter
    filter_backends = (DjangoFilterBackend,)

class PCIModuleViewSet(viewsets.ModelViewSet):
    model = PCIModule

class PCIAliasesViewSet(viewsets.ModelViewSet):
    model = PCIAliases


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'kernelversion', KernelVersionViewSet)
router.register(r'pcimodule', PCIModuleViewSet)
router.register(r'pcialiases', PCIAliasesViewSet)
router.register(r'kernelversion/(?P<name>\d+)', KernelVersionViewSet)

urlpatterns = patterns('',
    url(r'^$', 'views.home', name='home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # Upload stuff
    (r'^upload/', include('upload_kernel.urls')),
    (r'^$', RedirectView.as_view(url='/upload/list/')), # Just for ease of use.
    url(r'^api/', include(router.urls)),
    (r'^api/', include('rest_framework.urls', namespace='rest_framework')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
