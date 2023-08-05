from .. import DerivedBase, Property
from ..base import MappedObject
from .kernel import Kernel
from .disk import Disk
from ... import mappings as mapper

class Config(DerivedBase):
    api_name="configs"
    api_endpoint="/linode/instances/{linode_id}/configs/{id}"
    derived_url_path="configs"
    parent_id_name="linode_id"

    properties = {
        "id": Property(identifier=True),
        "linode_id": Property(identifier=True),
        "helpers": Property(),#TODO: mutable=True),
        "created": Property(is_datetime=True),
        "root_device": Property(mutable=True),
        "kernel": Property(relationship=Kernel, mutable=True, filterable=True),
        "devices": Property(filterable=True),#TODO: mutable=True),
        "initrd": Property(relationship=Disk),
        "updated": Property(),
        "comments": Property(mutable=True, filterable=True),
        "label": Property(mutable=True, filterable=True),
        "devtmpfs_automount": Property(mutable=True, filterable=True),
        "root_device_ro": Property(mutable=True, filterable=True),
        "run_level": Property(mutable=True, filterable=True),
        "virt_mode": Property(mutable=True, filterable=True),
        "ram_limit": Property(mutable=True, filterable=True),
    }

    def _populate(self, json):
        """
        Map devices more nicely while populating.
        """
        from .volume import Volume

        DerivedBase._populate(self, json)

        devices = {}
        for device_index, device in json['devices'].items():
            if not device:
                devices[device_index] = None
                continue

            dev = None
            if 'disk_id' in device and device['disk_id']: # this is a disk
                dev = mapper.make(device['disk_id'], self._client, parent_id=self.linode_id, cls=Disk)
            else:
                dev = mapper.make(device['volume_id'], self._client, parent_id=self.linode_id, cls=Volume)
            devices[device_index] = dev

        self._set('devices', MappedObject(**devices))
