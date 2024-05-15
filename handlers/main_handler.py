from handlers.enpoint_handler import EndpointHandler
from handlers.service_handler import ServiceHandler

endpoint_handler = EndpointHandler()
service_handler = ServiceHandler()

class MainHandler:
    def __init__(self) -> None:
        pass

    def check_endpoint(self, schema_name, filters):
        endpoint = endpoint_handler.get_endpont(schema_name=schema_name, filters=filters)
        if len(endpoint) > 0:
            endpoint = endpoint[0]
            return endpoint.as_dict()
        return []