from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Usuario import Base
from Ponto import Ponto
from Usuario import Usuario

USER = "postgres"
PASSWORD = "coders"
HOST = "localhost"
PORT = "5432"
DBNAME = "racing_coders"

#É necessário criar o banco com essas informações pessoal

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"

engine = create_engine(DATABASE_URL, echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()