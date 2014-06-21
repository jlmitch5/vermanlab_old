from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests, json

from diff_kernel.forms import KernelDiffForm

# Create your views here.
def diff(request):
    r = requests.get('http://localhost:8000/api/kv_list/', params=request.GET)
    kvs = json.loads(r.text)
    kvs= list((e[str('name')] for e in kvs))
    kvs = zip(kvs, kvs)
    
    if request.method == 'POST':
        form = KernelDiffForm(request.POST, kv_list = kvs)
        if form.is_valid():
            # process the form data
            k1 = form.cleaned_data['kernel_one']
            k2 = form.cleaned_data['kernel_two']
            kernels_to_diff_link = 'http://jmitchelnode.usersys.redhat.com:8000/api/pci_mod_list_intersection/' + k1 + '/' + k2
            r2 = requests.get(kernels_to_diff_link, params=request.GET)
            mods = json.loads(r2.text)
            print mods

    else:
        form = KernelDiffForm(kv_list = kvs)

    return render(request, 'diff_kernel/diff.html', { 
    	'form': form,
    })
