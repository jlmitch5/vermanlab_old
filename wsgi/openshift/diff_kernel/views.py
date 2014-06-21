from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests, json

from diff_kernel.forms import KernelDiffForm

# Create your views here.
def diff(request):
    r = requests.get('http://localhost:8000/api/kv_list/', params=request.GET)
    kvs = json.loads(r.text)
    
    if request.method == 'POST':
        form = KernelDiffForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('diff_kernel.views.list')
    else:
        form = KernelDiffForm(kv_list = kvs)

    return render(request, 'diff_kernel/diff.html', { 
    	'form': form,
    })
