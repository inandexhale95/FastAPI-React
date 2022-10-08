import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import jwt

import models as _models
import schemas as _schemas
import database as _database

oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")

JWT_SECRET = "secret"


async def get_user_by_email(user_email: str, db: _orm.Session) -> "_models.User":
    return db.query(_models.User).filter(_models.User.email == user_email).first()


async def create_user(user: _schemas.UserCreate, db: _orm.Session):
    user_obj = _models.User(
        email=user.email,
        username=user.username,
        company_name=user.company_name,
        hashed_password=_hash.bcrypt.hash(user.hashed_password),
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(email, db)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user


async def create_token(user: _models.User):
    user_obj = _schemas.User.from_orm(user)

    token = jwt.encode(payload=user_obj.dict(), key=JWT_SECRET)

    return dict(access_token=token, token_type="bearer")


async def get_current_user(
    token: str = _fastapi.Depends(oauth2schema),
    db: _orm.Session = _fastapi.Depends(_database.get_db),
):
    try:
        payload = jwt.decode(jwt=token, key=JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except:
        raise _fastapi.HTTPException(status_code=401, detail="이메일이나 패스워드가 일치하지 않습니다.")

    return _schemas.User.from_orm(user)
