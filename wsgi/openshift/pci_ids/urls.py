# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('pci_ids.views',
    url(r'^$', 'pci_ids', name='pci_ids'),
)