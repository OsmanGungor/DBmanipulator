from sqlalchemy import create_engine
from table_models.films_table_model import TableBase
import os


def create_table():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_file_path = os.path.join(current_dir, r'resources\films.db')
    engine = create_engine(f'sqlite:///{db_file_path}', echo=True)
    TableBase.metadata.create_all(engine)


create_table()
