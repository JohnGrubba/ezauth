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

## Advanced E-Mail Templating
If our provided placeholders are not enough, and you need more logic behind your Templating, you can use our `preprocessing` feature.
This feature allows you to run a custom function on the E-Mail Template before it is sent out. This function will be able to add / modify / remove placeholders from the template. You can also use this function to add custom logic to the template.<br>
Examples of what you can do with this feature:

!!! Info "Usage Examples of Preprocessing E-Mail Templates"
    - Adding a Formatted Date to the E-Mail Template
    - Utilizing an external Service to generate a QR Code
    - Adding a Random Quote to the E-Mail Template
    - Sending a Request to an external API

### Example
In this example, we will add a `timestamp` placeholder to the E-Mail Template. This placeholder will contain the current date and time when the E-Mail is sent out.

!!! Note "Preprocessing Function"
    - The function should be defined in a Python file in the `config/email` folder. The function should be named `preprocess` and should accept a single parameter `kwargs` which is a dictionary containing all the placeholders available in the E-Mail Template.
    - The function should return the modified `kwargs` object.
    - The Filename should be the same as the E-Mail Template filename with the `.py` extension. (e.g. `WelcomeMail.py` for the `WelcomeMail.html` template)

In this example, we will add a `timestamp` placeholder to the `ConfirmEmail.html` template.
```python hl_lines="4" linenums="1" title="config/email/ConfirmEmail.py"
from datetime import datetime

def preprocess(kwargs: dict) -> dict:
    kwargs["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return kwargs

```