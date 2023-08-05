from .. import Base, Property

class Distribution(Base):
    api_name = 'distributions'
    api_endpoint = '/linode/distributions/{id}'
    properties = {
        'id': Property(identifier=True),
        'label': Property(filterable=True),
        'minimum_storage_size': Property(filterable=True),
        'deprecated': Property(filterable=True),
        'vendor': Property(filterable=True),
        'created': Property(is_datetime=True),
        'x64': Property(),
    }
