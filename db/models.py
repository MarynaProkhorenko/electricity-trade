from sqlalchemy import Column, Integer, Date, Float, UniqueConstraint

from db.engine import Base, engine


class DBPricing(Base):
    __tablename__ = "price"
    __table_args__ = (UniqueConstraint("date", "hour"),)

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date())
    hour = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)


Base.metadata.create_all(engine)
