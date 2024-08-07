# E-Mail Templates
EZAuth uses a set of default E-mail templates to send out e-mails to users. These templates are stored in the `config/email` folder. You can customize these templates as per your requirements.

!!! Info "E-Mail Subject"
    EZAuth will automatically use the HTML `<title></title>` tag to specify the subject of the e-mail.

!!! Info "Default Placeholders"
    Every E-Mail template which is directed at a registered user will be able to use any of the properties of the user in the database. This includes the `username`, `email`, `id`, and any other property you might have added to the user object.

## Required E-Mail Templates

!!! Warning "Required Templates"
    Only edit those templates and don't delete them. If you delete them, the service will not work as expected.

### 1. **Email Verification**
- Can be enabled in the `config.json` file.
- File Name: `ConfirmEmail.html`

This can also be triggered, when a user changes their email address. So avoid wording like "new account" in the template.

#### Additional Placeholders
- `{{code}}`: The confirmation code to confirm the email address.
- `{{time}}`: Time remaining before the confirmation code expires in minutes. (e.g. 5)
- `{{username}}`: The username of the user wanting to verify their email address.

### 2. **Welcome Email**
- Can be enabled in the `config.json` file.
- Will be sent out after the user has successfully verified their email address.
- File Name: `WelcomeMail.html`

### 3. **Password Reset**
- Can be enabled in the `config.json` file.
- Will be sent out when a user requests a password reset.
- File Name: `ChangePassword.html`

#### Additional Placeholders
- `{{code}}`: The confirmation code to confirm the password change.
- `{{time}}`: Time remaining before the confirmation code expires in minutes. (e.g. 5). This will be the same as the `signup.conf_code_expiry` value in the `config.json` file.


## Custom E-Mail Templates
You can add custom e-mail templates to the `config/email` folder.
Whenever you are able to specifiy a E-Mail Template, you can specify the template you want to use by providing the file name without the `.html` extension.
Example: `WelcomeMail` will use the `WelcomeMail.html` template.

!!! Info "Broadcast E-Mails"
    By using the Internal API you can send out broadcast e-mails to all users. This can be useful for maintenance notifications or other important information.
    You can also provide a custom [MongoDB Filter](https://www.mongodb.com/docs/compass/current/query/filter/) to only send the e-mail to a specific group of users. Example: `{"sexual_preference": "gay"}` -> This will only send the e-mail to users who have `gay` as their `sexual_preference`.