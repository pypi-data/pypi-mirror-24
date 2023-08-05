from .base import Base, Property

class Distribution(Base):
    api_name = 'distributions'
    api_endpoint = '/distributions/{id}'
    properties = {
        'id': Property(identifier=True),
        'label': Property(filterable=True),
        'minimum_storage_size': Property(filterable=True),
        'recommended': Property(filterable=True),
        'vendor': Property(filterable=True),
        'created': Property(is_datetime=True),
        'x64': Property(),
    }
