from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns

from schema_kernel import views

urlpatterns = patterns('',
	url(r'^get_kernel_versions/$', views.GetKernelVersions.as_view()),
    url(r'^diff/(?P<name1>[^/]+)/(?P<name2>[^/]+)/$', views.Diff.as_view()),
)

