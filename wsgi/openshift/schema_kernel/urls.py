from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from schema_kernel import views

urlpatterns = patterns('',
    url(r'^kv_list/$', views.KVList.as_view()),
    url(r'^kv_detail/(?P<name>[^/]+)/$', views.KVDetail.as_view()),
)

