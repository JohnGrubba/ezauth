# Default E-Mail Templates

EZAuth uses a set of default E-mail templates to send out e-mails to users. These templates are stored in the `config/email` folder. You can customize these templates as per your requirements.

!!! Info "E-Mail Subject"
    EZAuth will automatically use the HTML `<title></title>` tag to specify the subject of the e-mail.

## Required E-Mail Templates

??? Warning "Required Templates"
    Only edit those templates and don't delete them. If you delete them, the service will not work as expected.

### 1. **Email Verification**
- Can be enabled in the `config.json` file.
- File Name: `ConfirmEmail.html`

#### Additional Placeholders
- `{{code}}`: The confirmation code to confirm the email address.
- `{{time}}`: Time remaining before the confirmation code expires in minutes. (e.g. 5)
- `{{username}}`: The username of the user wanting to verify their email address.

!!! Info "Default Placeholders"
    Every E-Mail template which is directed at a registered user will be able to use any of the properties of the user in the database. This includes the `username`, `email`, `id`, and any other property you might have added to the user object.

### 2. **Welcome Email**
- Can be enabled in the `config.json` file.
- Will be sent out after the user has successfully verified their email address.
- File Name: `WelcomeMail.html`

# Custom E-Mail Templates

!!! Info "Work in Progress"
    This feature is still in development and might not work as expected.
You can also create custom E-mail templates and use them in the service. To use a custom E-mail template you need to specify the path to the template in the `config.json` file.