# Internal API

EZAuth provides an internal API for other services to interact with the service. This API is not meant to be exposed to the public and should only be used by services that are running on the same network as the EZAuth service.
The Idea is to provide only the User ID to other services, which can then be stored in their own database to reference the user.
And once the data is needed, the service can use the internal API to get the user data. This way the user data is not exposed to the public and always kept secure by EZAuth :)

!!! danger "Internal API Key"
    Even though it is recommended to hide the `/internal` endpoints from the public with a middleware, you should still keep the `internal-api-key` secret. If someone gets access to this key, they can access all the internal API endpoints.

## Access the Internal API

To access any endpoints prefixed with `/internal` you need to set the `internal-api-key` header.

Example in Python:

```python
import requests

url = "http://localhost:3250/internal/<whatever_endpoint>"
headers = {
    "internal-api-key": "YOUR_INTERNAL_API_KEY"
}

response = requests.get(url, headers=headers)
print(response.json())
```

Any request to an internal endpoint without the `internal-api-key` header will result in a `401 Unauthorized` response.


!!! Info "E-Mail Information"
    For more information on how to send E-Mails using the internal API, see the [E-Mail Configuration](./configuration/email_templates.md#custom-e-mail-templates) section.