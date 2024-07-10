## Google OAuth
### Setup Google OAuth
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Go to the [APIs & Services -> Credentials](https://console.cloud.google.com/apis/credentials) section.
4. Click on `Create credentials` and select `OAuth client ID`.
5. Select `Web application` as the application type.
6. Add the following URIs to the `Authorized redirect URIs` (Where `{BASE_URL}` is the Hostname of the server eg. `http://test.com`):
    - `{BASE_URL}/oauth/google/callback`
7. Add the following scopes
<img src="/assets/scopes_google.png" style='margin-top: 10px;' />

8. Click on `Create` and download the credentials as JSON and place them in the `config` folder.
Make sure the name of the file is `google_client_secret.env.json`.

## GitHub OAuth
### Setup GitHub OAuth
1. Go to the [GitHub Developer Settings](https://github.com/settings/developers)
2. Click on `New OAuth App`.
3. Add the following URIs to the `Authorization callback URL` (Where `{BASE_URL}` is the Hostname of the server eg. `http://localhost:3250`):
    - `{BASE_URL}/oauth/github/callback`
4. Create the Application and copy the `Client ID` and `Client Secret` and create the following file in the `config` folder.

```json title="github_client_secret.env.json"
{
    "client_id": "YOUR_CLIENT",
    "client_secret": "YOUR_SECRET"
}
```