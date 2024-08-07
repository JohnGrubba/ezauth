import json
import sys
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

if "pytest" in sys.modules:
    # Running Tests (Load Testing Config)
    config = json.load(open(os.path.join(__location__, "testing_config.json"), "rb"))
else:
    # Normal Startup
    config = json.load(open("/src/app/config/config.json", "rb"))

# Columns that should never leave EZAuth (maybe get more in the future)
default_signup_fields = {"username", "email", "password"}
insecure_cols = {"password": 0, "2fa_secret": 0, "google_uid": 0, "github_uid": 0}
not_updateable_cols_internal = ["createdAt", "expiresAfter"]
# Columns that can leave EZAuth but should only be used internally can be defined in config
