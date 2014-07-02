import requests, json, settings

from django.http import HttpResponseRedirect
from django.shortcuts import render

from diff_kernel.forms import KernelDiffForm

# Create your views here.
def diff(request):
    # this sets the correct url root for making api requests
    if settings.ON_OPENSHIFT:
        api_url_root = 'http://python-jmitchel.rhcloud.com'
    else:
        api_url_root = 'http://localhost:8000'

    # this gets all the possible kernel versions so that the user can select from the form
    get_kernel_versions_url = api_url_root + '/api/get_kernel_versions'
    kvs = json.loads(requests.get(get_kernel_versions_url, params=request.GET).text)
    kvs = list((e[str('name')] for e in kvs))
    kvs = zip(kvs, kvs)

    # this will hold all the kernel diff data
    kernel_diff_info = []

    # render the form (and kernel_diff_data if the user has selected the kernel versions)    
    if request.method == 'POST':
        form = KernelDiffForm(request.POST, kv_list = kvs)
        if form.is_valid():
            #k1 and k2 are the selected kernel versions (names)
            k1 = form.cleaned_data['kernel_one']
            k2 = form.cleaned_data['kernel_two']

            diff_url = api_url_root + '/api/diff/' + k1 + '/' + k2

            diff_data = requests.get(diff_url, params=request.GET)

            #mods are all the modules from the kernel diff
            kernel_diff_info = json.loads(diff_data.text)
    else:
        form = KernelDiffForm(kv_list = kvs)

    return render(request, 'diff_kernel/diff.html', { 
    	'form': form,
        'kernel_diff_info': kernel_diff_info
    })
