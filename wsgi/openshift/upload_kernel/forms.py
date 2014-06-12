# -*- coding: utf-8 -*-
from django import forms

class KernelTarballForm(forms.Form):
    docfile = forms.FileField(
        label='Upload the .tar.gz file the script you ran created:'
    )
