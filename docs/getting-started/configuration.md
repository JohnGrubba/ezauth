# Configuration

To configure EZAuth you can take a look at the `configtemplate.json` file in the `config` directory. This file contains all the configuration options for EZAuth.

## Parameters table

All configuration parameters are listed in the tables below.
Make sure that all parameters are set correctly before starting the service.

### Signup Configuration
|  Parameter | Description |
|------------|-------------|
| `signup.enable_conf_email` | **Datatype:** Boolean <br> **Default:** `false` <br> Enable or disable the confirmation E-Mail for new users. |
| `signup.conf_code_expiry` | **Datatype:** Integer <br> **Default:** `5` <br> The time in minutes until the confirmation code expires. |
| `signup.enable_welcome_email` | **Datatype:** Boolean <br> **Default:** `false` <br> Enable or disable the welcome E-Mail for new users. |

### Email Configuration

??? Warning "SMTP SSL required"
    EZAuth uses SMTP_SSL to send E-Mails. Make sure that your SMTP server supports SSL.
    Currently EZAuth does not support STARTTLS.

|  Parameter | Description |
|------------|-------------|
| `email.login_usr` | **Datatype:** String <br> **Default:** `""` <br> E-Mail Login Identifier (mostly the email itself). <br> **Example:** test@test.com |
| `email.login_pwd` | **Datatype:** String <br> **Default:** `""` <br> E-Mail Login Password. |
| `email.sender_email` | **Datatype:** String <br> **Default:** `""` <br> E-Mail address from which the emails are sent (mostly the same as `email.login_usr`) |
| `email.smtp_host` | **Datatype:** String <br> **Default:** `""` <br> SMTP Host for the E-Mail server. <br> **Example:** `smtp.gmail.com` |
| `email.smtp_port` | **Datatype:** Integer <br> **Default:** `465` <br> SMTP Port for the E-Mail server. |