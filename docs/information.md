# Information about EZAuth

EZAuth is a simple and easy-to-use authentication service for your applications. It is built on top of [FastAPI](https://fastapi.tiangolo.com/)
and [MongoDB](https://www.mongodb.com/). It also uses [Redis](https://redis.io/) for temporary storage.

## Security
To guarantee the security of your user data, EZAuth uses the following security measures:

- **Password Hashing**: All passwords are hashed using the `bcrypt` algorithm.
- **Session Management**: Sessions can be configured to expire after a certain amount of time. Users can also delete sessions manually if they forgot to log out elsewhere.
- **E-Mail Verification**: Users can verify their email address before using the service.
- **2FA**: Two-factor authentication can be enabled for users.
- **OAuth2**: OAuth2 can be enabled for users.
- **Rate Limiting**: Rate limiting can be enabled to prevent brute force attacks.
- **Password Reset**: Users can reset their password via E-Mail.

## Documentation
You are reading the informative documentation for EZAuth. 
If you need a documentation of all the endpoints, you can start the service and navigate to the `/docs` endpoint to find the API Documentation.
Because we utilize FastAPI, the documentation is done automatically and displayed via Swagger UI.
This also makes the API OpenAPI compliant.

!!! Info "API Documentation"
    Navigate to [`http://localhost:3250/docs`](http://localhost:3250/docs) to see the API Documentation.

## Code Examples

!!! Info "Official Libraries"
    We are working on official Libraries for different languages. Until then, you can use the REST API to interact with the service.
    Every help is appreciated.


You can use EZAuth in any Application and or Language that supports HTTP.
Here are some examples in different languages:

### Python
```py linenums="1"
import requests

url = "http://localhost:3250/signup/"

payload = {
    "email": "testemail123@email.com",
    "username": "Hans",
    "password": "Kennwort1!",
}

requests.post(url, json=payload)
```

### JavaScript
```js linenums="1"
fetch("http://localhost:3250/signup/", {
    method: 'POST',
    headers: {
        "Content-Type", "application/json"
    },
    body: JSON.stringify({
        "email": "testemail123@email.com",
        "username": "Hans",
        "password": "Kennwort1!"
    })
})
```

### cURL
```bash
curl -X 'POST'
'http://localhost:3250/signup/'
-H 'Content-Type: application/json'
-d '{
    "email": "testemail123@email.com",
    "username": "Hans",
    "password": "Kennwort1!"
}'
```
