import fastapi as _fastapi
import fastapi.security as _security
from fastapi.middleware.cors import CORSMiddleware

import sqlalchemy.orm as _orm

import database as _database
import schemas as _schemas
import services as _services

app = _fastapi.FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.on_event("startup")


@app.get("/api")
async def index():
    return {"message": "Hello world!"}


@app.post("/api/users")
async def create_user(
    user_data: _schemas.UserCreate,
    db: _orm.Session = _fastapi.Depends(_database.get_db),
):
    db_user = await _services.get_user_by_email(user_data.email, db)

    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="이미 존재하는 이메일 입니다.")

    user = await _services.create_user(user_data=user_data, db=db)

    return await _services.create_token(user)


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


@app.post("/api/posts", response_model=_schemas.Post)
async def create_post(
    post_data: _schemas.PostCreate,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_database.get_db),
):
    return await _services.create_post(post_data, user, db)


@app.get("/api/posts/{post_id}", response_model=_schemas.Post)
async def get_post(
    post_id: int,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_database.get_db),
):
    return await _services.get_post_one(post_id, user, db)


@app.put("/api/posts/{post_id}", status_code=201)
async def update_post(
    post_id: int,
    post_data: _schemas.PostCreate,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_database.get_db),
):
    await _services.update_post(post_id, post_data, user, db)

    return {"message": "Successfully updated!"}


@app.delete("/api/posts/{post_id}", status_code=204)
async def delete_post(
    post_id: int,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_database.get_db),
):
    await _services.delete_post(post_id, user, db)

    return {"message": "Successfully deleted!"}
