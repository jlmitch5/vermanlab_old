from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from schema_kernel.models import KernelVersion, PCIModule, PCIAliases
from schema_kernel.api import KernelVersionResource, PCIModuleResource, PCIAliasesResource

kv_resource = KernelVersionResource()
pci_mod_resource = PCIModuleResource()
pci_aliases_resource = PCIAliasesResource()

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^upload/', include('upload_kernel.urls')),
    url(r'^diff/', include('diff_kernel.urls')),
    url(r'^api/', include('schema_kernel.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
