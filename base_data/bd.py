from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.orm import Session, declarative_base, relationship

from settings import (DB_HOST, DB_NAME, DB_PORT, POSTGRES_PASSWORD,
                      POSTGRES_USER, DEBUG)


if DEBUG:
    engine = create_engine(
        'postgresql+psycopg2://postgres:1234@localhost:5432/postgres'
    )
else:
    engine = create_engine(
        f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
        f'{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )
model = declarative_base()
session = Session(bind=engine)


class DayWeek(model):
    __tablename__ = 'day_week'

    id = Column(Integer(), primary_key=True)
    name = Column(String(12), nullable=False)
    parity = Column(Boolean(), nullable=False)
    couples = relationship('Couple', cascade='all,delete')

    def __repr__(self):
        return f'{self.name} Чётная:{self.parity}'


class Couple(model):
    __tablename__ = 'couple'

    id = Column(Integer(), primary_key=True)
    title = Column(String(200), nullable=False)
    university_building = Column(String(10), nullable=False)
    lecture_stream = Column(Boolean(), default=False, nullable=False)
    lecture_hall = Column(String(15), nullable=True)
    teacher = Column(String(150), nullable=True)
    period = Column(String(150), nullable=False)
    note = Column(String(200), nullable=True)
    time_from = Column(String(10), nullable=False)
    time_to = Column(String(10), nullable=False)
    type_of_occupation = Column(String(100), nullable=False)
    couple_num = Column(Integer(), nullable=None)
    week_id = Column(Integer(), ForeignKey('day_week.id'))

    def __repr__(self):
        return f'{self.title} {self.university_building}-{self.lecture_hall}'


model.metadata.create_all(engine)
