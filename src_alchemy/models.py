import datetime
from typing import List

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

user_group = Table(
    "user_group",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("usergroup_id", Integer, ForeignKey("usergroup.id"))
)


class UserGroup(Base):
    __tablename__ = "usergroup"

    id: str = Column(Integer, primary_key=True)
    name: str = Column(String(50))

    def __str__(self):
        return self.name


class User(Base):
    __tablename__ = "user"

    id: str = Column(Integer, primary_key=True)
    username: str = Column(String(100), unique=True)
    email: str = Column(String(254), nullable=True, unique=True)
    groups: List[UserGroup] = relationship(
        "UserGroup",
        secondary=user_group,
        backref="users"
    )
    created_at: datetime.datetime = Column(DateTime(), server_default=func.now())
    updated_at: datetime.datetime = Column(DateTime(), onupdate=func.now())

    addresses: List = relationship("UserAddress", back_populates="user")

    def __str__(self):
        return self.username


class UserAddress(Base):
    __tablename__ = "useraddress"

    id: str = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, ForeignKey("user.id"))
    user: User = relationship("User", back_populates="addresses")
    address: str = Column(String(100))
    zip_code: str = Column(String(5))
    city: str = Column(String(50))
    created_at: datetime.datetime = Column(DateTime(), server_default=func.now())
    updated_at: datetime.datetime = Column(DateTime(), onupdate=func.now())

    def __str__(self):
        return f"{self.address}, {self.zip_code} {self.city}"
