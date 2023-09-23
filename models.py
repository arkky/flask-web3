from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from database import engine


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(30))
    surname: Mapped[Optional[str]] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    eth_address: Mapped[Optional[str]] = mapped_column(String(120))
    password: Mapped[str] = mapped_column(String(100))
    signature: Mapped[Optional[str]] = mapped_column(String(256))

    def __repr__(self):
        return f'<User {self.name!r}>'


class Auth(Base):
    __tablename__ = "auth"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    jwt_token: Mapped[str]


if __name__ == "__main__":
    Base.metadata.create_all(engine)