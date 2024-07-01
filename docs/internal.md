# Internal API

EZAuth provides an internal API for other services to interact with the service. This API is not meant to be exposed to the public and should only be used by services that are running on the same network as the EZAuth service.

!!! danger "Internal API Key"
    Even though it is recommended to hide the `/internal` endpoints from the public with a middleware, you should still keep the `internal_api_key` secret. If someone gets access to this key, they can access all the internal API endpoints.

## Access the Internal API

To access any endpoints prefixed with `/internal` you need to set the `internal_api_key` header.

Example in Python:

```python
import requests

url = "http://localhost:3250/internal/<whatever_endpoint>"
headers = {
    "internal_api_key": "YOUR_INTERNAL_API_KEY"
}

response = requests.get(url, headers=headers)
print(response.json())
```

Any request to an internal endpoint without the `internal_api_key` header will result in a `401 Unauthorized` response.