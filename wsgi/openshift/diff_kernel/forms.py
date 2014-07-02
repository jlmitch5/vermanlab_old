# -*- coding: utf-8 -*-
from django import forms

class KernelDiffForm(forms.Form):

    def __init__(self,*args,**kwargs):
        kernel_list = kwargs.pop('kv_list')
        kernel_tuples = zip(kernel_list, kernel_list)
        super(KernelDiffForm, self).__init__(*args,**kwargs)
        self.fields['kernel_one'] = forms.ChoiceField(label="kernel_one", choices=kernel_list)
        self.fields['kernel_two'] = forms.ChoiceField(label="kernel_two", choices=kernel_list)
