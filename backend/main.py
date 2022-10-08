import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm

import database as _database
import schemas as _schemas
import services as _services

app = _fastapi.FastAPI()

# @app.on_event("startup")


@app.post("/api/users", response_model=_schemas.User)
async def create_user(
    user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_database.get_db)
):
    db_user = await _services.get_user_by_email(user.email, db)

    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="이미 존재하는 이메일 입니다.")

    return await _services.create_user(user=user, db=db)


@app.post("/api/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_database.get_db),
):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="인증에 실패했습니다.")

    return await _services.create_token(user)


@app.get("/api/users/me", response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user
