from django.contrib import admin
import ESXi
#from ESXi.models import Poll

class VmInline(admin.StackedInline):
    model = ESXi.models.VirtualMachine
    extra = 1

class EsxiHostAdmin(admin.ModelAdmin):
    inlines = [VmInline]

admin.site.register(ESXi.models.EsxiHost, EsxiHostAdmin)
