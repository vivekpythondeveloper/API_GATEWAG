from models.service import service_model
from urllib.parse import urlparse

class ServiceHandler:
    def __init__(self) -> None:
        pass

    def create_service(self, schema_name):
        service_model(schema_name=schema_name)

    def add_service(self, data, schema_name):
        new_service = None
        try:
            parsed_url = urlparse(data.get('url'))
            service = service_model(schema_name)
            new_service = service.insert(name=data.get('name'),
                           protocol=parsed_url.scheme,
                           host =parsed_url.hostname,
                           port =parsed_url.port,
                           path =parsed_url.path)
            
            
        except Exception as e:
            print(f"error in endpoints  {str(e)}")
        return new_service
    
    def get_service(self, schema_name, filters):
        service = service_model(schema_name)
        return service.dynamic_query(filters=filters)