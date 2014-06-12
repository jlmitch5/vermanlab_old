# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from upload_kernel.models import Kernel_Tarball
from upload_kernel.models import Shell_Scripts
from upload_kernel.forms import KernelTarballForm

def list(request):

    # Load documents for the list page
    kernel_tarballs = Kernel_Tarball.objects.all()
    shell_scripts = Sell_Scripts.objects.all()

    # Handle file upload
    if request.method == 'POST':
        form = KernelTarballForm(request.POST, request.FILES)
        if form.is_valid():
            new_kernel_tarball = Kernel_Tarball(docfile = request.FILES['docfile'])

            # Don't add a duplicate file
            if not Kernel_Tarball.objects.filter(name=new_kernel_tarball.name):
                new_kernel_tarball.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('upload_kernel.views.list'))
    else:
        form = KernelTarballForm() # A empty, unbound form

    # Render list page with the documents and the form
    return render_to_response(
        'upload_kernel/list.html',
        {'shell_scripts': shell_scripts, 'kernel_tarballs': kernell_tarballs, 'form': form},
        context_instance=RequestContext(request)
    )
