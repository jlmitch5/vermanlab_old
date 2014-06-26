from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests, json, settings

from diff_kernel.forms import KernelDiffForm

# Create your views here.
def diff(request):
    # this gets the list of the kernel versions
    if settings.ON_OPENSHIFT:
        r = requests.get('http://python-jmitchel.rhcloud.com/api/kv_list/', params=request.GET)
    else:       
        r = requests.get('http://localhost:8000/api/kv_list/', params=request.GET)
    if settings.ON_OPENSHIFT:
        api_url_root = 'http://python-jmitchel.rhcloud.com'
    else:
        api_url_root = 'http://localhost:8000'

    kvs = json.loads(r.text)
    kvs= list((e[str('name')] for e in kvs))

    #kvs: the list of the kernel versiosn
    kvs = zip(kvs, kvs)

    display_list = []
    display_list_length = 0
    
    if request.method == 'POST':
        form = KernelDiffForm(request.POST, kv_list = kvs)
        if form.is_valid():
            #k1 and k2 are the selected kernel versions (names)
            k1 = form.cleaned_data['kernel_one']
            k2 = form.cleaned_data['kernel_two']

            if settings.ON_OPENSHIFT:
                kernels_to_diff_link = 'http://python-jmitchel.rhcloud.com/api/pci_mod_list_intersection/' + k1 + '/' + k2
            else:
                kernels_to_diff_link = 'http://localhost:8000/api/pci_mod_list_intersection/' + k1 + '/' + k2

            r2 = requests.get(kernels_to_diff_link, params=request.GET)

            #mods are all the modules from the kernel diff
            mods = json.loads(r2.text)

            #this grabs the id of the kernel version
            if settings.ON_OPENSHIFT:
                kernel_id_1_link = 'http://python-jmitchel.rhcloud.com/api/kv_id/' + k1
                kernel_id_2_link = 'http://python-jmitchel.rhcloud.com/api/kv_id/' + k2
            else:
                kernel_id_1_link = 'http://localhost:8000/api/kv_id/' + k1
                kernel_id_2_link = 'http://localhost:8000/api/kv_id/' + k2

            kv1_r = requests.get(kernel_id_1_link, params=request.GET)
            kv2_r = requests.get(kernel_id_2_link, params=request.GET)
            kv1 = json.loads(kv1_r.text)
            kv2 = json.loads(kv2_r.text)
            # kv1 and kv2 are the selected kernel version IDs
            kv1 = kv1['id']
            kv2 = kv2['id']

            display_list = []

            previous_name = 'null'
            for mod in mods:
                if mod['name'] == previous_name:
                    kv_str = mod['kernelVersionModuleConnector']
                    if kv1 in kv_str:
                        display_list[-1]['kv_one_id'] = mod['id']
                    else:
                        display_list[-1]['kv_two_id'] = mod['id']
                    previous_name = mod['name']
                else:
                    display_list.append({'name': mod['name'], 'kv_one_id': 'null', 'kv_two_id': 'null'})
                    kv_str = mod['kernelVersionModuleConnector']
                    if kv1 in kv_str:
                        display_list[-1]['kv_one_id'] = mod['id']
                    else:
                        display_list[-1]['kv_two_id'] = mod['id']
                    previous_name = mod['name']

            #     if settings.ON_OPENSHIFT:
            #         mod_pretty_link = 'http://python-jmitchel.rhcloud.com/api/mod_pretty/' + str(mod['id'])
            #     else:
            #         mod_pretty_link = 'http://localhost:8000/api/mod_pretty/' + str(mod['id'])
            #     req_mod_pretty = requests.get(mod_pretty_link, params=request.GET)
            #     mod_pretty = json.loads(req_mod_pretty.text)

            display_list_length = len(display_list)

    else:
        form = KernelDiffForm(kv_list = kvs)

    return render(request, 'diff_kernel/diff.html', { 
    	'form': form,
        'display_list': display_list,
        'api_url_root': api_url_root,
        'display_list_length': display_list_length,
    })
