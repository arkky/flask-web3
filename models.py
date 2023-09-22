from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    eth_address: Mapped[str] = mapped_column(String(120))
    password: Mapped[str] = mapped_column(String(100))
    token: Mapped[str] = mapped_column(String(256))

    def __init__(self, name, surname, email, eth_address, password, token):
        self.name = name
        self.surname = surname
        self.email = email
        self.eth_address = eth_address
        self.password = password
        self.token = token

    def __repr__(self):
        return f'<User {self.name!r}>'
