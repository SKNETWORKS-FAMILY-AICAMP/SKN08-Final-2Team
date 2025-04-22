# models/account_prefer.py
from sqlalchemy import Column, Integer, Text, ForeignKey
from db import Base

class AccountPrefer(Base):
    __tablename__ = 'account_prefer'

    account_id = Column(Integer, primary_key=True, index=True)

    Q_1 = Column(Text)
    Q_2 = Column(Text)
    Q_3 = Column(Text)
    Q_4 = Column(Text)
    Q_5 = Column(Text)
    Q_6 = Column(Text)
    Q_7 = Column(Text)
    Q_8 = Column(Text)
    Q_9 = Column(Text)
    Q_10 = Column(Text)
    Q_11 = Column(Text)
    Q_12 = Column(Text)
    Q_13 = Column(Text)
    Q_14 = Column(Text)
    Q_15 = Column(Text)
    Q_16 = Column(Text)
    Q_17 = Column(Text)
    Q_18 = Column(Text)
    Q_19 = Column(Text)
    Q_20 = Column(Text)
