## Google OAuth
### Setup Google OAuth
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Go to the [APIs & Services -> Credentials](https://console.cloud.google.com/apis/credentials) section.
4. Click on `Create credentials` and select `OAuth client ID`.
5. Select `Web application` as the application type.
6. Add the following URIs to the `Authorized redirect URIs`:
    - `http://localhost:3250/oauth/google/callback`
7. Add the following scopes
<img src="/assets/scopes_google.png" style='margin-top: 10px;' />

8. Click on `Create` and download the credentials as JSON and place them in the `config` folder.
Make sure the name of the file is `client_secret.env.json`.