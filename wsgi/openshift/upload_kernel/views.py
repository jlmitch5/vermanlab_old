# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from upload_kernel.models import Kernel_Tarball
from upload_kernel.models import Shell_Script
from upload_kernel.forms import KernelTarballForm
import os, gzip, settings, pdb

def list(request):

    # Load documents for the list page
    kernel_tarballs = Kernel_Tarball.objects.all()
    shell_scripts = Shell_Script.objects.all()

    # Handle file upload
    if request.method == 'POST':
        form = KernelTarballForm(request.POST, request.FILES)
        if form.is_valid():
            new_kernel_tarball = Kernel_Tarball(docfile = request.FILES['docfile'], decompressed_folder = request.FILES['docfile'])
            # TODO: Fix don't add a duplicate file
            # if not Kernel_Tarball.objects.filter(name=new_kernel_tarball.name):
            #     new_kernel_tarball.save()
            new_kernel_tarball.save()
            
            #unzip the file
            unzip_file(new_kernel_tarball)

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('upload_kernel.views.list'))
    else:
        form = KernelTarballForm() # A empty, unbound form

    # Render list page with the documents and the form
    return render_to_response(
        'upload_kernel/list.html',
        {'shell_scripts': shell_scripts, 'kernel_tarballs': kernel_tarballs, 'form': form},
        context_instance=RequestContext(request)
    )

def unzip_file(kernel_object):
    added_folder_path = os.path.join(settings.MEDIA_ROOT, 'added/')
    file_path = os.path.join(settings.MEDIA_ROOT, kernel_object.decompressed_folder.name)
    print "%s" % file_path
    # TODO: on OSX, this was adding to the code base dir, not the static dir: (SEE ISSUE 5)
    os.system('tar xvf ' + file_path + ' -C ' + added_folder_path)
    os.system('rm -f ' + file_path)
