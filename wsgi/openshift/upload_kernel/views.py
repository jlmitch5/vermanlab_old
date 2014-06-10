# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from upload_kernel.models import Document
from upload_kernel.forms import DocumentForm

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            
            # this is where the file is uploaded to the folder
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('upload_kernel.views.list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'upload_kernel/list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
