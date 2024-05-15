from models.Endpoint import endpoint_model

class EndpointHandler:
    def __init__(self) -> None:
        pass

    def create_endpoint(self, schema_name):
        endpoint_model(schema_name=schema_name)

    def get_endponts(self, service_name, schema_name):
        output = []
        try:
            endpoint = endpoint_model(schema_name)
            endpoints = endpoint.query.all()
            for endpoint in endpoints:
                endpoint_data = {
                    'endpoint_id': endpoint.endpoint_id,
                    'url': endpoint.url,
                    'http_method': endpoint.http_method,
                    'request_format': endpoint.request_format,
                    'response_format': endpoint.response_format,
                    'parameters': endpoint.parameters,
                    'example_request_payload': endpoint.example_request_payload,
                    'example_response_payload': endpoint.example_response_payload
                }
                output.append(endpoint_data)
        except Exception as e:
            print(f"error in endpoints  {str(e)}")
        return output
    
    def add_endpoint(self, data, schema_name):
        endpoint = endpoint_model(schema_name)
        return endpoint.insert(data=data)
    
    def get_endpont(self, schema_name, filters):
        print(filters)
        endpont = endpoint_model(schema_name)
        return endpont.dynamic_query(filters=filters)