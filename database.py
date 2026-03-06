from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///games.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    input_name = Column(String, nullable=False)
    normalized_name = Column(String, nullable=False, unique=True)
    steam_appid = Column(Integer, nullable=True)
    steam_positive_pct = Column(Float, nullable=True)
    steam_review_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

Base.metadata.create_all(engine)