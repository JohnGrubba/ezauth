from fastapi import APIRouter, Depends
from api.dependencies.authenticated import get_pub_user


router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
    dependencies=[Depends(get_pub_user)],
)


@router.get("/")
async def profile(user: dict = Depends(get_pub_user)):
    """
    # Get Profile Information

    ## Description
    This endpoint is used to get the public profile information of the user.
    """
    return user
