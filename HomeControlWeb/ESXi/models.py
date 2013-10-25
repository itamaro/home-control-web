import logging
from collections import defaultdict

from django.db import models

from common import load_json_from_url

logger = logging.getLogger(__name__)

class EsxiHost(models.Model):
    POWER_ON = 'ON'
    POWER_OFF = 'OFF'
    POWER_UNKNOWN = 'TBD'
    POWER_STATES = (
        (POWER_ON, 'On'),
        (POWER_OFF, 'Off'),
        (POWER_UNKNOWN, 'Unknown'),
    )
    name = models.CharField(max_length=100, unique=True)
    ip_addr = models.IPAddressField(verbose_name='IP Address')
    ssh_port = models.PositiveIntegerField(verbose_name='SSH Port')
    root_user = models.CharField(max_length=100, default='root')
    root_pass = models.CharField(max_length=100)
    power_state = models.CharField(max_length=3, choices=POWER_STATES)
    updated = models.DateTimeField(auto_now=True)
    rpc_url = models.URLField()
    
    def __unicode__(self):
        return self.name
    
    def is_cached_power_on(self):
        "Return True if host is On, based on local cache"
        return self.POWER_ON == self.power_state
    
    def update_power_remote(self):
        "Retrieve power state from remote ESXi host and update local DB"
        res = load_json_from_url(self.rpc_url, 'check-power', self.name)
        self.power_state = res[self.name] == 'ON' and   \
                           self.POWER_ON or self.POWER_OFF
        self.save()
    
    def turn_on(self):
        if self.is_cached_power_on():
            logger.warning('Received Turn On command while host is ON')
            return
        res = load_json_from_url(self.rpc_url, 'turn-on', self.name)
        self.power_state = res[self.name] == 'ON' and   \
                           self.POWER_ON or self.POWER_OFF
        self.save()
        # TODO: Turn on VMs?
    
    def shutdown(self):
        "Send remote shutdown command and update local DB"
        if not self.is_cached_power_on():
            logger.warning('Received Shutdown command while host is OFF')
            return
        # Shutdown related virtual machines
        for vm in self.virtualmachine_set.all():
            # TODO: Shutdown order??
            if vm.is_cached_power_on():
                logger.info('Shutting down VM "%s"' % (vm.name))
                #TODO: Uncomment
                vm.shutdown()
            else:
                logger.debug('VM "%s" already off' % (vm.name))
        # Send shutdown RPC command
        res = load_json_from_url(self.rpc_url, 'shutdown', self.name)
        self.power_state = res[self.name] == 'ON' and   \
                           self.POWER_ON or self.POWER_OFF
        self.save()
    
    def update_from_rpc(self):
        "Retrieve list of VMs from remote ESXi host and update local DB"
        # First check host power state
        self.update_power_remote()
        if self.is_cached_power_on():
            # Host on, so check VMs
            res = load_json_from_url(self.rpc_url, 'list-vms', self.name)
            summary = defaultdict(set)
            summary['missing'] = [vm.vmid
                                  for vm in self.virtualmachine_set.all()]
            for vm_dict in res[self.name]:
                vm_dict['vmid'] = int(vm_dict['vmid'])
                vm, created = VirtualMachine.objects.get_or_create(
                                vmid=vm_dict.get('vmid'), esxi_host=self,
                                defaults=vm_dict)
                if created:
                    logger.debug('Added new VM: %s' % (vm.name))
                    summary['created'].add(vm.vmid)
                else:
                    summary['exists'].add(vm.vmid)
                    summary['missing'].remove(vm.vmid)
                vm.update_from_rpc()
            for vmid in summary['missing']:
                vm = self.virtualmachine_set.get(vmid=vmid)
                logger.debug('Removed VM: %s' % (vm))
                vm.delete()
        else:
            # Host off, so all VMs are naturally off
            for vm in self.virtualmachine_set.all():
                vm.power_state = vm.POWER_OFF
                vm.save()

class VirtualMachine(models.Model):
    POWER_ON = 'ON'
    POWER_OFF = 'OFF'
    POWER_SUSPEND = 'SUS'
    POWER_UNKNOWN = 'TBD'
    POWER_STATES = (
        (POWER_ON, 'On'),
        (POWER_OFF, 'Off'),
        (POWER_SUSPEND, 'Suspended'),
        (POWER_UNKNOWN, 'Unknown'),
    )
    esxi_host = models.ForeignKey(EsxiHost)
    vmid = models.IntegerField(verbose_name='VM ID')
    name = models.CharField(max_length=100, verbose_name='VM name')
    vmfile = models.CharField(max_length=256, verbose_name='VM file')
    guest_os = models.CharField(max_length=50, verbose_name='VM Guest OS')
    version = models.CharField(max_length=10, verbose_name='VM version')
    power_state = models.CharField(max_length=3, choices=POWER_STATES,
                                   default=POWER_UNKNOWN)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return '%s::%s' % (self.esxi_host.name, self.name)
    
    def is_cached_power_on(self):
        return self.POWER_ON == self.power_state
        
    def update_power_remote(self):
        "Retrieve VM power state from remote ESXi host and update local DB"
        res = load_json_from_url(self.esxi_host.rpc_url, 'check-power',
                                 self.esxi_host.name, str(self.vmid))
        self.power_state = res[str(self.vmid)] == 'ON' and   \
                           self.POWER_ON or self.POWER_OFF
        self.save()
    
    def update_from_rpc(self):
        self.update_power_remote()
    
    def turn_on(self):
        if self.is_cached_power_on():
            logger.warning('Received Turn On command while VM is ON')
            return
        res = load_json_from_url(self.esxi_host.rpc_url, 'turn-on',
                                 self.esxi_host.name, str(self.vmid))
        self.power_state = res[str(self.vmid)] == 'ON' and   \
                           self.POWER_ON or self.POWER_OFF
        self.save()
    
    def shutdown(self):
        if not self.is_cached_power_on():
            logger.warning('Received Shutdown command while VM is OFF')
            return
        res = load_json_from_url(self.esxi_host.rpc_url, 'shutdown',
                                 self.esxi_host.name, str(self.vmid))
        self.power_state = res[str(self.vmid)] == 'ON' and   \
                           self.POWER_ON or self.POWER_OFF
        self.save()
