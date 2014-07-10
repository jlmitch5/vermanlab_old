# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from upload_kernel.models import Kernel_Tarball
from upload_kernel.models import Shell_Script
from upload_kernel.forms import KernelTarballForm
import os, gzip, settings, pdb, subprocess
from schema_kernel.models import KernelVersion, PCIModule, PCIAliases

def upload(request):

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
            return HttpResponseRedirect(reverse('upload_kernel.views.upload'))
    else:
        form = KernelTarballForm() # A empty, unbound form

    # Render list page with the documents and the form
    return render_to_response(
        'upload_kernel/upload.html',
        {'shell_scripts': shell_scripts, 'kernel_tarballs': kernel_tarballs, 'form': form},
        context_instance=RequestContext(request)
    )

def unzip_file(kernel_object):
    added_folder_path = os.path.join(settings.MEDIA_ROOT, 'added/')
    file_path = os.path.join(settings.MEDIA_ROOT, kernel_object.decompressed_folder.name)
    
    
    os.system('tar xf ' + file_path + ' -C ' + added_folder_path)
    os.system('rm -f ' + file_path)

    # start processing file
    machine_name = file_path[:-7]
    output = subprocess.check_output(['ls', '%s' % (machine_name)])
    kernel_list =  (output).splitlines()

    #FOR EACH KERNEL
    for kernel_path in kernel_list:
        # TODO: add support for more than just the pci modules
        kernel_name = kernel_path
        #UPLOAD TO KERNELVERSION DB
        kv, created_kv = KernelVersion.objects.get_or_create(name=kernel_name)
        kv.save
        kernel_path = machine_name + '/' + kernel_path + '/__pci_modules__'
        
        output = subprocess.check_output(['ls', '%s' % (kernel_path)])
        module_list = (output).splitlines()

        #FOR EACH MODULE IN THAT KERNEL VERSION
        for module_path in module_list:
            module_name = module_path
            module_path = kernel_path + '/' + module_path
            
            version_path = module_path + '/version'
            srcversion_path = module_path + '/srcversion'
            alias_path = module_path + '/aliases'

            version_name = 'NULL'
            srcversion_name = 'NULL'
            try:
                version_name = subprocess.check_output(['cat', '%s' % (version_path)])
            except subprocess.CalledProcessError:
                pass
            try:
                srcversion_name = subprocess.check_output(['cat', '%s' % (srcversion_path)])
            except subprocess.CalledProcessError:
                pass
            m, created_m = PCIModule.objects.get_or_create(name=module_name, version=version_name, srcversion=srcversion_name)
            m.kernelVersionModuleConnector.add(kv)
            m.save

            output = subprocess.check_output( ['cat', '%s' % (alias_path)] )
            
            alias_list = (output.splitlines())
            for inst_alias in alias_list:
                alias_component = (inst_alias).rstrip('\\n').split(':')
                vendor = 'null'
                device = 'null'
                subvendor = 'null'
                subdevice = 'null'
                try:
                    if alias_component[0]:
                        vendor = alias_component[0]
                except:
                    pass
                try:
                    if alias_component[1]:
                        device = alias_component[1]
                except:
                    pass
                try:
                    if alias_component[2]:
                        subvendor = alias_component[2]
                except:
                    pass
                try:
                    if alias_component[3]:
                        subdevice = alias_component[3]
                except:
                    pass

                a, created_a = PCIAliases.objects.get_or_create(vendor=vendor, device=device, subvendor=subvendor, subdevice=subdevice)
                a.module.add(m)
                a.save
