from sqlalchemy import Table, MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
engine = create_engine("postgresql+psycopg2://postgres:140697@localhost:5432/library",
                       echo=False, pool_size=6, max_overflow=10, encoding='utf-8')
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)


# Инициализируем существующие таблицы в library

class Book(Base):
    __table__ = Table('book', metadata, autoload=True)


class People(Base):
    __table__ = Table('people', metadata, autoload=True)


class Reader(Base):
    __table__ = Table('reader', metadata, autoload=True)


class CommandsServer():
    session = Session()
    async def get_all_deptor(self, ):
        try:
            res = self.session.query(Reader.person_id, Reader.start_read,
                                     People.first_name, People.last_name, Book.book_name).join(Book).join(People).filter\
                (People.member_family == None, Reader.finish_read == None)
            return res.all()
        except Exception as exc:
            return exc

    def where_is_book(self, book_name):
        try:
            res = self.session.query(Reader.start_read, People.first_name,
                                       People.last_name, People.person_id, ).join(Book).join(People). \
                filter(Book.book_name == book_name, Book.at_home == False)
            print(res.all())
            return res.all()
        except Exception as exc:
            return exc

    async def have_read(self, member_family):
        try:
            res = self.session.query(Reader.person_id, Reader.start_read, Reader.finish_read, Book.book_name). \
                join(Book).join(People) \
                .filter(Reader.finish_read != None, People.member_family == member_family)
            return res.all()
        except Exception as exc:
            return exc

    async def who_gaves(self, member_family):
        try:
            res = self.session.query(People.person_id).filter(People.member_family == member_family)
            res_2 = self.session.query(Reader.start_read,People.person_id, People.first_name, People.last_name).\
                join(People).filter(People.friend_family == res[0][0])
            return res_2.all()
        except Exception as exc:
            return exc


# a = CommandsServer().where_is_book("Улисск")