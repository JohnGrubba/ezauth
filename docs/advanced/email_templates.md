If the provided placeholders are not enough, and you need more logic behind your Templating, you can use our `preprocessing` feature.
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