# Configuration

To configure EZAuth you can take a look at the `configtemplate.json` file in the `config` directory. This file contains all the configuration options for EZAuth.

## Parameters table

All configuration parameters are listed in the tables below.
Make sure that all parameters are set correctly before starting the service.

!!! Warning "Apply Configuration"
    If you change the configuration file, make sure to restart the service to apply the changes.

### Signup Configuration
|  Parameter | Description |
|------------|-------------|
| `signup.enable_conf_email` | **Datatype:** Boolean <br> **Default:** `false` <br> Enable or disable the confirmation E-Mail for new users. |
| `signup.conf_code_expiry` | **Datatype:** Integer <br> **Default:** `5` <br> The time in minutes until the confirmation code expires. |
| `signup.conf_code_complexity` | **Datatype:** Integer <br> **Default:** `1` <br> The complexity of the confirmation code. <br> **Possible Values** <br> <ul><li>**1**: `4 Digit Numeric`</li><li>**2**: `6 Digit Numeric`</li><li>**3**: `4 Characters`</li><li>**4**: `6 Characters`</li></ul>  |
| `signup.enable_welcome_email` | **Datatype:** Boolean <br> **Default:** `false` <br> Enable or disable the welcome E-Mail for new users. |
| `signup.oauth.providers_enabled` | **Datatype:** List <br> **Default:** `[]` <br> Enabled OAuth Providers.  <br> **Possible Providers**<ul><li>[**Google**](../advanced/oauth.md#google-oauth)</li><li>[**GitHub**](../advanced/oauth.md#github-oauth)</li></ul>  |
| `signup.oauth.base_url` | **Datatype:** String <br> **Default:** `"http://localhost:3250/"` <br> The Base URL for the callback URL from OAuth Providers. When you host the service somewhere, you may want to change this to the official Domain instead of an IP. This is also the value you set when setting up your OAuth Providers. Make sure those values match. |
| `signup.password_complexity` | **Datatype:** Integer <br> **Default:** `4` <br> Password Complexity Requirement. Every higher value, includes all the previous ones too.<br> <ul><li>**1**: Minimum 8 Characters</li><li>**2**: Min. One Digit</li><li>**3**: Min. One Capital Letter</li><li>**4**: Min. One Special Character</li></ul>  |
| `signup.username_complexity` | **Datatype:** Integer <br> **Default:** `2` <br> Username Complexity Requirement. Every higher value, includes all the previous ones too.<br> <ul><li>**1**: Minimum 4 Characters</li><li>**2**: Max. 20 Characters</li></ul>  |

### E-Mail Configuration

!!! Warning "SMTP SSL required"
    EZAuth uses SMTP_SSL to send E-Mails. Make sure that your SMTP server supports SSL.
    Currently EZAuth does not support STARTTLS.

|  Parameter | Description |
|------------|-------------|
| `email.login_usr` | **Datatype:** String <br> **Default:** `""` <br> E-Mail Login Identifier (mostly the E-Mail itself). <br> **Example:** test@test.com |
| `email.login_pwd` | **Datatype:** String <br> **Default:** `""` <br> E-Mail Login Password. |
| `email.sender_email` | **Datatype:** String <br> **Default:** `""` <br> E-Mail address from which the E-Mails are sent. Can be changed to something like `EZAuth <ezauth.noreply@gmail.com` to achieve a nicer looking E-Mail. |
| `email.smtp_host` | **Datatype:** String <br> **Default:** `""` <br> SMTP Host for the E-Mail server. <br> **Example:** `smtp.gmail.com` |
| `email.smtp_port` | **Datatype:** Integer <br> **Default:** `465` <br> SMTP Port for the E-Mail server. |

### Session Configuration
|  Parameter | Description |
|------------|-------------|
| `session.session_expiry_seconds` | **Datatype:** Integer <br> **Default:** `86400` <br> The time in seconds until a login session expires. Expires on Client (Browser) and on the Server (Database). |
| `session.max_session_count` | **Datatype:** Integer <br> **Default:** `5` <br> Maximum amount of sessions for one User. |
| `session.auto_cookie` | **Datatype:** Boolean <br> **Default:** `true` <br> Specifies if the API should automatically return a `Set-Cookie` header to potentially automatically set the Session Token for the client. May simplify upcoming requests to this API. |
| `session.auto_cookie_name` | **Datatype:** String <br> **Default:** `"session"` <br> The name of the cookie which will be set by the API. |
| `session.cookie_samesite` | **Datatype:** String <br> **Default:** `none` <br> Same Site Cookie Mode. <br> <ul><li>**none**</li><li>**strict**</li><li>**lax**</li></ul> |
| `session.cookie_secure` | **Datatype:** Boolean <br> **Default:** `true` <br> Secure Cookie Mode. |

### Internal API Configuration

!!! danger "Internal API Key"
    Change this **immediately** after cloning the repository. Keeping the default value is a **severe security risk**.

|  Parameter | Description |
|------------|-------------|
| `internal.internal_api_key` | **Datatype:** String <br> **Default:** `"CHANGE_ME_NOW"` <br> This is **sensitive** information and must **never** be exposed anywhere. |
| `internal.internal_columns` | **Datatype:** List <br> **Default:** `["_id"]` <br> Columns that should only be revealed via the internal API. This example will never reveal `_id` to public endpoints, but just to the `/internal` endpoints as well as E-Mails. |
| `internal.not_updateable_columns` | **Datatype:** List <br> **Default:** `["email"]` <br> Columns that should not be able to get updated via the public API. |

### Account Features Configuration
|  Parameter | Description |
|------------|-------------|
| `account_features.enable_reset_pswd` | **Datatype:** Boolean <br> **Default:** `true` <br> Enable or disable the password reset feature. |
| `account_features.reset_pswd_conf_mail` | **Datatype:** Boolean <br> **Default:** `true` <br> Enable or disable the password change confirmation E-Mail. |
| `account_features.2fa.enable` | **Datatype:** Boolean <br> **Default:** `false` <br> Enable or disable two factor for Login. 2FA was tested with [Google Authenticator](https://support.google.com/accounts/answer/1066447) and [2FAS Auth](https://2fas.com/) |
| `account_features.2fa.issuer_name` | **Datatype:** String <br> **Default:** `"EZAuth"` <br> How the two factor code will be titled in the users 2FA App. (Mostly the App Name) |
| `account_features.2fa.issuer_image_url` | **Datatype:** String <br> **Default:** `""` <br> URL for an optional Image which will be displayed in the 2FA App. |
| `account_features.2fa.qr_endpoint` | **Datatype:** Boolean <br> **Default:** `true` <br> Enable or disable QR Code Generation Endpoint for 2FA Login. This can be useful if you don't want to use any libraries on the client Side. |
| `account_features.allow_add_fields_on_signup` | **Datatype:** List <br> **Default:** `[]` <br> Allow those additional fields on signup. Leave empty if not sure. |
| `account_features.allow_add_fields_patch_user` | **Datatype:** List <br> **Default:** `[]` <br> Allow those additional fields to be set when modifying user. Leave empty if not sure. The entries here extend already set `account_features.allow_add_fields_on_signup` fields. |
| `account_features.allow_deletion` | **Datatype:** Boolean <br> **Default:** `true` <br> Allow the user to request an account deletion. |
| `account_features.deletion_pending_minutes` | **Datatype:** Integer <br> **Default:** `10080` <br> Minutes before the account gets deleted. Directly after requesting deletion, the User can't log in anymore, but the data will be persisted until this value passes by. Example Value is a Week.  |

!!! Note "Additional Fields"
    The `allow_add_fields_on_signup` makes it possible to add custom fields to the signup process. If you don't set the fields that are allowed here on signup, you can't update them later, except you also have them in `allow_add_fields_patch_user`.


### Security Configuration

!!! Warning "CORS Configuration"
    Be careful when configuring CORS. Leaving the `security.allow_origins` at `*` can lead to security vulnerabilities. Make sure to also check if your `session.cookie*` settings work with your CORS settings. When setting `allow_origins` to `*`, the auto cookie functionality may not work Cross Site. Google Chrome will remove Cross Domain Cookies Support in the future so be careful when configuring this setting and always test it before deploying.

|  Parameter | Description |
|------------|-------------|
| `security.allow_origins` | **Datatype:** List <br> **Default:** `["*"]` <br> CORS (Cross Origin Ressource Sharing) Policy. Enables access from different domains. Don't leave at `*` |
| `security.allow_headers` | **Datatype:** List <br> **Default:** `["*"]` <br> Allowed HTTP Headers. Can be used to restrict certain users from accessing EZAuth. |
| `security.max_login_attempts` | **Datatype:** Integer <br> **Default:** `5` <br> Maximum amount of login attempts before the account gets locked. Set to `0` to disable. If a User performs a successfull login the counter gets deleted. If this doesn't happen (counter doesn't reach maximum but still has a value), the failed attempts will be expired after `security.expire_unfinished_timeout`. |
| `security.login_timeout` | **Datatype:** Integer <br> **Default:** `5` <br> Time in minutes until the account gets unlocked after the maximum login attempts. |
| `security.expire_unfinished_timeout` | **Datatype:** Integer <br> **Default:** `60` <br> Time in minutes until the failed login attempts get expired. (Without reaching the max_login_attempts) |