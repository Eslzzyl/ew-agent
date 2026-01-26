import os
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
    Index,
)
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker


class Base(DeclarativeBase):
    pass


class FoodChoice(Base):
    __tablename__ = "food_choices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, comment="餐厅名称")
    food_type = Column(String(100), nullable=False, comment="餐食品种")
    description = Column(String(500), nullable=True, comment="根据用户评价得出的描述")
    created_at = Column(
        DateTime, default=datetime.now, nullable=False, comment="创建时间"
    )

    eating_histories = relationship(
        "EatingHistory", back_populates="food_choice", cascade="all, delete-orphan"
    )


class EatingHistory(Base):
    __tablename__ = "eating_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    food_choice_id = Column(
        Integer, ForeignKey("food_choices.id"), nullable=False, comment="关联的餐厅ID"
    )
    meal_type = Column(String(20), nullable=False, comment="餐次：早/午/晚饭")
    eaten_at = Column(
        DateTime, default=datetime.now, nullable=False, comment="吃饭时间"
    )
    user_id = Column(String(100), nullable=True, comment="用户ID")

    food_choice = relationship("FoodChoice", back_populates="eating_histories")


class GlobalInfo(Base):
    __tablename__ = "global_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(200), nullable=False, comment="信息键名")
    value = Column(Text, nullable=True, comment="信息值（纯文本）")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间"
    )

    __table_args__ = (Index("ix_global_info_key", "key", unique=True),)


DATABASE_URL = (
    f"sqlite:///{os.path.join(os.path.dirname(__file__), 'data', 'eat_what.db')}"
)
os.makedirs("data", exist_ok=True)
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
