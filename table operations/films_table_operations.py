from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_models.films_table_model import FilmsTable, TableBase
from sqlalchemy.exc import IntegrityError
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(current_dir, r'resources\films.db')
engine = create_engine(f'sqlite:///{db_file}')
TableBase.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def insert_film(*films_to_add):
    with Session() as session:
        for film in films_to_add:
            try:
                existing_row = session.query(FilmsTable).filter_by(title=film.title, director=film.director).first()
                if existing_row:
                    print(f"A film with title '{film.title}' and director '{film.director}' already exists.")
                    continue
                else:
                    session.add(film)
                    session.commit()
                print(f"New film '{film.title}' added successfully.")
            except IntegrityError as e:
                print(f"Error: {e.orig}")
                session.rollback()


def update_film(film_title, film_director, **kwargs):
    with Session() as session:
        try:
            films_to_update = session.query(FilmsTable).filter_by(title=film_title, director=film_director).all()
            if films_to_update:
                for film in films_to_update:
                    for key, value in kwargs.items():
                        setattr(film, key, value)
                        session.commit()
                    print(f"Film '{film_title}' by '{film_director}' updated successfully.")
            else:
                print(f"No film found with title '{film_title}' and director '{film_director}'.")
        except Exception as e:
            print(f"Error: {e}")
            session.rollback()


def print_data_from_table(**kwargs):
    with Session() as session:
        query = session.query(FilmsTable)
        for key, value in kwargs.items():
            query = query.filter(getattr(FilmsTable, key) == value)
        results = query.all()
        if len(results) == 0:
            print(f"Film with {key}:{value} doesn't exist.")
        else:
            for film in results:
                print(film)


def delete_all_data_from_table(table):
    with Session() as session:
        try:
            session.query(table).delete()
            session.commit()
            print(f"All data deleted from the {table.__tablename__}.")
        except Exception as e:
            session.rollback()
            print(f"Error deleting data: {e}")


film1 = FilmsTable(title='Im Juli', director='Fatih Akin', release_year=2000)
film2 = FilmsTable(title='The Godfather', director='Francis Ford Coppola', release_year=1972)
film3 = FilmsTable(title='Pulp Fiction', director='Quentin Tarantino', release_year=1994)
film4 = FilmsTable(id=1, title='Gladiator', director='Ridley Scott', release_year=2000)

# insert_film(film1, film2, film3)
# insert_film(film4)
# update_film('Im Juli', 'Fatih Akin', release_year=1997)
print_data_from_table(title='Im Juli')
# delete_all_data_from_table(FilmsTable)
