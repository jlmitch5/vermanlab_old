from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests, json, settings

from diff_kernel.forms import KernelDiffForm

# Create your views here.
def diff(request):
    if settings.ON_OPENSHIFT:
        r = requests.get('http://python-jmitchel.rhcloud.com/api/kv_list/', params=request.GET)
    else:       
        r = requests.get('http://localhost:8000/api/kv_list/', params=request.GET)
    kvs = json.loads(r.text)
    kvs= list((e[str('name')] for e in kvs))
    kvs = zip(kvs, kvs)
    kv1_mods_list = []
    kv2_mods_list = []
    list_names = []
    
    if request.method == 'POST':
        form = KernelDiffForm(request.POST, kv_list = kvs)
        if form.is_valid():
            # process the form data
            k1 = form.cleaned_data['kernel_one']
            k2 = form.cleaned_data['kernel_two']

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
            kv1 = kv1['id']
            kv2 = kv2['id']

            if settings.ON_OPENSHIFT:
                kernels_to_diff_link = 'http://python-jmitchel.rhcloud.com/api/pci_mod_list_intersection/' + k1 + '/' + k2
            else:
                kernels_to_diff_link = 'http://localhost:8000/api/pci_mod_list_intersection/' + k1 + '/' + k2

            r2 = requests.get(kernels_to_diff_link, params=request.GET)

            mods = json.loads(r2.text)
            kv1_mods_list = []
            kv2_mods_list = []
            list_names = []

            for mod in mods:
                if settings.ON_OPENSHIFT:
                    mod_pretty_link = 'http://python-jmitchel.rhcloud.com/api/mod_pretty/' + str(mod['id'])
                else:
                    mod_pretty_link = 'http://localhost:8000/api/mod_pretty/' + str(mod['id'])
                req_mod_pretty = requests.get(mod_pretty_link, params=request.GET)
                mod_pretty = json.loads(req_mod_pretty.text)

                kv_str = mod['kernelVersionModuleConnector']
                if kv1 in kv_str:
                    kv1_mods_list.append(mod_pretty)
                else:
                    kv2_mods_list.append(mod_pretty)



            names = set(i['name'] for i in kv1_mods_list+kv2_mods_list)
            list_names = list(names)
            list_names.sort()
            print list_names


    else:
        form = KernelDiffForm(kv_list = kvs)

    return render(request, 'diff_kernel/diff.html', { 
    	'form': form,
        'kv1_mods_list': kv1_mods_list,
        'kv2_mods_list': kv2_mods_list,
        'list_names': list_names,
    })
