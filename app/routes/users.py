from urllib.request import Request
import fastapi
from fastapi import Depends, HTTPException, Response
from fastapi.responses import RedirectResponse

from app.database.db import get_session
from sqlmodel import Session, select
from app.models.models import AccessCompany
from app.models.basemodels import AccessCompanyModel

from app.security import bearer
from app.security.bearer import *

router = fastapi.APIRouter()

# Insert Access Company Entry to test
# db.create_access_company_table()

# Get Token and Sign In
@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends(), session: Session=Depends(get_session)):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires, type=1
    )

    refresh_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires, type=2
    )

    return {"user": user, "access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post(
    '/sign_up',
    # dependencies=[Depends(bearer.get_current_active_user)],
    # tags=["Authentication"],
    # include_in_schema=True,
    # description="Sign up a user",
)
def sign_up_user(accessCompanyModel: AccessCompanyModel, session: Session= Depends(get_session)):

    query_result = session.query(AccessCompany).filter(AccessCompany.login == AccessCompanyModel.login).first()

    if query_result is not None:
        return {'Status': 'Success', 'Response': 'Already Exists'}

    try:
        new_user = AccessCompany(
            login = accessCompanyModel.login,
            password = get_password_hash(accessCompanyModel.password),
        )
        session.add(new_user)
        session.commit()

        # return RedirectResponse('/token', status_code=303)
        return {'Status': 'Success', 'Response': 1}
    except:
        return {'Status': 'Fail', 'Response': 'Failed to sign up'}

@router.get(
    "/signout",
    dependencies=[Depends(bearer.get_current_active_user)],
    tags=["Authentication"],
    include_in_schema=True,
    description="Sign out a user",
)
def signout(response: Response):
    # response = templates.TemplateResponse("login.html", {"request": request, "title": "Login", "current_user": AnonymousUser()})
    # response.delete_cookie("access_token")
    # return response
    return 'OK'