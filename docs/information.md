# Information about EZAuth

EZAuth is a simple and easy-to-use authentication service for your applications. It is built on top of [FastAPI](https://fastapi.tiangolo.com/)
and [MongoDB](https://www.mongodb.com/).

## Security
To guarantee the security of your user data, EZAuth uses the following security measures:

- **Password Hashing**: All passwords are hashed using the `bcrypt` algorithm.
- **Session Management**: Sessions can be configured to expire after a certain amount of time.
- **E-Mail Verification**: Users can verify their email address before using the service.
- **2FA**: Two-factor authentication can be enabled for users.
- **OAuth2**: OAuth2 can be enabled for users.