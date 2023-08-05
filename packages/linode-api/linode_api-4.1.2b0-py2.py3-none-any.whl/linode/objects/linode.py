from .base import Base, Property
from .disk import Disk
from .config import Config
from .backup import Backup
from .service import Service
from .datacenter import Datacenter
from .distribution import Distribution
from .ipaddress import IPAddress

from random import choice

class Linode(Base):
    api_name = 'linodes'
    api_endpoint = '/linodes/{id}'
    properties = {
        'id': Property(identifier=True),
        'label': Property(mutable=True, filterable=True),
        'group': Property(mutable=True, filterable=True),
        'state': Property(volatile=True),
        'created': Property(is_datetime=True),
        'updated': Property(volatile=True, is_datetime=True),
        'total_transfer': Property(),
        'ips': Property(),
        'distribution': Property(),
        'datacenter': Property(relationship=Datacenter, filterable=True),
        'alerts': Property(),
        'distribution': Property(relationship=Distribution, filterable=True),
        'disks': Property(derived_class=Disk),
        'configs': Property(derived_class=Config),
        'services': Property(relationship=Service),
        'backups': Property(),
        'recent_backups': Property(derived_class=Backup),
        'ips_collection': Property(derived_class=IPAddress),
    }

    def boot(self, config=None):
        resp = self._client.post("{}/boot".format(Linode.api_endpoint), model=self, data={'config': config.id} if config else None)

        if 'error' in resp:
            return False
        return True

    def shutdown(self):
        resp = self._client.post("{}/shutdown".format(Linode.api_endpoint), model=self)

        if 'error' in resp:
            return False
        return True

    def reboot(self):
        resp = self._client.post("{}/reboot".format(Linode.api_endpoint), model=self)

        if 'error' in resp:
            return False
        return True

    @staticmethod
    def generate_root_password():
        return ''.join([choice('abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*_+-=') for _ in range(0, 32) ])

    # create derived objects
    def create_config(self, kernel, label=None, disks=None, **kwargs):

        disk_list = []
        if disks:
            disk_list = [ d.id for d in disks ]

        params = {
            'kernel': kernel.id if issubclass(type(kernel), Base) else kernel,
            'label': label if label else "{}_config_{}".format(self.label, len(self.configs)),
            'disks': disk_list,
        }
        params.update(kwargs)

        result = self._client.post("{}/configs".format(Linode.api_endpoint), model=self, data=params)
        self.invalidate()

        if not 'id' in result:
            return result

        c = Config(self._client, result['id'], self.id)
        c._populate(result)
        return c

    def create_disk(self, size, label=None, filesystem=None, read_only=False, distribution=None, \
            root_pass=None, root_ssh_key=None, stackscript=None, **stackscript_args):

        gen_pass = None
        if distribution and not root_pass:
            gen_pass  = Linode.generate_root_password()
            root_pass = gen_pass

        if root_ssh_key:
            accepted_types = ('ssh-dss', 'ssh-rsa', 'ecdsa-sha2-nistp', 'ssh-ed25519')
            if not any([ t for t in accepted_types if root_ssh_key.startswith(t) ]):
                # it doesn't appear to be a key.. is it a path to the key?
                import os
                root_ssh_key = os.path.expanduser(root_ssh_key)
                if os.path.isfile(root_ssh_key):
                    with open(root_ssh_key) as f:
                        root_ssh_key = "".join([ l.strip() for l in f ])
                else:
                    raise ValueError("root_ssh_key must either be a path to the key file or a "
                                    "raw public key of one of these types: {}".format(accepted_types))

        if distribution and not label:
            label = "My {} Disk".format(distribution.label)

        params = {
            'size': size,
            'label': label if label else "{}_disk_{}".format(self.label, len(self.disks)),
            'read_only': read_only,
            'filesystem': filesystem if filesystem else 'raw',
        }

        if distribution:
            params.update({
                'distribution': distribution.id if issubclass(type(distribution), Base) else distribution,
                'root_pass': root_pass,
            })

        if stackscript:
            params['stackscript'] = stackscript.id
            if stackscript_args:
                params['stackscript_data'] = stackscript_args

        result = self._client.post("{}/disks".format(Linode.api_endpoint), model=self, data=params)
        self.invalidate()

        if not 'id' in result:
            return result

        d = Disk(self._client, result['id'], self.id)
        d._populate(result)

        if gen_pass:
            return d, gen_pass
        return d

    def enable_backups(self):
        result = self._client.post("{}/backups/enable".format(Linode.api_endpoint), model=self)
        self._populate(result)
        return True

    def cancel_backups(self):
        result = self._client.post("{}/backups/cancel".format(Linode.api_endpoint), model=self)
        self._populate(result)
        return True

    def snapshot(self, label=None):
        result = self._client.post("{}/backups".format(Linode.api_endpoint), model=self,
            data={ "label": label })

        if not 'id' in result:
            return result

        b = Backup(self._client, result['id'], self.id)
        b._populate(result)
        return b

    def allocate_ip(self, public=False):
        result = self._client.post("{}/ips".format(Linode.api_endpoint), model=self,
                data={ "type": "public" if public else "private" })

        if not 'id' in result:
            return result

        i = IPAddress(self._client, result['id'], self.id)
        i._populate(result)
        return i
