import datetime

import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash

import database as _database


class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, index=True, nullable=False)
    username = _sql.Column(_sql.String, index=True, nullable=False)
    company_name = _sql.Column(_sql.String, index=True, nullable=False)
    hashed_password = _sql.Column(_sql.String, nullable=False)
    is_active = _sql.Column(_sql.Boolean, default=True, nullable=False)
    is_staff = _sql.Column(_sql.Boolean, default=False, nullable=False)
    is_superuser = _sql.Column(_sql.Boolean, default=False, nullable=False)

    posts = _orm.relationship("Post", back_populates="user")

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)

    # @_orm.validates("hashed_password")
    # def validate_email(self, key, address):
    #     pass

    def __repr__(self) -> str:
        return f"User({self.email!r}, {self.username!r}, {self.company_name!r})"


class Post(_database.Base):
    __tablename__ = "posts"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, index=True, nullable=False)
    content = _sql.Column(_sql.String, index=True, nullable=False)
    date_created = _sql.Column(
        _sql.DateTime, default=datetime.datetime.now, nullable=False
    )
    date_last_updated = _sql.Column(
        _sql.DateTime, default=datetime.datetime.now, nullable=False
    )

    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"), nullable=False)
    user = _orm.relationship("User", back_populates="posts")

    def __repr__(self) -> str:
        return f"Post({self.title!r})"
