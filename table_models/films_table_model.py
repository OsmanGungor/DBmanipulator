from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

TableBase = declarative_base()


class FilmsTable(TableBase):
    __tablename__ = 'films'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    director = Column(Integer)
    release_year = Column(Integer)

    def __str__(self):
        return f"films id={self.id}, title='{self.title}', release_year={self.release_year},director='{self.director}' "
