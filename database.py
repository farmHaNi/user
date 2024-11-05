from typing import Optional
from sqlmodel import SQLModel, Session, create_engine, select, text
from pydantic_settings import BaseSettings

from utils.setting import Settings



settings = Settings()
engine_url = create_engine(settings.DATABASE_URL, echo=True)


def conn():
    SQLModel.metadata.create_all(engine_url)

    # import os
    # sql_file_path = os.path.join(os.path.dirname(__file__), "setup.sql")
    # session = get_session()
    # with open(sql_file_path, 'r') as file:
    #     sql_script = file.read()
    #     session.exec(text(sql_script))
    # session.commit()
    pass

def get_session():
    with Session(engine_url) as session:
        yield session