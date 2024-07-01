from fastapi import APIRouter, Response
from api.model import UserSignupRequest, LoginResponse, ConfirmEmailCodeRequest
from tools import send_email
from tools import SignupConfig
from expiring_dict import ExpiringDict
import random
from crud.user import create_user

# Create an ExpiringDict object to store temporary accounts (not email verified yet)
temp_accounts = ExpiringDict(ttl=SignupConfig.conf_code_expiry * 60, interval=10)

# Generate and shuffle 10000 unique IDs for confirmation email (Depending on complexity)
match (SignupConfig.conf_code_complexity):
    case 2:
        # Random 6 Digit Numbers
        all_ids = [str(random.randint(100000, 999999)) for _ in range(10000)]
        random.shuffle(all_ids)
    case 3:
        # Random 4 Character Strings
        all_ids = [
            "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=4))
            for _ in range(10000)
        ]
        random.shuffle(all_ids)
    case 4:
        # Random 6 Character Strings
        all_ids = [
            "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=6))
            for _ in range(10000)
        ]
        random.shuffle(all_ids)
    case _:
        # Default Case (1)
        all_ids = [str(i) for i in range(10000)]
        random.shuffle(all_ids)

router = APIRouter(
    prefix="/signup",
    tags=["Sign Up"],
    dependencies=[],
)


@router.post(
    "/",
    status_code=200,
    responses={
        409: {"description": "Duplicate Entry"},
        204: {"description": "Confirmation Email Sent"},
        200: {"description": "Account was created successfully."},
    },
)
async def signup(signup_form: UserSignupRequest):
    if SignupConfig.enable_conf_email:
        # If all numbers have been used, raise an exception
        if not all_ids:
            raise Exception(
                "All unique IDs have been used. More than 10000 signups in a short time."
            )
        # Get a unique ID for confirmation email
        unique_id = all_ids.pop()
        # Save the Account into the expiring dict (delete if user refuses to confirm email in time)
        temp_accounts[unique_id] = signup_form

        # Generate and send confirmation email
        send_email(
            "ConfirmEmail",
            signup_form.email,
            code=unique_id,
            time=SignupConfig.conf_code_expiry,
            username=signup_form.username,
        )
        return Response(status_code=204)
    else:
        return create_user(signup_form)


@router.post(
    "/confirm",
    response_model=LoginResponse,
    responses={
        404: {"description": "No Account Found with this code. Or Code expired."},
        200: {"description": "Account was created successfully."},
    },
)
async def confirm_email(payload: ConfirmEmailCodeRequest):
    try:
        acc: UserSignupRequest = temp_accounts[payload.code]
        if acc.email != payload.email:
            return Response(status_code=404)
    except KeyError:
        return Response(status_code=404)
    del temp_accounts[payload.code]
    # Account is confirmed, create the user
    return create_user(acc)
