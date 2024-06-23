# Configuration

## Email Configuration
- All Template emails are stored in `config/email` folder.
- You can customize the email templates as per your requirements.
- To specify a subject, use the HTML `<title></title>` tag.

### Required Email Templates
1. **Email Verification**
    - Can be enabled in the `config.json` file.
    - Check [here](./email/ConfirmEmail.md) for predefined placeholders.

2. **Welcome Email**
    - Can be enabled in the `config.json` file.
    - Will be sent out after the user has successfully verified their email address.
    - Check [here](./email/WelcomeMail.md) for predefined placeholders.