from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from modules.Role import Role

class Base(DeclarativeBase):
    ...

class UserModel(Base):
    __tablename__ = "user"

    role: Mapped[Role] = mapped_column(default = Role.basic)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)