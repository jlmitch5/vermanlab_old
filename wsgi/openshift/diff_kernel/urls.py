# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('diff_kernel.views',
	url(r'^$', 'diff', name='diff'),
)
