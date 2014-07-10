from django.shortcuts import render

from django.db import IntegrityError

from pci_ids.models import pciam

from django.http import HttpResponse

def pci_ids(request):
    add_pci_ids_file()
    # Redirect to the document list after POST
    return HttpResponse("Here's the text of the Web page.")

def add_pci_ids_file():
    with open('/Users/apple/alias_pretty.txt', 'r') as f:
        tab_level = 0

        final_list = ""

        vendor = ""
        device = ""
        subs = ""

        vendor_pretty = ""
        device_pretty = ""
        subs_pretty = ""

        for line in f:
            if line.startswith('C '):
                break
            else:
                if line.startswith('\t\t'):
                    subs = line[2:11].replace(' ', ':')
                    subs_pretty = line[13:-1]
                    value = vendor + ":" + device + ":" + subs
                    print value
                    a, created_a = pciam.objects.get_or_create(val=value, v=vendor_pretty, d=device_pretty, s=subs_pretty)
                    a.save
                elif line.startswith ('\t'):
                    device = line[1:5]
                    device_pretty = line[7:-1]
                    value = vendor + ":" + device
                    print value
                    a, created_a = pciam.objects.get_or_create(val=value, v=vendor_pretty, d=device_pretty)
                    a.save
                else:
                    vendor = line[0:4]
                    vendor_pretty = line[6:-1]
                    device = ""
                    device_pretty = ""
                    subs = ""
                    subs_pretty = ""
                    value = vendor
                    print value
                    try:
                        a, created_a = pciam.objects.get_or_create(val=value, v=vendor_pretty)
                        a.save
                    except IntegrityError:
                        print "fine"
