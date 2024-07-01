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


### E-Mail Configuration

!!! Warning "SMTP SSL required"
    EZAuth uses SMTP_SSL to send E-Mails. Make sure that your SMTP server supports SSL.
    Currently EZAuth does not support STARTTLS.

|  Parameter | Description |
|------------|-------------|
| `email.login_usr` | **Datatype:** String <br> **Default:** `""` <br> E-Mail Login Identifier (mostly the E-Mail itself). <br> **Example:** test@test.com |
| `email.login_pwd` | **Datatype:** String <br> **Default:** `""` <br> E-Mail Login Password. |
| `email.sender_email` | **Datatype:** String <br> **Default:** `""` <br> E-Mail address from which the E-Mails are sent (mostly the same as `email.login_usr`) |
| `email.smtp_host` | **Datatype:** String <br> **Default:** `""` <br> SMTP Host for the E-Mail server. <br> **Example:** `smtp.gmail.com` |
| `email.smtp_port` | **Datatype:** Integer <br> **Default:** `465` <br> SMTP Port for the E-Mail server. |

### Session Configuration
|  Parameter | Description |
|------------|-------------|
| `session.session_expiry_seconds` | **Datatype:** Integer <br> **Default:** `86400` <br> The time in seconds until a login session expires. |
| `session.max_session_count` | **Datatype:** Integer <br> **Default:** `5` <br> Maximum amount of sessions for one User. |
| `session.auto_cookie` | **Datatype:** Boolean <br> **Default:** `true` <br> Specifies if the API should automatically return a `Set-Cookie` header to potentially automatically set the Session Token for the client. May simplify upcoming requests to this API. |
| `session.auto_cookie_name` | **Datatype:** String <br> **Default:** `session` <br> The name of the cookie which will be set by the API. |

### Internal API Configuration

!!! danger "Internal API Key"
    Change this **immediately** after cloning the repository. Keeping the default value is a **severe security risk**.

|  Parameter | Description |
|------------|-------------|
| `internal.internal_api_key` | **Datatype:** String <br> **Default:** `CHANGE_ME_NOW` <br> This is **sensitive** information and must **never** be exposed anywhere. |