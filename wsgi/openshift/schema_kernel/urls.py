from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from schema_kernel import views

urlpatterns = patterns('',
    url(r'^kv_list/$', views.KVList.as_view()),
    url(r'^kv_detail/(?P<name>[^/]+)/$', views.KVDetail.as_view()),
    url(r'^pci_mod_list/$', views.PCIMList.as_view()),
    url(r'^pci_mod_list_by_kv/(?P<name>[^/]+)/$', views.PCIMList_by_kv.as_view()),
    url(r'^pci_mod_list_intersection/(?P<name1>[^/]+)/(?P<name2>[^/]+)/$', views.PCIMList_intersection.as_view()),
    url(r'^mod_id/(?P<name>[^/]+)/(?P<version>[^/]+)/(?P<srcversion>[^/]+)$', views.ModID.as_view()),
    url(r'^kv_id/(?P<name>[^/]+)/$', views.KVID.as_view()),
    url(r'^mod_pretty/(?P<id>[^/]+)/$', views.ModPretty.as_view()),
)

