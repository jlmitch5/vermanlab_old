from django.contrib import admin
from upload_kernel.models import Kernel_Tarball
from upload_kernel.models import Shell_Script

admin.site.register(Kernel_Tarball)
admin.site.register(Shell_Script)
# Register your models here.
